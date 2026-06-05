"""
Agent 开发知识库 — Streamlit Web 界面（多轮对话）
"""
import os
import sys

# 加载 .env（必须在其他模块导入前执行，否则 HuggingFace 直连被墙）
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import config
from qa_chain import _format_history, build_conversational_chain

# ── 页面配置 ──
st.set_page_config(
    page_title="Agent开发知识库",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── 自定义样式 ──
st.markdown(
    """
<style>
    /* ── 全局 ── */
    .stMain {
        padding-top: 1rem;
    }

    /* ── 排版 ── */
    h1 {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }
    h2 { font-size: 1.25rem !important; font-weight: 600 !important; }
    h3 { font-size: 1.1rem !important; font-weight: 600 !important; }

    /* ── 代码块 ── */
    .stMarkdown pre {
        border-radius: 6px;
        border: 1px solid #e5e5e5;
        background: #f5f5f5;
    }
    .stMarkdown code {
        font-size: 0.875em;
    }

    /* ── 引用块 ── */
    .stMarkdown blockquote {
        border-left: 3px solid #2563EB;
        padding-left: 1rem;
        color: #555;
    }

    /* ── 来源引用小字 ── */
    .source-tag {
        display: inline-block;
        font-size: 0.75rem;
        color: #888;
        background: #f0f0f0;
        border-radius: 4px;
        padding: 1px 6px;
        margin-right: 4px;
    }

    /* ── 空状态 ── */
    .welcome-hint {
        text-align: center;
        color: #999;
        padding: 3rem 1rem;
        font-size: 0.925rem;
        line-height: 1.8;
    }
    .welcome-hint p {
        margin: 0.3rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ── 资源缓存 ──

@st.cache_resource
def _get_embeddings():
    """Embedding 模型（全局单例）"""
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


@st.cache_resource
def _get_vectorstore():
    """ChromaDB 向量库（全局单例）"""
    return Chroma(
        persist_directory=config.CHROMA_DIR,
        embedding_function=_get_embeddings(),
    )


@st.cache_resource
def _get_chain():
    """多轮对话 RAG Chain（全局单例）"""
    return build_conversational_chain()


def _retrieve_for_display(query: str):
    """检索文档用于来源展示"""
    vs = _get_vectorstore()
    results = vs.similarity_search_with_relevance_scores(
        query, k=config.RETRIEVER_K
    )
    filtered = [
        (doc, score) for doc, score in results
        if score >= config.SIMILARITY_THRESHOLD
    ]
    if not filtered and results:
        filtered = [(doc, score) for doc, score in results[:2]]
    return filtered


# ── 会话初始化 ──

if "messages" not in st.session_state:
    st.session_state.messages = []


# ── 侧边栏 ──

with st.sidebar:
    st.markdown("## 🧠 Agent 知识库")

    try:
        vs = _get_vectorstore()
        total_chunks = vs._collection.count()

        col1, col2 = st.columns(2)
        col1.metric("📄 文档块", f"{total_chunks}")

        if total_chunks > 0:
            sample = vs._collection.get(
                limit=min(total_chunks, 500),
                include=["metadatas"],
            )
            if sample["metadatas"]:
                sources = sorted(set(
                    m.get("source", "unknown")
                    for m in sample["metadatas"]
                ))
                col2.metric("📁 文档", f"{len(sources)}")
    except Exception as e:
        st.error(f"向量库连接失败：{e}")

    st.divider()

    st.caption(f"Embedding: `{config.EMBEDDING_MODEL}`")
    st.caption(f"LLM: `{config.LLM_MODEL}`")
    st.caption(f"Top-K: {config.RETRIEVER_K}")

    st.divider()

    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ── 主区域 ──

st.title("Agent 开发知识库")
st.caption(
    "基于 RAG 检索增强生成，覆盖 LangChain、LangGraph、DeepSeek 等技术文档。"
    "支持多轮对话，答案可溯源至原始文档。"
)

# ── 对话历史渲染 ──

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 空状态欢迎语 ──

if not st.session_state.messages:
    st.markdown(
        "<div class='welcome-hint'>"
        "<p>👋 输入你的问题，开始查询知识库</p>"
        "<p style='font-size:0.8rem;color:#bbb;'>支持多轮对话，会自动结合上文理解你的问题</p>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── 输入框 ──

if question := st.chat_input("输入问题，按 Enter 发送…"):
    # 1. 添加用户消息
    st.session_state.messages.append({"role": "user", "content": question})

    # 2. 渲染用户消息
    with st.chat_message("user"):
        st.markdown(question)

    # 3. 生成回答
    with st.chat_message("assistant"):
        # 构建历史文本（不包含当前问题）
        history_messages = st.session_state.messages[:-1]
        history_text = _format_history(history_messages)

        with st.spinner(""):
            try:
                chain = _get_chain()
                answer = chain.invoke({
                    "question": question,
                    "chat_history": history_text,
                })
                st.markdown(answer)
            except Exception as e:
                error_msg = f"查询失败 [{type(e).__name__}]：{e}"
                st.error(error_msg)
                answer = f"（系统错误：{error_msg}）"

        # 4. 来源展示
        retrieved = _retrieve_for_display(question)
        if retrieved:
            with st.expander("📎 查看引用来源"):
                for i, (doc, score) in enumerate(retrieved, 1):
                    source_name = doc.metadata.get("source", "unknown")
                    st.caption(
                        f"**片段 {i}** · `{source_name}` · 相关度 {score:.3f}"
                    )
                    st.markdown(doc.page_content)
                    if i < len(retrieved):
                        st.divider()

    # 5. 保存回答到历史
    st.session_state.messages.append({"role": "assistant", "content": answer})
