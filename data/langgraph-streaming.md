# 流式传输

* * *

# [流式传输](#流式传输)

LangGraph实现了一个流式传输系统，用于实时展示更新。流式传输对于增强基于LLM构建的应用程序的响应性至关重要。通过在完整响应准备好之前逐步显示输出，流式传输显著改善了用户体验(UX)，特别是在处理LLM延迟时。

LangGraph流式传输可以实现以下功能：

  * **流式传输图状态** — 使用`updates`和`values`模式获取状态更新/值。
  * **流式传输子图输出** — 包含父图和任何嵌套子图的输出。
  * **流式传输LLM令牌** — 从任何地方捕获令牌流：节点内部、子图或工具中。
  * **流式传输自定义数据** — 直接从工具函数发送自定义更新或进度信号。
  * **使用多种流式传输模式** — 可以选择`values`（完整状态）、`updates`（状态增量）、`messages`（LLM令牌+元数据）、`custom`（任意用户数据）或`debug`（详细跟踪）。



## [支持的流式传输模式](#支持的流式传输模式)

将以下流式传输模式中的一种或多种作为列表传递给`stream`或`astream`方法：

模式| 描述  
---|---  
`values`| 在图的每个步骤后流式传输状态的完整值。  
`updates`| 在图的每个步骤后流式传输状态的更新。如果在同一步骤中进行了多次更新（例如，运行了多个节点），这些更新会分别流式传输。  
`custom`| 从图节点内部流式传输自定义数据。  
`messages`| 从调用LLM的任何图节点流式传输2元组（LLM令牌，元数据）。  
`debug`| 在图执行过程中流式传输尽可能多的信息。  
  
## [基本使用示例](#基本使用示例)

LangGraph图暴露了`stream`（同步）和`astream`（异步）方法，以迭代器的形式生成流式输出。

### [Python](#python)
    
    
    for chunk in graph.stream(inputs, stream_mode="updates"):
        print(chunk)

### [JavaScript](#javascript)
    
    
    for await (const chunk of await graph.stream(inputs, {
      streamMode: "updates",
    })) {
      console.log(chunk);
    }

扩展示例：流式传输更新

### [Python](#python-1)
    
    
    from typing import TypedDict
    from langgraph.graph import StateGraph, START, END
    
    class State(TypedDict):
        topic: str
        joke: str
    
    def refine_topic(state: State):
        return {"topic": state["topic"] + " and cats"}
    
    def generate_joke(state: State):
        return {"joke": f"This is a joke about {state['topic']}"}
    
    graph = (
        StateGraph(State)
        .add_node(refine_topic)
        .add_node(generate_joke)
        .add_edge(START, "refine_topic")
        .add_edge("refine_topic", "generate_joke")
        .add_edge("generate_joke", END)
        .compile()
    )
    
    # stream()方法返回一个迭代器，生成流式输出
    for chunk in graph.stream(
        {"topic": "ice cream"},
        # 设置stream_mode="updates"以仅流式传输每个节点后图状态的更新
        # 也可以使用其他流式传输模式。详见支持的流式传输模式
        stream_mode="updates",
    ):
        print(chunk)

### [JavaScript](#javascript-1)
    
    
    import { StateGraph, START, END } from "@langchain/langgraph";
    import * as z from "zod";
    
    const State = z.object({
      topic: z.string(),
      joke: z.string(),
    });
    
    const graph = new StateGraph(State)
      .addNode("refineTopic", (state) => {
        return { topic: state.topic + " and cats" };
      })
      .addNode("generateJoke", (state) => {
        return { joke: `This is a joke about ${state.topic}` };
      })
      .addEdge(START, "refineTopic")
      .addEdge("refineTopic", "generateJoke")
      .addEdge("generateJoke", END)
      .compile();
    
    for await (const chunk of await graph.stream(
      { topic: "ice cream" },
      // 设置streamMode: "updates"以仅流式传输每个节点后图状态的更新
      // 也可以使用其他流式传输模式。详见支持的流式传输模式
      { streamMode: "updates" }
    )) {
      console.log(chunk);
    }
    
    
    {'refineTopic': {'topic': 'ice cream and cats'}}
    {'generateJoke': {'joke': 'This is a joke about ice cream and cats'}}

## [流式传输多种模式](#流式传输多种模式)

### [Python](#python-2)

您可以将列表作为`stream_mode`参数传递，一次流式传输多种模式。

流式输出将是元组`(mode, chunk)`，其中`mode`是流式传输模式的名称，`chunk`是该模式流式传输的数据。
    
    
    for mode, chunk in graph.stream(inputs, stream_mode=["updates", "custom"]):
        print(chunk)

### [JavaScript](#javascript-2)

您可以将数组作为`streamMode`参数传递，一次流式传输多种模式。

流式输出将是元组`[mode, chunk]`，其中`mode`是流式传输模式的名称，`chunk`是该模式流式传输的数据。
    
    
    for await (const [mode, chunk] of await graph.stream(inputs, {
      streamMode: ["updates", "custom"],
    })) {
      console.log(chunk);
    }

## [流式传输图状态](#流式传输图状态)

使用流式传输模式`updates`和`values`来流式传输图执行时的状态。

  * `updates`在图的每个步骤后流式传输状态的**更新** 。
  * `values`在图的每个步骤后流式传输状态的**完整值** 。



