---
created: 2026-06-02T12:51:34 (UTC +08:00)
tags: []
source: https://langchain-doc.cn/v1/python/langgraph/errors/MISSING_CHECKPOINTER.html
author: 
---

# MISSING_CHECKPOINTER

> ## Excerpt
> 您正在尝试使用LangGraph内置的持久化功能，但未提供检查点工具。 这种情况发生在@[StateGraph][StateGraph]或@[@entrypoint]的compile()方法中缺少checkpointer时。 故障排除 以下方法可能有助于解决此错误： 初始化并将检查点工具传递给@[StateGraph][StateGraph]或@[@e...

---
1.  [LangChain 中文教程](https://langchain-doc.cn/)
2.  [V1](https://langchain-doc.cn/v1/)
3.  [Python](https://langchain-doc.cn/v1/python/)
4.  [Langgraph](https://langchain-doc.cn/v1/python/langgraph/)
5.  [Errors](https://langchain-doc.cn/v1/python/langgraph/errors/)
6.  [MISSING\_CHECKPOINTER](https://langchain-doc.cn/v1/python/langgraph/errors/MISSING_CHECKPOINTER.html)

您正在尝试使用LangGraph内置的持久化功能，但未提供检查点工具。

这种情况发生在@\[`StateGraph`\]\[StateGraph\]或@\[`@entrypoint`\]的`compile()`方法中缺少`checkpointer`时。

## [故障排除](https://langchain-doc.cn/v1/python/langgraph/errors/MISSING_CHECKPOINTER.html#%E6%95%85%E9%9A%9C%E6%8E%92%E9%99%A4)

以下方法可能有助于解决此错误：

-   初始化并将检查点工具传递给@\[`StateGraph`\]\[StateGraph\]或@\[`@entrypoint`\]的`compile()`方法。

```python
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# Graph API
graph = StateGraph(...).compile(checkpointer=checkpointer)

# Functional API
@entrypoint(checkpointer=checkpointer)
def workflow(messages: list[str]) -> str:
    ...
```

```typescript
import { InMemorySaver, StateGraph } from "@langchain/langgraph";
const checkpointer = new InMemorySaver();

// Graph API
import { StateGraph } from "@langchain/langgraph";
const graph = new StateGraph(...).compile({ checkpointer });

// Functional API
import { entrypoint } from "@langchain/langgraph";
const workflow = entrypoint(
    { checkpointer, name: "workflow" },
    async (messages: string[]) => {
        // ...
    }
);
```

-   使用LangGraph API，这样您就不需要手动实现或配置检查点工具。API会为您处理所有持久化基础设施。

## [相关链接](https://langchain-doc.cn/v1/python/langgraph/errors/MISSING_CHECKPOINTER.html#%E7%9B%B8%E5%85%B3%E9%93%BE%E6%8E%A5)

-   阅读更多关于[持久化](https://langchain-doc.cn/v1/python/langgraph/persistence)的信息。
