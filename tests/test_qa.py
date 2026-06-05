"""
RAG 知识库功能测试

运行方式：
    cd rag-kb
    python tests\test_qa.py

要求：
    1. 已安装所有依赖（pip install -r requirements.txt）
    2. 测试 LLM 问答时需设置 DEEPSEEK_API_KEY 环境变量
"""
import glob
import os
import shutil
import sys
import tempfile

# 将项目根目录加入 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
from qa_chain import _format_docs, build_qa_chain


# ── 准备阶段：创建临时向量库 ──

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TMP_CHROMA_DIR = os.path.join(tempfile.gettempdir(), "rag_test_chroma")
PASS = 0
FAIL = 0


def setup():
    """加载测试文档 → 切分 → 向量化 → 写入临时 ChromaDB"""
    print("=" * 60)
    print("  准备测试环境…")
    print("=" * 60)

    # 清理旧数据
    if os.path.exists(TMP_CHROMA_DIR):
        shutil.rmtree(TMP_CHROMA_DIR)

    # 加载文档
    md_files = sorted(glob.glob(os.path.join(TEST_DATA_DIR, "*.md")))
    all_docs = []
    for fp in md_files:
        loader = TextLoader(fp, encoding="utf-8")
        docs = loader.load()
        filename = os.path.basename(fp)
        for doc in docs:
            doc.metadata["source"] = filename
        all_docs.extend(docs)

    # 切分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", ".", " ", ""],
    )
    chunks = splitter.split_documents(all_docs)

    # 向量化
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=TMP_CHROMA_DIR,
    )

    return len(chunks), embeddings, len(md_files)


def run_test(name, condition):
    """执行单个测试断言"""
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}")


# ── 测试用例 ──

def test_chunk_count(chunk_count):
    """测试 5：入库后 chunk 数量大于 0"""
    print("\n── 测试：入库验证 ──")
    run_test("ChromaDB 中的 chunk 数量大于 0", chunk_count > 0)
    print(f"       实际 chunk 数: {chunk_count}")


def test_retrieval_formatting(embeddings):
    """测试格式化函数和检索功能"""
    print("\n── 测试：检索与格式化 ──")

    vectorstore = Chroma(
        persist_directory=TMP_CHROMA_DIR,
        embedding_function=embeddings,
    )

    # 测试 LCEL 检索
    results = vectorstore.similarity_search("LCEL 是什么", k=3)
    run_test("LCEL 检索返回结果数 > 0", len(results) > 0)

    # 测试格式化输出包含来源标记
    formatted = _format_docs(results)
    run_test("格式化结果包含 [来源: 标记", "[来源:" in formatted)
    run_test("格式化结果包含段落编号", "第" in formatted and "段]" in formatted)

    # 测试空文档格式化
    empty = _format_docs([])
    run_test("空文档时提示未检索到内容", "未检索到" in empty)

    # 测试来源文档名
    sources = set(doc.metadata.get("source", "") for doc in results)
    run_test("检索结果包含 lcel.md", "lcel.md" in str(sources))


def test_rag_chain(embeddings):
    """测试完整 RAG Chain（需要 DEEPSEEK_API_KEY）"""
    print("\n── 测试：LLM 问答（需要 API Key）──")

    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("  跳过：未设置 DEEPSEEK_API_KEY 环境变量")
        return

    # 用临时向量库路径覆盖配置，构造 chain
    original_dir = config.CHROMA_DIR
    config.CHROMA_DIR = TMP_CHROMA_DIR
    try:
        chain = build_qa_chain()
    finally:
        config.CHROMA_DIR = original_dir

    # 测试 1：LCEL 相关问题
    try:
        answer1 = chain.invoke({"question": "LCEL 的管道符有什么作用？"})
        print(f"  Q: LCEL 的管道符有什么作用？")
        print(f"  A: {answer1[:150]}...")
        # LCEL 相关内容应出现在答案中，同时不能是"未找到"
        run_test(
            "能正确回答 LCEL 相关问题",
            "未找到与问题相关的信息" not in answer1
            and len(answer1) > 20
        )
    except Exception as e:
        run_test(f"能正确回答 LCEL 相关问题（异常: {e}）", False)

    # 测试 2：RAG 相关问题
    try:
        answer2 = chain.invoke({"question": "RAG 有什么优势？"})
        print(f"  Q: RAG 有什么优势？")
        print(f"  A: {answer2[:150]}...")
        run_test(
            "能正确回答 RAG 相关问题",
            "未找到与问题相关的信息" not in answer2
            and len(answer2) > 20
        )
    except Exception as e:
        run_test(f"能正确回答 RAG 相关问题（异常: {e}）", False)

    # 测试 3：无关问题
    try:
        answer3 = chain.invoke({"question": "比特币的价格是多少？"})
        print(f"  Q: 比特币的价格是多少？")
        print(f"  A: {answer3[:150]}...")
        run_test(
            "无关问题返回未找到相关信息",
            "未找到" in answer3 or "没有相关" in answer3
        )
    except Exception as e:
        run_test(f"无关问题返回未找到相关信息（异常: {e}）", False)

    # 测试 4：来源标注
    try:
        answer4 = chain.invoke({"question": "StateGraph 是什么？"})
        print(f"  Q: StateGraph 是什么？")
        print(f"  A: {answer4[:200]}...")
        run_test(
            "答案中包含来源标注",
            "[来源:" in answer4 or ".md" in answer4 or "来源" in answer4
        )
    except Exception as e:
        run_test(f"答案中包含来源标注（异常: {e}）", False)


# ── 清理 ──

def teardown():
    """删除临时 ChromaDB，处理文件锁"""
    import gc
    gc.collect()
    if os.path.exists(TMP_CHROMA_DIR):
        for attempt in range(3):
            try:
                shutil.rmtree(TMP_CHROMA_DIR)
                break
            except PermissionError:
                if attempt < 2:
                    import time
                    time.sleep(0.5)
                else:
                    print(f"  警告：无法清理临时目录 {TMP_CHROMA_DIR}")


# ── 主入口 ──

if __name__ == "__main__":
    try:
        chunk_count, embeddings, file_count = setup()
        print(f"\n  已入库 {file_count} 个文件 → {chunk_count} 个 chunk")

        test_chunk_count(chunk_count)
        test_retrieval_formatting(embeddings)
        test_rag_chain(embeddings)

    finally:
        teardown()

    # 汇总
    total = PASS + FAIL
    print(f"\n{'=' * 60}")
    print(f"  结果: {PASS}/{total} 通过, {FAIL}/{total} 失败")
    print(f"{'=' * 60}")

    sys.exit(0 if FAIL == 0 else 1)
