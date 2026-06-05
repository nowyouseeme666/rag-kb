---
created: 2026-06-05T11:58:34 (UTC +08:00)
tags: []
source: https://langchain-doc.cn/v1/python/langgraph/releases/langgraph-v1.html#create-react-agent-%E5%B7%B2%E5%BC%83%E7%94%A8
author: 
---

# v1 新特性 | LangChain 中文文档

> ## Excerpt
> LangGraph v1 是一个以稳定性为重点的 Agent 运行时版本。 它保持了核心图 API 和执行模型不变，同时改进了类型安全、文档和开发人员的人体工程学。 它旨在与 LangChain v1（其 create_agent 是基于 LangGraph 构建的）协同工作，这样你就可以从高层次开始，并在需要时下钻到更细粒度的控制。 稳定的核心 AP...

---
1.  [LangChain 中文教程](https://langchain-doc.cn/)
2.  [V1](https://langchain-doc.cn/v1/)
3.  [Python](https://langchain-doc.cn/v1/python/)
4.  [Langgraph](https://langchain-doc.cn/v1/python/langgraph/)
5.  [Releases](https://langchain-doc.cn/v1/python/langgraph/releases/)
6.  [v1 新特性](https://langchain-doc.cn/v1/python/langgraph/releases/langgraph-v1.html)

<ins data-ad-client="ca-pub-1595614882063454" data-ad-slot="5798145835" data-adsbygoogle-status="done" data-ad-status="unfill-optimized"><div data-google-ad-efd="true" id="aswift_2_host"><p>深入探索</p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>LangSmith 平台</span></p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>中文文档翻译</span></p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>LangChain 教程</span></p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>Deployment</span></p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>框架操作指南</span></p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>LangChain 文档</span></p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>框架集成服务</span></p><p><span><svg viewBox="0 -960 960 960" width="16px" height="16px" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: rgb(26, 115, 232) !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important; position: relative !important; top: 3px !important;"><path d="M168-144q-29.7 0-50.85-21.15Q96-186.3 96-216v-528q0-29.7 21.15-50.85Q138.3-816 168-816h624q29.7 0 50.85 21.15Q864-773.7 864-744v528q0 29.7-21.15 50.85Q821.7-144 792-144H168Zm0-72h624v-528H168v528Zm72-96h480v-72H240v72Zm0-144h168v-216H240v216Zm240 0h240v-72H480v72Zm0-144h240v-72H480v72ZM168-216v-528 528Z" style="animation: initial !important; background: initial !important; border: 0px !important; box-shadow: none !important; color: inherit !important; cursor: inherit !important; direction: inherit !important; display: inline !important; fill: currentcolor !important; filter: initial !important; float: none !important; margin: 0px !important; opacity: initial !important; outline: 0px !important; overflow: initial !important; padding: 0px !important; stroke: initial !important; transform: initial !important; vertical-align: initial !important; visibility: inherit !important;"></path></svg></span><span>LangGraph 教程</span></p></div></ins>

**LangGraph v1 是一个以稳定性为重点的 Agent 运行时版本。** 它保持了核心图 API 和执行模型不变，同时改进了类型安全、文档和开发人员的人体工程学。

它旨在与 [LangChain v1](https://langchain-doc.cn/v1/python/releases/langchain-v1)（其 `create_agent` 是基于 LangGraph 构建的）协同工作，这样你就可以从高层次开始，并在需要时下钻到更细粒度的控制。

-   **稳定的核心 API**
    
    图元语（状态、节点、边）和执行/运行时模型保持不变，使得升级过程直截了当。
    
-   **默认可靠性**
    
    具有检查点（checkpointing）、持久化、流式传输和人工干预（human-in-the-loop）的持久化执行（durable execution）仍然是头等功能。
    
-   **与 LangChain v1 无缝衔接**
    
    LangChain 的 `create_agent` 运行在 LangGraph 上。使用 LangChain 可以快速入门；需要自定义编排时，则下钻到 LangGraph。
    

要升级，请执行以下操作：

```bash
pip install -U langgraph
```

或

```bash
uv add langgraph
```

## [`create_react_agent` 已弃用](https://langchain-doc.cn/v1/python/langgraph/releases/langgraph-v1.html#create-react-agent-%E5%B7%B2%E5%BC%83%E7%94%A8)

LangGraph 的 [`create_react_agent`](https://langchain-doc.cn/v1/python/langgraph/releases/%5Bhttps:/reference.langchain.com/python/langgraph/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent%5D(https://reference.langchain.com/python/langgraph/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)) 预构建功能已被弃用，取而代之的是 LangChain 的 [`create_agent`](https://langchain-doc.cn/v1/python/langgraph/releases/%5Bhttps:/reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent%5D(https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent))。它提供了一个更简单的接口，并通过引入**中间件**提供了更大的自定义潜力。

-   有关新的 [`create_agent`](https://langchain-doc.cn/v1/python/langgraph/releases/%5Bhttps:/reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent%5D(https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent)) API 的信息，请参阅 [LangChain v1 发布说明](https://langchain-doc.cn/v1/python/releases/langchain-v1#create-agent)。
-   有关从 [`create_react_agent`](https://langchain-doc.cn/v1/python/langgraph/releases/%5Bhttps:/reference.langchain.com/python/langgraph/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent%5D(https://reference.langchain.com/python/langgraph/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)) 迁移到 [`create_agent`](https://langchain-doc.cn/v1/python/langgraph/releases/%5Bhttps:/reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent%5D(https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent)) 的信息，请参阅 [LangChain v1 迁移指南](https://langchain-doc.cn/v1/python/migrate/langchain-v1#create-agent)。

## [报告问题](https://langchain-doc.cn/v1/python/langgraph/releases/langgraph-v1.html#%E6%8A%A5%E5%91%8A%E9%97%AE%E9%A2%98)

请在 [GitHub](https://github.com/langchain-ai/langgraph/issues) 上使用 [`'v1'` 标签](https://langchain-doc.cn/v1/python/langgraph/releases/%5Bhttps://github.com/langchain-ai/langgraph/issues?q=state%3Aopen%20label%3Av1%5D(https://github.com/langchain-ai/langgraph/issues?q=state%3Aopen%20label%3Av1)) 报告在使用 1.0 版本时发现的任何问题。

## [更多资源](https://langchain-doc.cn/v1/python/langgraph/releases/langgraph-v1.html#%E6%9B%B4%E5%A4%9A%E8%B5%84%E6%BA%90)

-   **LangGraph 1.0**
    
    阅读公告
    
-   **概述**
    
    LangGraph 是什么以及何时使用它
    
-   **图 API**
    
    使用状态、节点和边构建图
    
-   **LangChain Agents**
    
    基于 LangGraph 构建的高层次 Agent
    
-   **迁移指南**
    
    如何迁移到 LangGraph v1
    
-   **GitHub**
    
    报告问题或贡献代码
    

## [另请参阅](https://langchain-doc.cn/v1/python/langgraph/releases/langgraph-v1.html#%E5%8F%A6%E8%AF%B7%E5%8F%82%E9%98%85)

-   [版本控制](https://langchain-doc.cn/v1/python/versioning) - 了解版本号
-   [发布策略](https://langchain-doc.cn/v1/python/release-policy) - 详细的发布策略
