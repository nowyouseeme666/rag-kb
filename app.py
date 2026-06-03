"""
Agent 开发知识库 — Streamlit Web 界面
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
from qa_chain import build_qa_chain

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
        padding-top: 2rem;
    }

    /* ── 排版 ── */
    .stMarkdown {
        line-height: 1.7;
    }
    .stMarkdown p {
        margin-bottom: 0.8rem;
    }
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

    /* ── 输入框：缩小 + 居中 ── */
    textarea {
        font-size: 0.925rem !important;
        line-height: 1.55 !important;
        border-radius: 8px !important;
        border: 1px solid #d4d4d4 !important;
        max-width: 600px;
        margin: 0 auto;
        display: block;
    }
    textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
    }

    /* ── 表单容器居中 ── */
    [data-testid="stForm"] {
        max-width: 640px;
        margin: 0 auto;
    }

    /* ── 按钮 ── */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.875rem;
        padding: 0.4rem 1.25rem;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-size: 0.85rem;
        color: #666;
    }

    /* ── 空状态引导 ── */
    .empty-hint {
        color: #888;
        font-size: 0.875rem;
        text-align: center;
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
    """RAG Chain（全局单例）"""
    return build_qa_chain()


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


# ── 侧边栏：向量库统计 ──

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

    if st.button("🗑️ 清空输入", use_container_width=True):
        st.session_state.question_input = ""

# ── 主区域 ──

st.title("Agent 开发知识库")
st.caption(
    "基于 RAG 检索增强生成，覆盖 LangChain、LangGraph、DeepSeek 等技术文档。"
    "答案由 DeepSeek V4-Flash 生成，可溯源至原始文档。"
)

# ── 引导文字 ──
st.markdown(
    "<p style='"
    "text-align: center;"
    "font-family: Georgia, 'Times New Roman', serif;"
    "font-style: italic;"
    "font-size: 0.85rem;"
    "letter-spacing: 0.12em;"
    "color: #999;"
    "margin: 1.75rem 0 0.75rem 0;"
    "text-transform: uppercase;"
    "'>Pose Your Questions</p>",
    unsafe_allow_html=True,
)

# ── 问答表单 ──

default_q = st.session_state.get("question_input", "")

with st.form("query_form", clear_on_submit=False):
    question = st.text_area(
        "输入问题",
        value=default_q,
        placeholder=(
            "LangChain 的 LCEL 管道符有什么作用？"
        ),
        height=52,
        label_visibility="collapsed",
        key="question_input",
    )
    submitted = st.form_submit_button("🔍 查询", use_container_width=True)

# ── 处理查询 ──

if submitted and question.strip():
    with st.spinner("正在检索知识库并生成回答..."):
        try:
            chain = _get_chain()
            answer = chain.invoke({"question": question.strip()})
        except Exception as e:
            st.error(f"查询失败 [{type(e).__name__}]：{e}")
            st.stop()

    st.markdown("---")
    st.markdown("### 💬 回答")
    st.markdown(answer)

    # 来源展开
    retrieved = _retrieve_for_display(question.strip())
    with st.expander("📎 查看引用来源", expanded=False):
        if not retrieved:
            st.info("未检索到高度相关的文档片段（相似度均低于阈值）。")
        else:
            for i, (doc, score) in enumerate(retrieved, 1):
                source_name = doc.metadata.get("source", "unknown")
                st.markdown(
                    f"**片段 {i}** · "
                    f"来源 `{source_name}` · "
                    f"相关度 `{score:.3f}`"
                )
                st.markdown(doc.page_content)
                if i < len(retrieved):
                    st.divider()

elif submitted and not question.strip():
    st.warning("请输入问题后再查询。")

# ── 空状态引导 ──

if not submitted:
    st.markdown("---")
    st.markdown(
        "<p class='empty-hint'>"
        "输入问题后点击「查询」或按 Ctrl+Enter 提交"
        "</p>",
        unsafe_allow_html=True,
    )
