---
created: 2026-06-05T11:59:53 (UTC +08:00)
tags: []
source: https://langchain-doc.cn/v1/python/langgraph/ui.html#%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5
author: 
---

# Agent聊天用户界面

> ## Excerpt
> LangChain 提供了一个功能强大的预构建用户界面，可与使用 create_agent 创建的智能体无缝协作。无论您是在本地运行还是在已部署的环境中（例如 ），该 UI 都旨在通过最少的设置，为您的智能体提供丰富、交互式的体验。 智能体聊天用户界面（Agent Chat UI） Agent Chat UI 是一个 Next.js 应用程序，它提供了...

---
1.  [LangChain 中文教程](https://langchain-doc.cn/)
2.  [V1](https://langchain-doc.cn/v1/)
3.  [Python](https://langchain-doc.cn/v1/python/)
4.  [Langgraph](https://langchain-doc.cn/v1/python/langgraph/)
5.  [Agent聊天用户界面](https://langchain-doc.cn/v1/python/langgraph/ui.html)

LangChain 提供了一个功能强大的预构建用户界面，可与使用 [`create_agent`](https://langchain-doc.cn/v1/python/langchain/agents) 创建的智能体无缝协作。无论您是在本地运行还是在已部署的环境中（例如 [LangSmith](https://langchain-doc.cn/langsmith/)），该 UI 都旨在通过最少的设置，为您的智能体提供**丰富、交互式的体验**。

## [智能体聊天用户界面（Agent Chat UI）](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E6%99%BA%E8%83%BD%E4%BD%93%E8%81%8A%E5%A4%A9%E7%94%A8%E6%88%B7%E7%95%8C%E9%9D%A2-agent-chat-ui)

[Agent Chat UI](https://github.com/langchain-ai/agent-chat-ui) 是一个 Next.js 应用程序，它提供了一个**会话式界面**，用于与任何 LangChain 智能体进行交互。它支持**实时聊天**、**工具可视化**以及**时间旅行调试**和**状态分叉**等高级功能。

Agent Chat UI 是开源的，可以根据您的应用需求进行调整。

<iframe width="560" height="315" src="https://www.youtube.com/embed/lInrwVnZ83o?si=Uw66mPtCERJm0EjU" title="Studio" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>

### [特性](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E7%89%B9%E6%80%A7)

#### [工具可视化](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E5%B7%A5%E5%85%B7%E5%8F%AF%E8%A7%86%E5%8C%96)

Studio 会在一个直观的界面中自动渲染工具调用和结果。

> \[工具可视化 GIF 示例\]
> 
> ![studio_tools.gif](https://langchain-doc.cn/img/langchain-5e9cc07a/zA84oCipUuW8ow2z/studio_tools.gif)

#### [时间旅行调试](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E6%97%B6%E9%97%B4%E6%97%85%E8%A1%8C%E8%B0%83%E8%AF%95)

浏览会话历史，并可以从任何时间点**分叉**（fork）新的会话。

> \[时间旅行调试 GIF 示例\]
> 
> ![studio_fork.gif](https://langchain-doc.cn/img/langchain-5e9cc07a/zA84oCipUuW8ow2z/studio_fork.gif)

#### [状态检查](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5)

在执行过程中的任何时间点**查看和修改**智能体的状态。

> \[状态检查 GIF 示例\]
> 
> ![studio_state.gif](https://langchain-doc.cn/img/langchain-5e9cc07a/zA84oCipUuW8ow2z/studio_state.gif)

#### [人在回路（Human-in-the-loop）](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E4%BA%BA%E5%9C%A8%E5%9B%9E%E8%B7%AF-human-in-the-loop)

内置支持**审查和响应**智能体的请求。

> \[人在回路 GIF 示例\]
> 
> ![studio_hitl.gif](https://langchain-doc.cn/img/langchain-5e9cc07a/zA84oCipUuW8ow2z/studio_hitl.gif)

> **提示**
> 
> 您可以在 Agent Chat UI 中使用**生成式 UI**。有关更多信息，请参阅 [使用 LangGraph 实现生成式用户界面](https://langchain-doc.cn/langsmith/generative-ui-react)。

### [快速入门](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8)

最快入门的方法是使用托管版本：

1.  **访问 [Agent Chat UI](https://agentchat.vercel.app/)**
2.  通过输入您的**部署 URL 或本地服务器地址**来**连接您的智能体**。
3.  **开始聊天**——UI 将自动检测并渲染工具调用和中断。

### [本地开发](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E6%9C%AC%E5%9C%B0%E5%BC%80%E5%8F%91)

对于定制或本地开发，您可以在本地运行 Agent Chat UI：

#### [使用npx](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E4%BD%BF%E7%94%A8npx)

```shell
# Create a new Agent Chat UI project
npx create-agent-chat-app --project-name my-chat-ui
cd my-chat-ui

# Install dependencies and start
pnpm install
pnpm dev
```

#### [克隆仓库](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E5%85%8B%E9%9A%86%E4%BB%93%E5%BA%93)

```shell
# Clone the repository
git clone https://github.com/langchain-ai/agent-chat-ui.git
cd agent-chat-ui

# Install dependencies and start
pnpm install
pnpm dev
```

### [连接到您的智能体](https://langchain-doc.cn/v1/python/langgraph/ui.html#%E8%BF%9E%E6%8E%A5%E5%88%B0%E6%82%A8%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93)

Agent Chat UI 可以连接到**本地** \[/v1/python/langgraph/studio#setup-local-langgraph-server\] 和**已部署的智能体** \[/v1/python/langgraph/deploy\]。

启动 Agent Chat UI 后，您需要配置它以连接到您的智能体：

1.  **Graph ID（图 ID）**：输入您的图名称（可在您的 `langgraph.json` 文件中的 `graphs` 下找到）。
2.  **Deployment URL（部署 URL）**：您的 LangGraph 服务器的端点（例如，本地开发为 `http://localhost:2024`，或您的已部署智能体的 URL）。
3.  **LangSmith API key (可选)**：添加您的 LangSmith API 密钥（如果您使用的是本地 LangGraph 服务器，则**不需要**）。

配置完成后，Agent Chat UI 将自动从您的智能体**获取并显示任何中断的线程**。

> **提示**
> 
> Agent Chat UI **开箱即用**地支持渲染工具调用和工具结果消息。要自定义显示哪些消息，请参阅 [在聊天中隐藏消息](https://github.com/langchain-ai/agent-chat-ui?tab=readme-ov-file#hiding-messages-in-the-chat)。

<ins data-ad-client="ca-pub-1595614882063454" data-ad-slot="7657898701" data-adsbygoogle-status="done" data-ad-status="unfill-optimized"><div data-google-ad-efd="true" id="aswift_3_host"><p><span aria-label="这些是与文章相关且您可能感兴趣的主题" tabindex="0" role="heading" aria-level="2">深入探索</span></p><p><span title="编程">编程</span></p><p><span title="计算机科学">计算机科学</span></p><p><span title="LangSmith 平台">LangSmith 平台</span></p></div></ins>

[

上一页

部署

](https://langchain-doc.cn/v1/python/langgraph/deploy.html)[

下一页

可观察性

](https://langchain-doc.cn/v1/python/langgraph/observability.html)
