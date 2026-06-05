"""
RAG 知识库文档入库脚本

扫描 ./data/ 目录下的 .md 文件，切分后向量化存入 ChromaDB。
"""
import glob
import os

# 加载 .env（必须在其他模块导入前执行，否则 HuggingFace 直连被墙）
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


def ingest() -> None:
    """主入库流程：扫描 → 加载 → 切分 → 向量化 → 持久化"""

    # 1. 扫描 ./data/ 目录下所有 .md 文件
    md_files = glob.glob(os.path.join(config.DATA_DIR, "*.md"))
    if not md_files:
        print(f"未在 {config.DATA_DIR}/ 目录下找到 .md 文件，请先放入文档再运行。")
        return

    print(f"扫描到 {len(md_files)} 个 .md 文件\n")

    # 2. 用 TextLoader 逐文件加载，metadata 记录 source
    all_documents = []
    for file_path in sorted(md_files):
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()

        # 3. 为每个文档标记来源文件名（不含路径）
        filename = os.path.basename(file_path)
        for doc in docs:
            doc.metadata["source"] = filename

        all_documents.extend(docs)
        print(f"  ✓ 已加载: {filename}  ({len(docs)} 页)")

    # 4. 文档切分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=[
            "\n\n",     # 段落
            "\n",       # 换行
            "。",       # 中文句号
            "！",       # 中文感叹号
            "？",       # 中文问号
            "；",       # 中文分号
            "，",       # 中文逗号
            ".",        # 英文句号
            " ",        # 空格
            "",         # 字符级兜底
        ],
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"\n文档切分完成，共 {len(chunks)} 个 chunk")

    # 5. 加载 Embedding 模型（首次运行自动从 HuggingFace 下载）
    print(f"\n正在加载 Embedding 模型: {config.EMBEDDING_MODEL} ...")
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    print("模型加载完成")

    # 6. 向量化并持久化到 ChromaDB
    print(f"\n正在向量化并写入 {config.CHROMA_DIR} ...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.CHROMA_DIR,
    )
    print("持久化完成")

    # 7. 入库总结
    print(f"\n{'='*40}")
    print(f"  入库完成！")
    print(f"  文件数 : {len(md_files)} 个")
    print(f"  Chunk 数: {len(chunks)} 个")
    print(f"  存储位置: {config.CHROMA_DIR}")
    print(f"{'='*40}")


if __name__ == "__main__":
    ingest()