### [Python](#python-3)
    
    
    from typing import TypedDict
    from langgraph.graph import StateGraph, START, END
    
    
    class State(TypedDict):
      topic: str
      joke: str
    
    
    def refine_topic(state: State):
        return {"topic": state["topic"] + " and cats"}
    
    
    def generate_joke(state: State):
        return {"joke": f"This is a joke about {state['topic']}"}
    
    graph = (
      StateGraph(State)
      .add_node(refine_topic)
      .add_node(generate_joke)
      .add_edge(START, "refine_topic")
      .add_edge("refine_topic", "generate_joke")
      .add_edge("generate_joke", END)
      .compile()
    )

### [JavaScript](#javascript-3)
    
    
    import { StateGraph, START, END } from "@langchain/langgraph";
    import * as z from "zod";
    
    const State = z.object({
      topic: z.string(),
      joke: z.string(),
    });
    
    const graph = new StateGraph(State)
      .addNode("refineTopic", (state) => {
        return { topic: state.topic + " and cats" };
      })
      .addNode("generateJoke", (state) => {
        return { joke: `This is a joke about ${state.topic}` };
      })
      .addEdge(START, "refineTopic")
      .addEdge("refineTopic", "generateJoke")
      .addEdge("generateJoke", END)
      .compile();

#### [使用updates模式](#使用updates模式)

使用此模式仅流式传输每个步骤后节点返回的**状态更新** 。流式输出包括节点名称和更新内容。

### [Python](#python-4)
    
    
    for chunk in graph.stream(
        {"topic": "ice cream"},
        stream_mode="updates",
    ):
        print(chunk)

### [JavaScript](#javascript-4)
    
    
    for await (const chunk of await graph.stream(
      { topic: "ice cream" },
      { streamMode: "updates" }
    )) {
      console.log(chunk);
    }

#### [使用values模式](#使用values模式)

使用此模式流式传输每个步骤后的**完整图状态** 。

### [Python](#python-5)
    
    
    for chunk in graph.stream(
        {"topic": "ice cream"},
        stream_mode="values",
    ):
        print(chunk)

### [JavaScript](#javascript-5)
    
    
    for await (const chunk of await graph.stream(
      { topic: "ice cream" },
      { streamMode: "values" }
    )) {
      console.log(chunk);
    }

## [流式传输子图输出](#流式传输子图输出)

### [Python](#python-6)

要在流式输出中包含子图的输出，可以在父图的`.stream()`方法中设置`subgraphs=True`。这将流式传输父图和任何子图的输出。

输出将以元组`(namespace, data)`的形式流式传输，其中`namespace`是包含子图调用节点路径的元组，例如`("parent_node:<task_id>", "child_node:<task_id>")`。
    
    
    for chunk in graph.stream(
        {"foo": "foo"},
        # 设置subgraphs=True以流式传输子图的输出
        subgraphs=True,
        stream_mode="updates",
    ):
        print(chunk)

### [JavaScript](#javascript-6)

要在流式输出中包含子图的输出，可以在父图的`.stream()`方法中设置`subgraphs: true`。这将流式传输父图和任何子图的输出。

输出将以元组`[namespace, data]`的形式流式传输，其中`namespace`是包含子图调用节点路径的元组，例如`["parent_node:<task_id>", "child_node:<task_id>"]`。
    
    
    for await (const chunk of await graph.stream(
      { foo: "foo" },
      {
        // 设置subgraphs: true以流式传输子图的输出
        subgraphs: true,
        streamMode: "updates",
      }
    )) {
      console.log(chunk);
    }

扩展示例：从子图流式传输

### [Python](#python-7)
    
    
    from langgraph.graph import START, StateGraph
    from typing import TypedDict
    
    # 定义子图
    class SubgraphState(TypedDict):
        foo: str  # 注意这个键与父图状态共享
        bar: str
    
    def subgraph_node_1(state: SubgraphState):
        return {"bar": "bar"}
    
    def subgraph_node_2(state: SubgraphState):
        return {"foo": state["foo"] + state["bar"]}
    
    subgraph_builder = StateGraph(SubgraphState)
    subgraph_builder.add_node(subgraph_node_1)
    subgraph_builder.add_node(subgraph_node_2)
    subgraph_builder.add_edge(START, "subgraph_node_1")
    subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
    subgraph = subgraph_builder.compile()
    
    # 定义父图
    class ParentState(TypedDict):
        foo: str
    
    def node_1(state: ParentState):
        return {"foo": "hi! " + state["foo"]}
    
    builder = StateGraph(ParentState)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", subgraph)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    graph = builder.compile()
    
    for chunk in graph.stream(
        {"foo": "foo"},
        stream_mode="updates",
        # 设置subgraphs=True以流式传输子图的输出
        subgraphs=True,
    ):
        print(chunk)

### [JavaScript](#javascript-7)
    
    
    import { StateGraph, START } from "@langchain/langgraph";
    import * as z from "zod";
    
    // 定义子图
    const SubgraphState = z.object({
      foo: z.string(), // 注意这个键与父图状态共享
      bar: z.string(),
    });
    
    const subgraphBuilder = new StateGraph(SubgraphState)
      .addNode("subgraphNode1", (state) => {
        return { bar: "bar" };
      })
      .addNode("subgraphNode2", (state) => {
        return { foo: state.foo + state.bar };
      })
      .addEdge(START, "subgraphNode1")
      .addEdge("subgraphNode1", "subgraphNode2");
    const subgraph = subgraphBuilder.compile();
    
    // 定义父图
    const ParentState = z.object({
      foo: z.string(),
    });
    
    const builder = new StateGraph(ParentState)
      .addNode("node1", (state) => {
        return { foo: "hi! " + state.foo };
      })
      .addNode("node2", subgraph)
      .addEdge(START, "node1")
      .addEdge("node1", "node2");
    const graph = builder.compile();
    
    for await (const chunk of await graph.stream(
      { foo: "foo" },
      {
        streamMode: "updates",
        // 设置subgraphs: true以流式传输子图的输出
        subgraphs: true,
      }
    )) {
      console.log(chunk);
    }

