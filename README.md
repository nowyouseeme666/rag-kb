# Agent 开发知识库 — RAG 问答系统

基于 LangChain + Streamlit 构建的 RAG（检索增强生成）问答系统，面向 Agent 开发场景，支持文档入库、语义检索和多轮对话。

## 技术栈

| 组件 | 选型 | 说明 |
|------|------|------|
| LLM | DeepSeek V4-Flash (`deepseek-chat`) | 性价比高，中文理解能力强 |
| Embedding | `BAAI/bge-small-zh-v1.5` | 中文语义向量，轻量高效 |
| 向量库 | ChromaDB | 本地持久化，零配置 |
| 框架 | LangChain LCEL | 声明式管道，可读性强 |
| 界面 | Streamlit | Web UI，支持多轮对话 |

## 快速开始

### 1. 安装依赖

```bash
cd rag-kb
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 设置 API Key

```bash
# 在项目根目录创建 .env 文件，写入：
DEEPSEEK_API_KEY=你的DeepSeek密钥
```

### 3. 文档入库

```bash
python ingest.py
```

首次运行会自动从 HuggingFace 下载 Embedding 模型（约 100MB）。如果下载失败，可设置镜像：

```bash
set HF_ENDPOINT=https://hf-mirror.com
python ingest.py
```

### 4. 启动 Web 界面

```bash
streamlit run app.py
```

浏览器打开 `http://localhost:8501` 即可使用。

特性：
- **多轮对话**：自动结合上文理解问题
- **来源溯源**：每个回答可展开查看引用片段和相关度
- **侧边栏**：实时显示文档块数量、已入库文档数、当前配置参数
- **一键清空**：侧边栏按钮清空对话历史

## 文档库内容

`data/` 目录包含以下技术文档，入库后可通过问答检索：

| 分类 | 文档 |
|------|------|
| LangChain | LCEL、ChatBot、Installation、Structured Output、Agents、Tool Calling |
| LangGraph | Graph API、Graph API Overview、State、Conditional、Checkpoint、Memory、Missing Checkpointer、Long-term Memory、Streaming、ReAct、Subgraph、Agentic RAG、Supervisor Agent、Tool-calling Agent |
| DeepSeek | API Overview、Chat Prefix、Chat、Error Codes、Function Calling、Pricing、Rate Limit、Reasoner、Token Usage |

## 项目结构

```
rag-kb/
├── app.py             # Streamlit Web 界面（多轮对话）
├── config.py          # 配置常量（chunk_size, 模型, 阈值等）
├── ingest.py          # 文档入库脚本（扫描 data/ → 切分 → 向量化 → ChromaDB）
├── qa_chain.py        # RAG 问答链（LCEL 管道：检索 → 提示 → LLM → 输出）
├── fetch_docs.py      # 文档抓取脚本（从官方文档站拉取 .md）
├── requirements.txt   # Python 依赖
├── README.md          # 本文件
├── .env               # 环境变量（API Key 等，不入库）
├── data/              # 待入库的 .md 文档（27 篇）
├── chroma_db/         # ChromaDB 持久化目录（ingest 后生成）
└── tests/
    ├── test_qa.py     # 功能验证脚本
    └── data/          # 测试专用文档
        ├── lcel.md
        ├── rag.md
        └── langgraph.md
```

### 文件说明

| 文件 | 职责 |
|------|------|
| `app.py` | Streamlit Web 界面：资源缓存、多轮对话、来源展示、侧边栏状态 |
| `config.py` | 所有可调参数集中管理：chunk 切分、模型名称、检索 K 值、相似度阈值 |
| `ingest.py` | 扫描 `data/` → TextLoader 加载 → RecursiveCharacterTextSplitter 切分 → bge-small-zh 向量化 → 写入 ChromaDB |
| `qa_chain.py` | 加载 ChromaDB → 构建 LCEL 管道 → `build_conversational_chain()` 支持多轮对话 |
| `fetch_docs.py` | 从 LangChain/LangGraph/DeepSeek 官方文档站抓取内容，自动生成 .md 文件 |

## 技术选型理由

### 为什么选 bge-small-zh-v1.5？

- **中文原生优化**：BAAI 专门针对中文训练，在 C-MTEB 基准上表现优异
- **体积小**：模型仅 ~100MB，CPU 推理即可，无需 GPU
- **归一化输出**：embedding 经 L2 归一化后可直接用余弦相似度比较

### 为什么 chunk_size=800，overlap=100？

- **800 字符**在中文场景下约为 400-500 个 token，适配 DeepSeek 的上下文窗口
- **100 字符 overlap**保证段落边界处的语义不会因切分而丢失
- 针对中文标点（`。！？；，`）做了分隔符定制，避免在句子中间切断

### 为什么用 RAG 而不是微调？

- **知识可更新**：新增文档只需重新入库，无需重新训练
- **可溯源**：每个回答都能追溯来源文档，降低幻觉风险
- **成本低**：无需 GPU 微调，日常运行只需 CPU + API 调用
- **适合场景**：知识库问答天然适合 RAG——知识是静态文档，推理交给 LLM

## 已知限制

1. **Embedding 模型仅支持中文**：`bge-small-zh-v1.5` 对英文检索效果有限，需切换到多语言模型
2. **相似度阈值固定为 0.5**：阈值过低可能引入噪声，过高可能漏掉相关结果，不同场景需调优
3. **ChromaDB 为本地单机**：不支持分布式部署和多用户并发
4. **检索策略为朴素相似度**：未使用 HyDE、Multi-Query、Rerank 等进阶技术
