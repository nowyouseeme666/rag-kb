"""验证 RAG 知识库检索是否正常"""
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import config

embeddings = HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Chroma(
    persist_directory=config.CHROMA_DIR,
    embedding_function=embeddings,
)

results = vectorstore.similarity_search("LangChain 是什么", k=3)

print(f"检索到 {len(results)} 条结果：")
for i, doc in enumerate(results, 1):
    print(f"\n--- 结果 {i} (来源: {doc.metadata.get('source', 'unknown')}) ---")
    print(doc.page_content[:200] + "...")