### [Python输出](#python输出)
    
    
    ((), {'node_1': {'foo': 'hi! foo'}})
    (('node_2:dfddc4ba-c3c5-6887-5012-a243b5b377c2',), {'subgraph_node_1': {'bar': 'bar'}})
    (('node_2:dfddc4ba-c3c5-6887-5012-a243b5b377c2',), {'subgraph_node_2': {'foo': 'hi! foobar'}})
    ((), {'node_2': {'foo': 'hi! foobar'}})

### [JavaScript输出](#javascript输出)
    
    
    [[], {'node1': {'foo': 'hi! foo'}}]
    [['node2:dfddc4ba-c3c5-6887-5012-a243b5b377c2'], {'subgraphNode1': {'bar': 'bar'}}]
    [['node2:dfddc4ba-c3c5-6887-5012-a243b5b377c2'], {'subgraphNode2': {'foo': 'hi! foobar'}}]
    [[], {'node2': {'foo': 'hi! foobar'}}]

**注意** 我们不仅接收节点更新，还接收命名空间，这些命名空间告诉我们正在从哪个图（或子图）流式传输。

### [调试](#调试)

使用`debug`流式传输模式在图执行过程中流式传输尽可能多的信息。流式输出包括节点名称和完整状态。

### [Python](#python-8)
    
    
    for chunk in graph.stream(
        {"topic": "ice cream"},
        stream_mode="debug",
    ):
        print(chunk)

### [JavaScript](#javascript-8)
    
    
    for await (const chunk of await graph.stream(
      { topic: "ice cream" },
      { streamMode: "debug" }
    )) {
      console.log(chunk);
    }

## [LLM令牌](#llm令牌)

使用`messages`流式传输模式从图的任何部分（包括节点、工具、子图或任务）**逐令牌** 流式传输大型语言模型(LLM)的输出。

### [Python](#python-9)

`messages`模式的流式输出是元组`(message_chunk, metadata)`，其中：

  * `message_chunk`：来自LLM的令牌或消息段。
  * `metadata`：包含图节点和LLM调用详细信息的字典。



