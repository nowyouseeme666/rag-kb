"""
RAG 知识库项目配置常量
"""

# 文档切分配置
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Embedding 模型
EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"

# LLM 配置
LLM_MODEL = "deepseek-chat"
RETRIEVER_K = 4
# ChromaDB 的 relevance_score 范围不在 [0,1]（约 -0.1 ~ 0.3），阈值需按实际调优
SIMILARITY_THRESHOLD = -0.1

# 存储路径
CHROMA_DIR = "./chroma_db"
DATA_DIR = "./data"
