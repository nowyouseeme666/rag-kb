# LangGraph StateGraph 详解

## 什么是 StateGraph

StateGraph 是 LangGraph 中用于构建有状态多步 Agent 的核心组件。它定义了一个图结构，其中每个节点代表一个处理步骤，边定义了步骤之间的流转逻辑。

## StateGraph 的基本结构

StateGraph 包含以下要素：
1. **State（状态）**：在整个图执行过程中共享的数据结构，通常是一个 TypedDict
2. **Nodes（节点）**：执行具体逻辑的函数，每个节点接收 State 并返回 State 的部分更新
3. **Edges（边）**：定义了节点之间的流转路径

## 条件边（Conditional Edges）

条件边允许根据当前状态动态决定下一步执行哪个节点。这是构建复杂 Agent 逻辑的关键机制。

条件边的定义方式：
```python
graph.add_conditional_edges("node_name", routing_function, {
    "option_a": "node_a",
    "option_b": "node_b",
})
```

routing_function 接收当前 state 作为参数，返回一个字符串表示下一步的目标节点名称。

## 检查点（Checkpoint）

LangGraph 的检查点机制允许保存和恢复图执行的状态。主要用途包括：
- 实现人机交互（Human-in-the-loop）
- 错误恢复和重试
- 长时间运行的 Agent 任务持久化

## StateGraph 与普通 Chain 的区别

Chain 是线性的、固定流程的，而 StateGraph 支持：
- 循环和分支
- 动态路由
- 状态持久化
- 多步推理和反思
