"""
RAG 问答链 —— 加载 ChromaDB，构建 LCEL 管道
提供两种模式:
    build_qa_chain()             — 单轮问答（CLI 用）
    build_conversational_chain() — 多轮对话（Web 用）
"""
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings

import config


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════

def _format_docs(docs) -> str:
    """将检索到的文档格式化为 LLM 上下文，来源信息独立成行便于 LLM 引用"""
    if not docs:
        return "（未检索到相关内容）"

    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        parts.append(
            f"── 参考片段 {i}（来源: {source}）──\n{doc.page_content}"
        )
    return "\n\n".join(parts)


def _format_history(messages: list[dict]) -> str:
    """将对话历史格式化为纯文本，用于 LLM 上下文压缩"""
    if not messages:
        return ""
    parts = []
    for msg in messages:
        role = "用户" if msg["role"] == "user" else "助手"
        parts.append(f"{role}：{msg['content']}")
    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════
# 共享资源（embeddings / vectorstore / llm 只初始化一次）
# ═══════════════════════════════════════════════════════════

_embeddings = None
_vectorstore = None
_llm = None


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings


def _get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=config.CHROMA_DIR,
            embedding_function=_get_embeddings(),
        )
    return _vectorstore


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatDeepSeek(model=config.LLM_MODEL)
    return _llm


def _retrieve(query: str):
    """检索：优先用分数过滤，若分数不可靠则直接返回 top-k"""
    vs = _get_vectorstore()
    results = vs.similarity_search_with_relevance_scores(
        query, k=config.RETRIEVER_K
    )
    filtered = [
        doc for doc, score in results
        if score >= config.SIMILARITY_THRESHOLD
    ]
    # 兜底：如果阈值过滤后为空，至少保留得分最高的 2 条
    if not filtered and results:
        filtered = [doc for doc, _ in results[:2]]
    return filtered


# ═══════════════════════════════════════════════════════════
# QA Prompt 模板（单轮和多轮共用）
# ═══════════════════════════════════════════════════════════

SYSTEM_PROMPT = (
    "你是一个 Agent 开发知识库助手。"
    "请严格根据下面「参考片段」中的内容回答问题，不要使用你自己的知识。"
    "规则：\n"
    "1. 用简洁清晰的中文回答，分段组织内容\n"
    "2. 引用参考片段中的信息时，在句末标注 [来源: xxx.md]\n"
    "3. 如果多个来源都相关，分别标注\n"
    "4. 不要在回答中复制「── 参考片段」这种内部标记\n"
    "5. 如果参考片段为空（显示「未检索到相关内容」），直接回答「未找到与问题相关的信息」\n"
    "6. 如果参考片段存在但内容与问题完全不相关，也回答「未找到与问题相关的信息」——不要强行关联或使用你自己的知识"
)


# ═══════════════════════════════════════════════════════════
# 单轮问答链（CLI 用，保持向后兼容）
# ═══════════════════════════════════════════════════════════

def build_qa_chain():
    """构建并返回单轮 RAG QA Chain（LCEL 管道）"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{context}\n\n用户问题：{question}"),
        ]
    )

    llm = _get_llm()

    chain = (
        {
            "context": RunnableLambda(lambda x: x["question"])
            | RunnableLambda(_retrieve)
            | RunnableLambda(_format_docs),
            "question": RunnableLambda(lambda x: x["question"]),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


# ═══════════════════════════════════════════════════════════
# 多轮对话链（Web 用）
# ═══════════════════════════════════════════════════════════

def build_conversational_chain():
    """
    构建多轮对话 RAG Chain。

    流程:
        chat_history + question
          → 上下文压缩 LLM → 独立问题
          → 检索 → 格式化文档
          → QA LLM（带原文问题） → 回答
    """

    llm = _get_llm()

    # ── 1. 问题重写 Prompt ──
    contextualize_system = (
        "Given a chat history and the latest user question which might reference "
        "context in the chat history, formulate a standalone question which can be "
        "understood without the chat history. Do NOT answer the question, just "
        "reformulate it. If the question is already self-contained, return it as is."
    )
    contextualize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_system),
            (
                "human",
                "Chat history:\n{chat_history}\n\n"
                "Question: {question}\n\n"
                "Standalone question:",
            ),
        ]
    )
    # 重写链: {chat_history, question} → standalone_question
    contextualize_chain = contextualize_prompt | llm | StrOutputParser()

    # ── 2. 重写 + 检索（合并为一步，减少 LCEL 复杂度）──
    def _rephrase_and_retrieve(inputs: dict):
        chat_history = inputs.get("chat_history", "")
        question = inputs["question"]

        if chat_history.strip():
            standalone = contextualize_chain.invoke(
                {"chat_history": chat_history, "question": question}
            )
        else:
            standalone = question

        return _retrieve(standalone)

    # ── 3. QA Prompt ──
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{context}\n\n用户问题：{question}"),
        ]
    )

    # ── 4. LCEL 管道 ──
    chain = (
        {
            "context": RunnableLambda(_rephrase_and_retrieve)
            | RunnableLambda(_format_docs),
            "question": RunnableLambda(lambda x: x["question"]),
        }
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    return chain
