"""
RAG 知识库 CLI 问答入口
"""
import os
import sys

# 自动加载项目根目录的 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass  # python-dotenv 未安装时静默跳过，依赖手动设置的环境变量

from qa_chain import build_qa_chain


def main() -> None:
    # ── 1. 检查 API Key ──
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("错误：未设置 DEEPSEEK_API_KEY")
        print("")
        print("解决方案（任选其一）：")
        print("  1. 创建 .env 文件：echo DEEPSEEK_API_KEY=你的密钥 > .env")
        print("  2. 手动设置：set DEEPSEEK_API_KEY=你的密钥")
        sys.exit(1)

    # ── 2. 构建 Chain ──
    print("正在加载 RAG 知识库...")
    try:
        chain = build_qa_chain()
    except Exception as e:
        print(f"加载知识库失败：{type(e).__name__}: {e}")
        sys.exit(1)

    # ── 3. CLI 交互循环 ──
    print("\n" + "=" * 50)
    print("  Agent 开发知识库")
    print("  输入问题开始查询，输入 quit 退出")
    print("=" * 50 + "\n")

    while True:
        try:
            question = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not question:
            print("请输入有效问题\n")
            continue

        if question.lower() in ("quit", "q"):
            print("再见！")
            break

        try:
            answer = chain.invoke({"question": question})
            print(f"\n{answer}\n")
            print("-" * 50 + "\n")
        except Exception as e:
            print(f"\n调用失败 [{type(e).__name__}]: {e}\n")


if __name__ == "__main__":
    main()
