# LCEL（LangChain Expression Language）

## 概述

LCEL 是 LangChain 的声明式管道语言，用于构建可组合的 LLM 应用链。

## 核心概念

LCEL 使用 `|`（管道操作符）将多个 Runnable 组件串联。每个组件的输出自动成为下一个组件的输入。

## 基本语法

```python
chain = prompt | model | output_parser
```

上述代码将 prompt、model 和 output_parser 三个组件串联成一个可执行的 chain。

## 使用管道符的好处

使用管道符构建的 chain 具有以下特点：
1. 自动支持 async/await 异步调用
2. 支持 stream 流式输出
3. 支持 batch 批量处理
4. 内置重试和回退机制
5. 中间结果可通过 RunnablePassthrough 传递

## 常见使用场景

### 场景一：创建简单的问答链

将 prompt 模板、LLM 和输出解析器串联，构建最基础的问答链。

### 场景二：RAG 检索增强链

将检索器、文档格式化器和 LLM 串联，实现基于知识库的问答。

### 场景三：多步推理链

通过 RunnableLambda 插入自定义的处理步骤，实现多步推理逻辑。

## RunnablePassthrough 的用法

RunnablePassthrough 用于在管道中传递数据而不做任何修改。它在以下场景特别有用：
- 需要同时传递多个变量到下游组件
- 需要在管道中保留原始输入供后续使用
- 作为占位符使用

## LCEL 与旧版 Chain 的区别

相比旧版的 LLMChain、ConversationChain 等，LCEL 提供了：
- 更简洁的代码
- 更好的可组合性
- 统一的接口
- 内置的并行处理支持