> 如果您的LLM没有可用的LangChain集成，可以使用`custom`模式代替流式传输其输出。详见[与任何LLM一起使用](#%E4%B8%8E%E4%BB%BB%E4%BD%95llm%E4%B8%80%E8%B5%B7%E4%BD%BF%E7%94%A8)部分。

> **Python < 3.11中异步需要手动配置**  
>  在使用Python < 3.11的异步代码时，必须显式地将`RunnableConfig`传递给`ainvoke()`以启用正确的流式传输。详见[Python < 3.11中的异步](#async)部分获取详细信息，或升级到Python 3.11+。
    
    
    from dataclasses import dataclass
    
    from langchain.chat_models import init_chat_model
    from langgraph.graph import StateGraph, START
    
    
    @dataclass
    class MyState:
        topic: str
        joke: str = ""
    
    
    model = init_chat_model(model="gpt-4o-mini")
    
    def call_model(state: MyState):
        """调用LLM生成关于某个主题的笑话"""
        # 注意，即使LLM是使用.invoke而不是.stream运行的，也会发出消息事件
        model_response = model.invoke(
            [
                {"role": "user", "content": f"Generate a joke about {state.topic}"}
            ]
        )
        return {"joke": model_response.content}
    
    graph = (
        StateGraph(MyState)
        .add_node(call_model)
        .add_edge(START, "call_model")
        .compile()
    )
    
    # "messages"流式传输模式返回元组迭代器(message_chunk, metadata)
    # 其中message_chunk是LLM流式传输的令牌，metadata是包含有关LLM调用的图节点信息和其他信息的字典
    for message_chunk, metadata in graph.stream(
        {"topic": "ice cream"},
        stream_mode="messages",
    ):
        if message_chunk.content:
            print(message_chunk.content, end="|", flush=True)

### [JavaScript](#javascript-9)

`messages`模式的流式输出是元组`[message_chunk, metadata]`，其中：

  * `message_chunk`：来自LLM的令牌或消息段。
  * `metadata`：包含图节点和LLM调用详细信息的字典。



> 如果您的LLM没有可用的LangChain集成，可以使用`custom`模式代替流式传输其输出。详见[与任何LLM一起使用](#%E4%B8%8E%E4%BB%BB%E4%BD%95llm%E4%B8%80%E8%B5%B7%E4%BD%BF%E7%94%A8)部分。
    
    
    import { ChatOpenAI } from "@langchain/openai";
    import { StateGraph, START } from "@langchain/langgraph";
    import * as z from "zod";
    
    const MyState = z.object({
      topic: z.string(),
      joke: z.string().default(""),
    });
    
    const model = new ChatOpenAI({ model: "gpt-4o-mini" });
    
    const callModel = async (state: z.infer<typeof MyState>) => {
      // 调用LLM生成关于某个主题的笑话
      // 注意，即使LLM是使用.invoke而不是.stream运行的，也会发出消息事件
      const modelResponse = await model.invoke([
        { role: "user", content: `Generate a joke about ${state.topic}` },
      ]);
      return { joke: modelResponse.content };
    };
    
    const graph = new StateGraph(MyState)
      .addNode("callModel", callModel)
      .addEdge(START, "callModel")
      .compile();
    
    // "messages"流式传输模式返回元组迭代器[messageChunk, metadata]
    // 其中messageChunk是LLM流式传输的令牌，metadata是包含有关LLM调用的图节点信息和其他信息的字典
    for await (const [messageChunk, metadata] of await graph.stream(
      { topic: "ice cream" },
      { streamMode: "messages" }
    )) {
      if (messageChunk.content) {
        console.log(messageChunk.content + "|");
      }
    }

#### [按LLM调用过滤](#按llm调用过滤)

您可以将`tags`与LLM调用关联，以按LLM调用过滤流式传输的令牌。

### [Python](#python-10)
    
    
    from langchain.chat_models import init_chat_model
    
    # model_1被标记为"joke"
    model_1 = init_chat_model(model="gpt-4o-mini", tags=['joke'])
    # model_2被标记为"poem"
    model_2 = init_chat_model(model="gpt-4o-mini", tags=['poem'])
    
    graph = ... # 定义使用这些LLM的图
    
    # stream_mode设置为"messages"以流式传输LLM令牌
    # metadata包含有关LLM调用的信息，包括tags
    async for msg, metadata in graph.astream(
        {"topic": "cats"},
        stream_mode="messages",
    ):
        # 通过metadata中的tags字段过滤流式传输的令牌，仅包含
        # 来自标记为"joke"的LLM调用的令牌
        if metadata["tags"] == ["joke"]:
            print(msg.content, end="|", flush=True)

### [JavaScript](#javascript-10)
    
    
    import { ChatOpenAI } from "@langchain/openai";
    
    // model1被标记为"joke"
    const model1 = new ChatOpenAI({
      model: "gpt-4o-mini",
      tags: ['joke']
    });
    // model2被标记为"poem"
    const model2 = new ChatOpenAI({
      model: "gpt-4o-mini",
      tags: ['poem']
    });
    
    const graph = // ... 定义使用这些LLM的图
    
    // streamMode设置为"messages"以流式传输LLM令牌
    // metadata包含有关LLM调用的信息，包括tags
    for await (const [msg, metadata] of await graph.stream(
      { topic: "cats" },
      { streamMode: "messages" }
    )) {
      // 通过metadata中的tags字段过滤流式传输的令牌，仅包含
      // 来自标记为"joke"的LLM调用的令牌
      if (metadata.tags?.includes("joke")) {
        console.log(msg.content + "|");
      }
    }

扩展示例：按标签过滤

### [Python](#python-11)
    
    
    from typing import TypedDict
    
    from langchain.chat_models import init_chat_model
    from langgraph.graph import START, StateGraph
    
    # joke_model被标记为"joke"
    joke_model = init_chat_model(model="gpt-4o-mini", tags=["joke"])
    # poem_model被标记为"poem"
    poem_model = init_chat_model(model="gpt-4o-mini", tags=["poem"])
    
    
    class State(TypedDict):
            topic: str
            joke: str
            poem: str
    
    
    async def call_model(state, config):
            topic = state["topic"]
            print("Writing joke...")
            # 注意：对于python < 3.11，需要显式传递config
            # 因为context var支持在那之前没有添加：https://docs.python.org/3/library/asyncio-task.html#creating-tasks
            # 显式传递config以确保context vars正确传播
            # 当在Python < 3.11中使用异步代码时，这是必需的。请参阅异步部分获取更多详细信息
            joke_response = await joke_model.ainvoke(
                  [{"role": "user", "content": f"Write a joke about {topic}"}],
                  config,
            )
            print("\n\nWriting poem...")
            poem_response = await poem_model.ainvoke(
                  [{"role": "user", "content": f"Write a short poem about {topic}"}],
                  config,
            )
            return {"joke": joke_response.content, "poem": poem_response.content}
    
    
    graph = (
            StateGraph(State)
            .add_node(call_model)
            .add_edge(START, "call_model")
            .compile()
    )
    
    # stream_mode设置为"messages"以流式传输LLM令牌
    # metadata包含有关LLM调用的信息，包括tags
    async for msg, metadata in graph.astream(
            {"topic": "cats"},
            stream_mode="messages",
    ):
        if metadata["tags"] == ["joke"]:
            print(msg.content, end="|", flush=True)

### [JavaScript](#javascript-11)
    
    
    import { ChatOpenAI } from "@langchain/openai";
    import { StateGraph, START } from "@langchain/langgraph";
    import * as z from "zod";
    
    // jokeModel被标记为"joke"
    const jokeModel = new ChatOpenAI({
      model: "gpt-4o-mini",
      tags: ["joke"]
    });
    // poemModel被标记为"poem"
    const poemModel = new ChatOpenAI({
      model: "gpt-4o-mini",
      tags: ["poem"]
    });
    
    const State = z.object({
      topic: z.string(),
      joke: z.string(),
      poem: z.string(),
    });
    
    const graph = new StateGraph(State)
      .addNode("callModel", async (state) => {
        const topic = state.topic;
        console.log("Writing joke...");
    
        const jokeResponse = await jokeModel.invoke([
          { role: "user", content: `Write a joke about ${topic}` }
        ]);
    
        console.log("\n\nWriting poem...");
        const poemResponse = await poemModel.invoke([
          { role: "user", content: `Write a short poem about ${topic}` }
        ]);
    
        return {
          joke: jokeResponse.content,
          poem: poemResponse.content
        };
      })
      .addEdge(START, "callModel")
      .compile();
    
    // streamMode设置为"messages"以流式传输LLM令牌
    // metadata包含有关LLM调用的信息，包括tags
    for await (const [msg, metadata] of await graph.stream(
      { topic: "cats" },
      { streamMode: "messages" }
    )) {
      // 通过metadata中的tags字段过滤流式传输的令牌，仅包含
      // 来自标记为"joke"的LLM调用的令牌
      if (metadata.tags?.includes("joke")) {
        console.log(msg.content + "|");
      }
    }

#### [按节点过滤](#按节点过滤)

要仅从特定节点流式传输令牌，请使用`stream_mode="messages"`并按流式传输的metadata中的`langgraph_node`字段过滤输出：

### [Python](#python-12)
    
    
    # "messages"流式传输模式返回(message_chunk, metadata)元组
    # 其中message_chunk是LLM流式传输的令牌，metadata是包含有关LLM调用的图节点信息和其他信息的字典
    for msg, metadata in graph.stream(
        inputs,
        stream_mode="messages",
    ):
        # 通过metadata中的langgraph_node字段过滤流式传输的令牌
        # 仅包含来自指定节点的令牌
        if msg.content and metadata["langgraph_node"] == "some_node_name":
            ...

### [JavaScript](#javascript-12)
    
    
    // "messages"流式传输模式返回[messageChunk, metadata]元组
    // 其中messageChunk是LLM流式传输的令牌，metadata是包含有关LLM调用的图节点信息和其他信息的字典
    for await (const [msg, metadata] of await graph.stream(
      inputs,
      { streamMode: "messages" }
    )) {
      // 通过metadata中的langgraph_node字段过滤流式传输的令牌
      // 仅包含来自指定节点的令牌
      if (msg.content && metadata.langgraph_node === "some_node_name") {
        // ...
      }
    }

扩展示例：从特定节点流式传输LLM令牌

### [Python](#python-13)
    
    
    from typing import TypedDict
    from langgraph.graph import START, StateGraph
    from langchain_openai import ChatOpenAI
    
    model = ChatOpenAI(model="gpt-4o-mini")
    
    
    class State(TypedDict):
            topic: str
            joke: str
            poem: str
    
    
    def write_joke(state: State):
            topic = state["topic"]
            joke_response = model.invoke(
                  [{"role": "user", "content": f"Write a joke about {topic}"}]
            )
            return {"joke": joke_response.content}
    
    
    def write_poem(state: State):
            topic = state["topic"]
            poem_response = model.invoke(
                  [{"role": "user", "content": f"Write a short poem about {topic}"}]
            )
            return {"poem": poem_response.content}
    
    
    graph = (
            StateGraph(State)
            .add_node(write_joke)
            .add_node(write_poem)
            # 同时编写笑话和诗歌
            .add_edge(START, "write_joke")
            .add_edge(START, "write_poem")
            .compile()
    )
    
    # "messages"流式传输模式返回(message_chunk, metadata)元组
    # 其中message_chunk是LLM流式传输的令牌，metadata是包含有关LLM调用的图节点信息和其他信息的字典
    for msg, metadata in graph.stream(
        {"topic": "cats"},
        stream_mode="messages",
    ):
        # 通过metadata中的langgraph_node字段过滤流式传输的令牌
        # 仅包含来自write_poem节点的令牌
        if msg.content and metadata["langgraph_node"] == "write_poem":
            print(msg.content, end="|", flush=True)

### [JavaScript](#javascript-13)
    
    
    import { ChatOpenAI } from "@langchain/openai";
    import { StateGraph, START } from "@langchain/langgraph";
    import * as z from "zod";
    
    const model = new ChatOpenAI({ model: "gpt-4o-mini" });
    
    const State = z.object({
      topic: z.string(),
      joke: z.string(),
      poem: z.string(),
    });
    
    const graph = new StateGraph(State)
      .addNode("writeJoke", async (state) => {
        const topic = state.topic;
        const jokeResponse = await model.invoke([
          { role: "user", content: `Write a joke about ${topic}` }
        ]);
        return { joke: jokeResponse.content };
      })
      .addNode("writePoem", async (state) => {
        const topic = state.topic;
        const poemResponse = await model.invoke([
          { role: "user", content: `Write a short poem about ${topic}` }
        ]);
        return { poem: poemResponse.content };
      })
      // 同时编写笑话和诗歌
      .addEdge(START, "writeJoke")
      .addEdge(START, "writePoem")
      .compile();
    
    // "messages"流式传输模式返回[messageChunk, metadata]元组
    // 其中messageChunk是LLM流式传输的令牌，metadata是包含有关LLM调用的图节点信息和其他信息的字典
    for await (const [msg, metadata] of await graph.stream(
      { topic: "cats" },
      { streamMode: "messages" }
    )) {
      // 通过metadata中的langgraph_node字段过滤流式传输的令牌
      // 仅包含来自writePoem节点的令牌
      if (msg.content && metadata.langgraph_node === "writePoem") {
        console.log(msg.content + "|");
      }
    }

## [流式传输自定义数据](#流式传输自定义数据)

### [Python](#python-14)

要从LangGraph节点或工具内部发送**自定义用户定义数据** ，请按照以下步骤操作：

  1. 使用`get_stream_writer`访问流写入器并发出自定义数据。
  2. 在调用`.stream()`或`.astream()`时设置`stream_mode="custom"`以在流中获取自定义数据。您可以组合多种模式（例如，`["updates", "custom"]`），但至少有一种必须是`"custom"`。



> **Python < 3.11中异步无法使用`get_stream_writer`**  
>  在Python < 3.11上运行的异步代码中，`get_stream_writer`将无法工作。  
>  相反，请在您的节点或工具中添加`writer`参数并手动传递它。  
>  详见[Python < 3.11中的异步](#async)部分获取使用示例。

#### [在节点中流式传输自定义数据](#在节点中流式传输自定义数据)
    
    
    from typing import TypedDict
    from langgraph.config import get_stream_writer
    from langgraph.graph import StateGraph, START
    
    class State(TypedDict):
        query: str
        answer: str
    
    def node(state: State):
        # 获取流写入器以发送自定义数据
        writer = get_stream_writer()
        # 发出自定义键值对（例如，进度更新）
        writer({"custom_key": "Generating custom data inside node"})
        return {"answer": "some data"}
    
    graph = (
        StateGraph(State)
        .add_node(node)
        .add_edge(START, "node")
        .compile()
    )
    
    inputs = {"query": "example"}
    
    # 设置stream_mode="custom"以在流中接收自定义数据
    for chunk in graph.stream(inputs, stream_mode="custom"):
        print(chunk)

#### [在工具中流式传输自定义数据](#在工具中流式传输自定义数据)
    
    
    from langchain.tools import tool
    from langgraph.config import get_stream_writer
    
    @tool
    def query_database(query: str) -> str:
        """查询数据库。"""
        # 访问流写入器以发送自定义数据
        writer = get_stream_writer()
        # 发出自定义键值对（例如，进度更新）
        writer({"data": "Retrieved 0/100 records", "type": "progress"})
        # 执行查询
        # 发出另一个自定义键值对
        writer({"data": "Retrieved 100/100 records", "type": "progress"})
        return "some-answer"
    
    
    graph = ... # 定义使用此工具的图
    
    # 设置stream_mode="custom"以在流中接收自定义数据
    for chunk in graph.stream(inputs, stream_mode="custom"):
        print(chunk)

### [JavaScript](#javascript-14)

要从LangGraph节点或工具内部发送**自定义用户定义数据** ，请按照以下步骤操作：

  1. 使用`LangGraphRunnableConfig`中的`writer`参数发出自定义数据。
  2. 在调用`.stream()`时设置`streamMode: "custom"`以在流中获取自定义数据。您可以组合多种模式（例如，`["updates", "custom"]`），但至少有一种必须是`"custom"`。



#### [在节点中流式传输自定义数据](#在节点中流式传输自定义数据-1)
    
    
    import { StateGraph, START, LangGraphRunnableConfig } from "@langchain/langgraph";
    import * as z from "zod";
    
    const State = z.object({
      query: z.string(),
      answer: z.string(),
    });
    
    const graph = new StateGraph(State)
      .addNode("node", async (state, config) => {
        // 使用writer发出自定义键值对（例如，进度更新）
        config.writer({ custom_key: "Generating custom data inside node" });
        return { answer: "some data" };
      })
      .addEdge(START, "node")
      .compile();
    
    const inputs = { query: "example" };
    
    // 设置streamMode: "custom"以在流中接收自定义数据
    for await (const chunk of await graph.stream(inputs, { streamMode: "custom" })) {
      console.log(chunk);
    }

#### [在工具中流式传输自定义数据](#在工具中流式传输自定义数据-1)
    
    
    import { tool } from "@langchain/core/tools";
    import { LangGraphRunnableConfig } from "@langchain/langgraph";
    import * as z from "zod";
    
    const queryDatabase = tool(
      async (input, config: LangGraphRunnableConfig) => {
        // 使用writer发出自定义键值对（例如，进度更新）
        config.writer({ data: "Retrieved 0/100 records", type: "progress" });
        // 执行查询
        // 发出另一个自定义键值对
        config.writer({ data: "Retrieved 100/100 records", type: "progress" });
        return "some-answer";
      },
      {
        name: "query_database",
        description: "Query the database.",
        schema: z.object({
          query: z.string().describe("The query to execute."),
        }),
      }
    );
    
    const graph = // ... 定义使用此工具的图
    
    // 设置streamMode: "custom"以在流中接收自定义数据
    for await (const chunk of await graph.stream(inputs, { streamMode: "custom" })) {
      console.log(chunk);
    }

## [与任何LLM一起使用](#与任何llm一起使用)

### [Python](#python-15)

您可以使用`stream_mode="custom"`从**任何LLM API** 流式传输数据——即使该API**不** 实现LangChain聊天模型接口。

这使您能够集成原始LLM客户端或提供自己流式传输接口的外部服务，使LangGraph对于自定义设置非常灵活。
    
    
    from langgraph.config import get_stream_writer
    
    def call_arbitrary_model(state):
        """调用任意模型并流式传输输出的示例节点"""
        # 获取流写入器以发送自定义数据
        writer = get_stream_writer()
        # 假设您有一个生成块的流式客户端
        # 使用自定义流式客户端生成LLM令牌
        for chunk in your_custom_streaming_client(state["topic"]):
            # 使用writer将自定义数据发送到流
            writer({"custom_llm_chunk": chunk})
        return {"result": "completed"}
    
    graph = (
        StateGraph(State)
        .add_node(call_arbitrary_model)
        # 根据需要添加其他节点和边
        .compile()
    )
    # 设置stream_mode="custom"以在流中接收自定义数据
    for chunk in graph.stream(
        {"topic": "cats"},
        stream_mode="custom",
    ):
        # chunk将包含从llm流式传输的自定义数据
        print(chunk)

### [JavaScript](#javascript-15)

您可以使用`streamMode: "custom"`从**任何LLM API** 流式传输数据——即使该API**不** 实现LangChain聊天模型接口。

这使您能够集成原始LLM客户端或提供自己流式传输接口的外部服务，使LangGraph对于自定义设置非常灵活。
    
    
    import { LangGraphRunnableConfig } from "@langchain/langgraph";
    
    const callArbitraryModel = async (
      state: any,
      config: LangGraphRunnableConfig
    ) => {
      // 调用任意模型并流式传输输出的示例节点
      // 假设您有一个生成块的流式客户端
      // 使用自定义流式客户端生成LLM令牌
      for await (const chunk of yourCustomStreamingClient(state.topic)) {
        // 使用writer将自定义数据发送到流
        config.writer({ custom_llm_chunk: chunk });
      }
      return { result: "completed" };
    };
    
    const graph = new StateGraph(State)
      .addNode("callArbitraryModel", callArbitraryModel)
      // 根据需要添加其他节点和边
      .compile();
    
    // 设置streamMode: "custom"以在流中接收自定义数据
    for await (const chunk of await graph.stream(
      { topic: "cats" },
      { streamMode: "custom" }
    )) {
      // chunk将包含从llm流式传输的自定义数据
      console.log(chunk);
    }

扩展示例：流式传输任意聊天模型

### [Python](#python-16)
    
    
    import operator
    import json
    
    from typing import TypedDict
    from typing_extensions import Annotated
    from langgraph.graph import StateGraph, START
    
    from openai import AsyncOpenAI
    
    openai_client = AsyncOpenAI()
    model_name = "gpt-4o-mini"
    
    
    async def stream_tokens(model_name: str, messages: list[dict]):
        response = await openai_client.chat.completions.create(
            messages=messages, model=model_name, stream=True
        )
        role = None
        async for chunk in response:
            delta = chunk.choices[0].delta
    
            if delta.role is not None:
                role = delta.role
    
            if delta.content:
                yield {"role": role, "content": delta.content}
    
    
    # 这是我们的工具
    async def get_items(place: str) -> str:
        """使用此工具列出您询问的地方可能找到的物品。"""
        writer = get_stream_writer()
        response = ""
        async for msg_chunk in stream_tokens(
            model_name,
            [
                {
                    "role": "user",
                    "content": (
                        "Can you tell me what kind of items "
                        f"i might find in the following place: '{place}'. "
                        "List at least 3 such items separating them by a comma. "
                        "And include a brief description of each item."
                    ),
                }
            ],
        ):
            response += msg_chunk["content"]
            writer(msg_chunk)
    
        return response
    
    
    class State(TypedDict):
        messages: Annotated[list[dict], operator.add]
    
    
    # 这是工具调用图节点
    async def call_tool(state: State):
        ai_message = state["messages"][-1]
        tool_call = ai_message["tool_calls"][-1]
    
        function_name = tool_call["function"]["name"]
        if function_name != "get_items":
            raise ValueError(f"Tool {function_name} not supported")
    
        function_arguments = tool_call["function"]["arguments"]
        arguments = json.loads(function_arguments)
    
        function_response = await get_items(**arguments)
        tool_message = {
            "tool_call_id": tool_call["id"],
            "role": "tool",
            "name": function_name,
            "content": function_response,
        }
        return {"messages": [tool_message]}
    
    
    graph = (
        StateGraph(State)
        .add_node(call_tool)
        .add_edge(START, "call_tool")
        .compile()
    )

让我们使用包含工具调用的`AIMessage`调用图：
    
    
    inputs = {
        "messages": [
            {
                "content": None,
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "1",
                        "function": {
                            "arguments": '{"place":"bedroom"}',
                            "name": "get_items",
                        },
                        "type": "function",
                    }
                ],
            }
        ]
    }
    
    async for chunk in graph.astream(
        inputs,
        stream_mode="custom",
    ):
        print(chunk["content"], end="|", flush=True)

### [JavaScript](#javascript-16)
    
    
    import { StateGraph, START, MessagesZodMeta, LangGraphRunnableConfig } from "@langchain/langgraph";
    import { BaseMessage } from "@langchain/core/messages";
    import { registry } from "@langchain/langgraph/zod";
    import * as z from "zod";
    import OpenAI from "openai";
    
    const openaiClient = new OpenAI();
    const modelName = "gpt-4o-mini";
    
    async function* streamTokens(modelName: string, messages: any[]) {
      const response = await openaiClient.chat.completions.create({
        messages,
        model: modelName,
        stream: true,
      });
    
      let role: string | null = null;
      for await (const chunk of response) {
        const delta = chunk.choices[0]?.delta;
    
        if (delta?.role) {
          role = delta.role;
        }
    
        if (delta?.content) {
          yield { role, content: delta.content };
        }
      }
    }
    
    // 这是我们的工具
    const getItems = tool(
      async (input, config: LangGraphRunnableConfig) => {
        let response = "";
        for await (const msgChunk of streamTokens(
          modelName,
          [
            {
              role: "user",
              content: `Can you tell me what kind of items i might find in the following place: '${input.place}'. List at least 3 such items separating them by a comma. And include a brief description of each item.`,
            },
          ]
        )) {
          response += msgChunk.content;
          config.writer?.(msgChunk);
        }
        return response;
      },
      {
        name: "get_items",
        description: "Use this tool to list items one might find in a place you're asked about.",
        schema: z.object({
          place: z.string().describe("The place to look up items for."),
        }),
      }
    );
    
    const State = z.object({
      messages: z
        .array(z.custom<BaseMessage>())
        .register(registry, MessagesZodMeta),
    });
    
    const graph = new StateGraph(State)
      // 这是工具调用图节点
      .addNode("callTool", async (state) => {
        const aiMessage = state.messages.at(-1);
        const toolCall = aiMessage.tool_calls?.at(-1);
    
        const functionName = toolCall?.function?.name;
        if (functionName !== "get_items") {
          throw new Error(`Tool ${functionName} not supported`);
        }
    
        const functionArguments = toolCall?.function?.arguments;
        const args = JSON.parse(functionArguments);
    
        const functionResponse = await getItems.invoke(args);
        const toolMessage = {
          tool_call_id: toolCall.id,
          role: "tool",
          name: functionName,
          content: functionResponse,
        };
        return { messages: [toolMessage] };
      })
      .addEdge(START, "callTool")
      .compile();

让我们使用包含工具调用的`AIMessage`调用图：
    
    
    const inputs = {
      messages: [
        {
          content: null,
          role: "assistant",
          tool_calls: [
            {
              id: "1",
              function: {
                arguments: '{"place":"bedroom"}',
                name: "get_items",
              },
              type: "function",
            }
          ],
        }
      ]
    };
    
    for await (const chunk of await graph.stream(
      inputs,
      { streamMode: "custom" }
    )) {
      console.log(chunk.content + "|");
    }

## [为特定聊天模型禁用流式传输](#为特定聊天模型禁用流式传输)

如果您的应用程序混合使用支持流式传输和不支持流式传输的模型，则可能需要明确为不支持流式传输的模型禁用流式传输。

### [Python](#python-17)

在初始化模型时设置`disable_streaming=True`。

#### [使用init_chat_model](#使用init-chat-model)
    
    
    from langchain.chat_models import init_chat_model
    
    model = init_chat_model(
        "claude-sonnet-4-5-20250929",
        # 设置disable_streaming=True以禁用聊天模型的流式传输
        disable_streaming=True
    )

#### [使用聊天模型接口](#使用聊天模型接口)
    
    
    from langchain_openai import ChatOpenAI
    
    # 设置disable_streaming=True以禁用聊天模型的流式传输
    model = ChatOpenAI(model="o1-preview", disable_streaming=True)

### [JavaScript](#javascript-17)

在初始化模型时设置`streaming: false`。
    
    
    import { ChatOpenAI } from "@langchain/openai";
    
    const model = new ChatOpenAI({
      model: "o1-preview",
      // 设置streaming: false以禁用聊天模型的流式传输
      streaming: false,
    });

### [Python < 3.11中的异步](#python-3-11中的异步)

在Python版本< 3.11中，[asyncio任务](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task)不支持`context`参数。  
这限制了LangGraph自动传播上下文的能力，并在两个关键方面影响LangGraph的流式传输机制：

  1. 您**必须** 显式地将[`RunnableConfig`](https://python.langchain.com/docs/concepts/runnables/#runnableconfig)传递给异步LLM调用（例如，`ainvoke()`），因为回调不会自动传播。
  2. 您**不能** 在异步节点或工具中使用`get_stream_writer`——您必须直接传递`writer`参数。

扩展示例：带有手动配置的异步LLM调用 ```python from typing import TypedDict from langgraph.graph import START, StateGraph from langchain.chat_models import init_chat_model 

model = init_chat_model(model="gpt-4o-mini")

class State(TypedDict):  
topic: str  
joke: str

# [在异步节点函数中接受config作为参数](#在异步节点函数中接受config作为参数)

async def call_model(state, config):  
topic = state["topic"]  
print("Generating joke...")  
# 将config传递给model.ainvoke()以确保正确的上下文传播  
joke_response = await model.ainvoke(  
[{"role": "user", "content": f"Write a joke about {topic}"}],  
config,  
)  
return

graph = (  
StateGraph(State)  
.add_node(call_model)  
.add_edge(START, "call_model")  
.compile()  
)

# [设置stream_mode="messages"以流式传输LLM令牌](#设置stream-mode-messages-以流式传输llm令牌)

async for chunk, metadata in graph.astream(  
{"topic": "ice cream"},  
stream_mode="messages",  
):  
if chunk.content:  
print(chunk.content, end="|", flush=True)
    
    
    </details>
    
    <details>
    <summary>扩展示例：带有流写入器的异步自定义流式传输</summary>
    ```python
    from typing import TypedDict
    from langgraph.types import StreamWriter
    
    class State(TypedDict):
            topic: str
            joke: str
    
    # 在异步节点或工具的函数签名中添加writer作为参数
    # LangGraph会自动将流写入器传递给函数
    async def generate_joke(state: State, writer: StreamWriter):
            writer({"custom_key": "Streaming custom data while generating a joke"})
            return {"joke": f"This is a joke about {state['topic']}"}
    
    graph = (
            StateGraph(State)
            .add_node(generate_joke)
            .add_edge(START, "generate_joke")
            .compile()
    )
    
    # 设置stream_mode="custom"以在流中接收自定义数据
    async for chunk in graph.astream(
            {"topic": "ice cream"},
            stream_mode="custom",
    ):
            print(chunk)

最近更新2025/11/1 22:56

[上一页持久执行](/v1/python/langgraph/durable-execution.html)[下一页中断](/v1/python/langgraph/interrupts.html)
