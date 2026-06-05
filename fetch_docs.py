"""
fetch_docs.py — 从官方文档站抓取 HTML 页面并转为 Markdown 存入 data/

用法:
    python fetch_docs.py           # 抓取清单中所有文档
    python fetch_docs.py --dry-run # 只打印 URL，不实际下载

依赖（推荐安装以获得更好的转换质量）:
    pip install html2text

源说明:
    - Web 页面 → 抓取 HTML → html2text（或内置正则兜底）→ .md
    - 每个条目可配置多个候选 URL，脚本依次尝试直到成功

如需增删文档，修改下方的 SOURCES 清单即可。
每个条目: (文件名, [候选URL列表], 备注)
"""

import os
import re
import sys
import time
import html as html_mod
import urllib.request
import urllib.error
from pathlib import Path

import config

# ── 文档抓取清单 ──────────────────────────────────────────
# 格式: (保存文件名, [候选URL, ...], 备注)
# 候选 URL 按优先级排列，脚本依次尝试直到成功
# ──────────────────────────────────────────────────────────

SOURCES = [
    # ═══════════════════════════════════════════════════════
    # DeepSeek API 文档（中文）
    # ═══════════════════════════════════════════════════════

    (
        "deepseek-reasoner.md",
        [
            "https://api-docs.deepseek.com/zh-cn/guides/reasoning_model",
            "https://api-docs.deepseek.com/guides/reasoning_model",
        ],
        "DeepSeek R1 推理模型"
    ),
    (
        "deepseek-rate-limit.md",
        [
            "https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit",
            "https://api-docs.deepseek.com/quick_start/rate_limit",
        ],
        "DeepSeek API 频率限制"
    ),
    (
        "deepseek-error-codes.md",
        [
            "https://api-docs.deepseek.com/zh-cn/quick_start/error_codes",
            "https://api-docs.deepseek.com/quick_start/error_codes",
        ],
        "DeepSeek API 错误码"
    ),
    (
        "deepseek-pricing.md",
        [
            "https://api-docs.deepseek.com/zh-cn/quick_start/pricing",
            "https://api-docs.deepseek.com/quick_start/pricing",
        ],
        "DeepSeek API 定价"
    ),
    (
        "deepseek-token-usage.md",
        [
            "https://api-docs.deepseek.com/zh-cn/quick_start/token_usage",
            "https://api-docs.deepseek.com/quick_start/token_usage",
        ],
        "DeepSeek Token 用量说明"
    ),
    (
        "deepseek-model-list.md",
        [
            "https://api-docs.deepseek.com/zh-cn/quick_start/models",
            "https://api-docs.deepseek.com/quick_start/models",
        ],
        "DeepSeek 模型列表"
    ),

    # ═══════════════════════════════════════════════════════
    # LangChain 中文文档 (langchain-doc.cn)
    # ═══════════════════════════════════════════════════════

    (
        "langchain-tool-calling.md",
        [
            "https://langchain-doc.cn/v1/python/langchain/tool-calling.html",
            "https://langchain-doc.cn/how_to/tool-calling.html",
            "https://langchain-doc.cn/how_to/tool_calling.html",
        ],
        "LangChain Tool Calling"
    ),
    (
        "langchain-callbacks.md",
        [
            "https://langchain-doc.cn/v1/python/langchain/callbacks.html",
            "https://langchain-doc.cn/how_to/callbacks.html",
        ],
        "LangChain Callbacks"
    ),
    (
        "langchain-custom-tools.md",
        [
            "https://langchain-doc.cn/v1/python/langchain/custom-tools.html",
            "https://langchain-doc.cn/how_to/custom-tools.html",
        ],
        "LangChain 自定义工具"
    ),

    # ═══════════════════════════════════════════════════════
    # LangGraph 中文文档 (langchain-doc.cn)
    # ═══════════════════════════════════════════════════════

    (
        "langgraph-agent-concepts.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/agentic-concepts.html",
            "https://langchain-doc.cn/v1/python/langgraph/agent-concepts.html",
        ],
        "LangGraph Agent 核心概念"
    ),
    (
        "langgraph-react-agent.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/create-react-agent.html",
            "https://langchain-doc.cn/v1/python/langgraph/react-agent.html",
        ],
        "LangGraph ReAct Agent"
    ),
    (
        "langgraph-supervisor-agent.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/supervisor.html",
            "https://langchain-doc.cn/v1/python/langgraph/multi-agent.html",
        ],
        "LangGraph Supervisor / 多 Agent"
    ),
    (
        "langgraph-subgraph.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/subgraph.html",
            "https://langchain-doc.cn/v1/python/langgraph/subgraphs.html",
        ],
        "LangGraph 子图"
    ),
    (
        "langgraph-human-in-the-loop.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/human-in-the-loop.html",
            "https://langchain-doc.cn/v1/python/langgraph/human_in_the_loop.html",
        ],
        "LangGraph Human-in-the-Loop"
    ),
    (
        "langgraph-memory.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/add-memory.html",
            "https://langchain-doc.cn/v1/python/langgraph/persistence.html",
            "https://langchain-doc.cn/v1/python/langgraph/memory.html",
        ],
        "LangGraph 长期记忆 / 持久化"
    ),
    (
        "langgraph-checkpoint.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/checkpointer.html",
            "https://langchain-doc.cn/v1/python/langgraph/checkpoints.html",
            "https://langchain-doc.cn/v1/python/langgraph/persistence.html",
        ],
        "LangGraph Checkpoint 持久化"
    ),

    # ═══════════════════════════════════════════════════════
    # 通用 Agent 开发（中文）
    # ═══════════════════════════════════════════════════════

    (
        "langchain-agents.md",
        [
            "https://langchain-doc.cn/v1/python/langchain/agents.html",
            "https://langchain-doc.cn/tutorials/agents.html",
        ],
        "LangChain Agents 概述"
    ),
    (
        "langgraph-streaming.md",
        [
            "https://langchain-doc.cn/v1/python/langgraph/streaming.html",
            "https://langchain-doc.cn/v1/python/langgraph/stream-events.html",
        ],
        "LangGraph Streaming"
    ),
]

