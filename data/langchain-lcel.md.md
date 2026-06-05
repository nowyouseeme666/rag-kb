# LangChain LCEL（LangChain Expression Language）简介

## 什么是 LCEL？

LCEL（LangChain Expression Language）是 LangChain 推出的一种声明式语言，用于组合 AI 工作流中的各个组件。它通过管道操作符 `|` 将不同的 Runnable 对象串联起来，使代码更加简洁、可读。

## 核心概念

### Runnable 协议

LangChain 中的所有组件都实现了 `Runnable` 协议，这意味着它们都支持以下通用方法：

- `invoke()` — 同步调用，传入输入并获取输出
- `ainvoke()` — 异步调用
- `batch()` — 批量处理多个输入
- `abatch()` — 异步批量处理
- `stream()` — 流式返回结果
- `astream()` — 异步流式返回

### 管道操作符 `|`

LCEL 的核心是管道操作符 `|`，它类似于 Unix 管道，将前一个组件的输出作为后一个组件的输入：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 使用 LCEL 构建链
prompt = ChatPromptTemplate.from_template("请用一句话介绍{topic}")
model = ChatOpenAI(model="gpt-4")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

# 执行链
result = chain.invoke({"topic": "深度学习"})
```

### RunnableParallel 并行执行

当需要对同一输入进行多路处理时，可以使用 `RunnableParallel`：

```python
from langchain_core.runnables import RunnableParallel

# 同时执行翻译和摘要
chain = RunnableParallel(
    translation=translation_chain,
    summary=summary_chain,
)
```

### RunnablePassthrough 透传

`RunnablePassthrough` 用于将输入数据原样传递，或为输入添加额外字段：

```python
from langchain_core.runnables import RunnablePassthrough

chain = {
    "context": retriever,
    "question": RunnablePassthrough(),
} | prompt | model | output_parser
```

## LCEL 的优势

1. **简洁的语法** — 使用管道操作符直观地表达数据流
2. **原生异步支持** — 所有链自动支持同步和异步调用
3. **内置流式处理** — 无需额外配置即可流式返回
4. **自动并行化** — RunnableParallel 自动并行执行独立任务
5. **可观测性** — 自动集成 LangSmith 进行调试和追踪
