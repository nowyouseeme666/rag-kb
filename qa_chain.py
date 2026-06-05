"""
RAG 问答链 —— 加载 ChromaDB，构建 LCEL 管道
"""
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings

import config


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


def build_qa_chain():
    """构建并返回 RAG QA Chain（LCEL 管道）"""

    # ── 1. 加载 Embedding 模型 ──
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # ── 2. 加载 ChromaDB ──
    vectorstore = Chroma(
        persist_directory=config.CHROMA_DIR,
        embedding_function=embeddings,
    )

    # ── 3. 检索函数 ──
    def _retrieve(query: str):
        """检索：优先用分数过滤，若分数不可靠则直接返回 top-k"""
        results = vectorstore.similarity_search_with_relevance_scores(
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

    # ── 4. 构建 Prompt 模板 ──
    system_prompt = (
        "你是一个 Agent 开发知识库助手。"
        "请根据下面「参考片段」中的内容回答问题。"
        "规则：\n"
        "1. 用简洁清晰的中文回答，分段组织内容\n"
        "2. 引用参考片段中的信息时，在句末标注 [来源: xxx.md]\n"
        "3. 如果多个来源都相关，分别标注\n"
        "4. 不要在回答中复制「── 参考片段」这种内部标记\n"
        "5. 如果参考片段为空或与问题完全无关，请回答「未找到与问题相关的信息」"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{context}\n\n用户问题：{question}"),
        ]
    )

    # ── 5. 初始化 LLM ──
    llm = ChatDeepSeek(model=config.LLM_MODEL)

    # ── 6. LCEL 管道 ──
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