# ── HTTP 配置 ──
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 1.5         # 请求间隔（秒）
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

# 正文提取标记
CONTENT_START_MARKERS = [
    r"<article",
    r'<main',
    r'class="content"',
    r'class="markdown"',
    r'class="doc-content"',
    r'class="theme-default-content"',
    r'class="post-content"',
]
CONTENT_END_MARKERS = [
    r"</article>",
    r"</main>",
]


# ── 工具函数 ─────────────────────────────────────────────

def _basic_html_to_md(html_text: str) -> str:
    """HTML → Markdown。优先用 html2text，没有则用正则兜底。"""
    try:
        import html2text
        converter = html2text.HTML2Text()
        converter.body_width = 0
        converter.ignore_links = False
        converter.ignore_images = False
        converter.skip_internal_links = False
        return converter.handle(html_text)
    except ImportError:
        pass

    text = html_text

    for tag in ("script", "style", "nav", "footer", "header", "aside"):
        text = re.sub(rf"<{tag}\b[^>]*>.*?</{tag}>", "", text,
                       flags=re.DOTALL | re.IGNORECASE)

    for tag in ("p", "div", "section", "article", "li", "tr",
                "h1", "h2", "h3", "h4", "h5", "h6"):
        text = re.sub(rf"</?{tag}\b[^>]*>", "\n", text, flags=re.IGNORECASE)

    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    text = re.sub(
        r'<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        r'[\2](\1)', text, flags=re.DOTALL | re.IGNORECASE,
    )
    text = re.sub(
        r'<img\b[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*/?>',
        r'![](\1)', text, flags=re.IGNORECASE,
    )

    for i in range(6, 0, -1):
        text = re.sub(
            rf"<h{i}\b[^>]*>(.*?)</h{i}>",
            # Use default arg to capture `i` in closure
            lambda m, n=i: f'{"#" * n} {m.group(1).strip()}\n',
            text, flags=re.DOTALL | re.IGNORECASE,
        )

    text = re.sub(r"</?(?:strong|b)\b[^>]*>", "**", text, flags=re.IGNORECASE)
    text = re.sub(r"</?(?:em|i)\b[^>]*>", "*", text, flags=re.IGNORECASE)
    text = re.sub(r"</?code\b[^>]*>", "`", text, flags=re.IGNORECASE)
    text = re.sub(r"<pre\b[^>]*>(.*?)</pre>", r"\n```\n\1\n```\n",
                   text, flags=re.DOTALL | re.IGNORECASE)

    for tag in ("ul", "ol", "blockquote", "table", "thead", "tbody"):
        text = re.sub(rf"</?{tag}\b[^>]*>", "\n", text, flags=re.IGNORECASE)

    text = re.sub(r"<hr\b[^>]*/?>", "\n---\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_mod.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_main_content(html_text: str) -> str:
    """尝试从 HTML 中提取正文区域"""
    for start_pat in CONTENT_START_MARKERS:
        m = re.search(start_pat, html_text, re.IGNORECASE)
        if m:
            html_text = html_text[m.start():]
            break
    for end_pat in CONTENT_END_MARKERS:
        m = re.search(end_pat, html_text, re.IGNORECASE)
        if m:
            html_text = html_text[:m.end()]
            break
    return html_text


# ── 核心逻辑 ─────────────────────────────────────────────

def fetch_url(url: str, timeout: int = REQUEST_TIMEOUT) -> tuple[str | None, str | None]:
    """抓取 URL，返回 (content, error_message)"""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            for enc in ("utf-8", "gbk", "gb2312", "latin-1"):
                try:
                    return raw.decode(enc), None
                except UnicodeDecodeError:
                    continue
            return raw.decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"连接失败: {e.reason}"
    except Exception as e:
        return None, f"未知错误: {e}"


def process_content(raw: str, url: str) -> str:
    """将抓到的原始内容转为 Markdown"""
    raw_stripped = raw.strip()
    # 已经是纯文本 / Markdown（非 HTML）
    if not raw_stripped.startswith("<!") and not raw_stripped.startswith("<html"):
        return raw_stripped
    # HTML → 提取正文 → Markdown
    body = _extract_main_content(raw)
    return _basic_html_to_md(body)


def save_doc(content: str, filename: str) -> str:
    """保存到 data/ 目录，返回完整路径"""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    filepath = os.path.join(config.DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


# ── 主流程 ────────────────────────────────────────────────

def main() -> None:
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    total = len(SOURCES)
    ok, fail, skip = 0, 0, 0
    results: list[tuple[str, str, str]] = []

    print(f"文档抓取清单 · 共 {total} 个\n")

    for i, (filename, urls, note) in enumerate(SOURCES, 1):

        # 检查是否已存在
        filepath = os.path.join(config.DATA_DIR, filename)
        if os.path.exists(filepath):
            print(f"[{i:2d}/{total}] ⏭️  {filename}  ← 已存在，跳过")
            skip += 1
            results.append((filename, "已存在", "跳过"))
            continue

        print(f"[{i:2d}/{total}] 📥 {filename}  ({note})")
        if dry_run:
            for j, u in enumerate(urls):
                print(f"      候选 [{j+1}] {u}")
            continue

        # 依次尝试候选 URL
        raw = None
        error = None
        success_url = None

        for j, url in enumerate(urls):
            print(f"      尝试 [{j+1}/{len(urls)}] {url} ...", end=" ", flush=True)
            raw, error = fetch_url(url)
            if raw is not None:
                print("✅")
                success_url = url
                break
            else:
                print(f"❌ {error}")

        if raw is None:
            print(f"      → 所有候选 URL 均失败")
            fail += 1
            results.append((filename, "失败", f"尝试了 {len(urls)} 个 URL 均失败"))
            continue

        # 转 Markdown
        try:
            md_content = process_content(raw, success_url)
        except Exception as e:
            print(f"      → 转换失败: {e}")
            fail += 1
            results.append((filename, "转换失败", str(e)))
            continue

        if not md_content or len(md_content.strip()) < 80:
            print(f"      ⚠️  内容过短 ({len(md_content)} 字符)，仍保存")

        # 保存
        saved_path = save_doc(md_content, filename)
        size_kb = os.path.getsize(saved_path) / 1024
        print(f"      → 已保存 {size_kb:.1f} KB")
        ok += 1
        results.append((filename, "成功", f"{size_kb:.1f} KB"))

        if i < total:
            time.sleep(REQUEST_DELAY)

    # ── 汇总 ──
    print(f"\n{'='*50}")
    print(f"  完成: {ok} 成功 · {skip} 跳过 · {fail} 失败 · 共 {total} 个")
    print(f"{'='*50}")

    if fail:
        print("\n失败项（需手动确认 URL）：")
        for name, status, detail in results:
            if status == "失败":
                print(f"  ❌ {name}: {detail}")
        print("\n👉 打开对应文档站，找到正确页面 URL，更新 SOURCES 中的候选列表即可。")

    if ok > 0:
        print(f"\n文档已保存到 {config.DATA_DIR}/")
        print(f"确认无误后运行: python ingest.py   # 重新入库")


if __name__ == "__main__":
    main()
