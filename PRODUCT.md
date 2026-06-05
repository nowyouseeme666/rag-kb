# Product

## Register

product

## Users

个人开发者，在学习和使用 Agent 开发框架（LangChain、LangGraph、DeepSeek 等）时，需要通过自然语言快速查询技术文档中的关键信息。单人使用，偶尔可能本地共享。

## Product Purpose

一个基于 RAG 的 Agent 开发知识库问答系统。将 LangChain/LangGraph/DeepSeek 等技术文档向量化后存入 ChromaDB，用户通过自然语言提问，系统检索相关文档片段并调用 DeepSeek LLM 生成带来源引用的回答。解决开发者面对分散的英文文档时查找效率低的问题。

## Brand Personality

- **干净高效**：像一把好用的工具，不喧宾夺主
- **专业精确**：回答有据可查，不编造不模糊
- **安静克制**：界面退后，内容前置

## Anti-references

- 不要 SaaS 营销风格的渐变、动画、英雄区块
- 不要 Perplexity 式的多卡片信息密度
- 不要花哨的 loading 动画或音效
- 避免 cream/sand 暖色背景——工具应像编辑器一样冷静

## Design Principles

1. **内容即界面**：Markdown 渲染是核心体验，排版和代码块必须清晰
2. **回答可溯源**：每个引用都标注来源文件，用户可追溯验证
3. **零学习成本**：打开就能用，输入框居中，一个按钮完成一切
4. **安静的工具**：界面退后，不做任何分散注意力的设计

## Accessibility & Inclusion

- 标准对比度 (WCAG AA)，正文 ≥4.5:1
- 支持键盘操作（Enter 提交）
- `prefers-reduced-motion` 尊重系统设置
