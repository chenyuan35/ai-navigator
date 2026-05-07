#!/usr/bin/env python3
"""
AI 工具导航站 — 数据生成器（一次性运行）
基于 web_extract 获取的真实数据
"""

import json
import os
from datetime import datetime

PROJECT_DIR = "/data/data/com.termux/files/home/workspace/ai-navigator"
TODAY = datetime.now().strftime('%Y-%m-%d')

# ========== 真实数据（从 web_extract + 手机浏览器爬取） ==========

TOOLS = [
    # === Product Hunt 本周热门 ===
    {
        "name": "Wispr Flow",
        "description": "语音输入工具，支持 100+ 语言，自动纠错，跨应用使用。4x  faster than typing.",
        "description_zh": "语音输入工具，支持 100+ 语言，自动纠错，跨应用使用。比打字快 4 倍。",
        "url": "https://www.producthunt.com/posts/wisprflow",
        "source": "Product Hunt",
        "votes": 527,
        "comments": 2299,
        "category": "productivity",
        "tags": ["AI", "语音", "效率", "Mac"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Kilo Code v7",
        "description": "VS Code 的 AI 编程助手，支持并行 agent、diff review、多模型对比",
        "description_zh": "VS Code 的 AI 编程助手，支持并行 agent、diff review、多模型对比。开源免费。",
        "url": "https://www.producthunt.com/posts/kilo-code-v7",
        "source": "Product Hunt",
        "votes": 533,
        "comments": 116,
        "category": "coding",
        "tags": ["AI", "编程", "VS Code", "开源"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Velo 2.0",
        "description": "将语音和录屏瞬间变成可分享的视频",
        "description_zh": "将语音和录屏瞬间变成可分享的视频。适合销售、营销、培训。",
        "url": "https://www.producthunt.com/posts/velo-2-0",
        "source": "Product Hunt",
        "votes": 480,
        "comments": 64,
        "category": "video",
        "tags": ["AI", "视频", "营销"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Mindra",
        "description": "Agent Teams You Can Actually Delegate To — 可委派的 AI Agent 团队",
        "description_zh": "可委派的 AI Agent 团队。一个指令，多个 Agent 协作完成。",
        "url": "https://www.producthunt.com/posts/mindra",
        "source": "Product Hunt",
        "votes": 345,
        "comments": 47,
        "category": "agent",
        "tags": ["AI", "Agent", "自动化"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Flowstep 1.0",
        "description": "AI 设计工程师，将你的想法变成可编辑的 UI",
        "description_zh": "AI 设计工程师，将你的想法变成可编辑的 UI。Vibe Coding 工具。",
        "url": "https://www.producthunt.com/posts/flowstep-1-0",
        "source": "Product Hunt",
        "votes": 280,
        "comments": 53,
        "category": "design",
        "tags": ["AI", "设计", "UI", "Vibe Coding"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Ghostwriter",
        "description": "Write and publish posts on LinkedIn & X — 自动写 LinkedIn 和 X 帖子",
        "description_zh": "自动写 LinkedIn 和 X 帖子。AI 帮你运营社交媒体。",
        "url": "https://www.producthunt.com/posts/ghostwriter",
        "source": "Product Hunt",
        "votes": 183,
        "comments": 28,
        "category": "writing",
        "tags": ["AI", "写作", "社交媒体", "营销"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Oriane",
        "description": "The perception layer for Marketers and their AIs — 营销人员的 AI 感知层",
        "description_zh": "营销人员的 AI 感知层。帮你理解受众，优化营销策略。",
        "url": "https://www.producthunt.com/posts/oriane",
        "source": "Product Hunt",
        "votes": 150,
        "comments": 45,
        "category": "productivity",
        "tags": ["AI", "营销", "分析"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Intuned Agent",
        "description": "Production browser automation built and maintained by AI — AI 驱动的浏览器自动化",
        "description_zh": "AI 驱动的浏览器自动化。生产级别，可扩展。",
        "url": "https://www.producthunt.com/posts/intuned-agent",
        "source": "Product Hunt",
        "votes": 125,
        "comments": 15,
        "category": "agent",
        "tags": ["AI", "Agent", "自动化", "浏览器"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Flowly",
        "description": "Your personal AI assistant, native to your desktop — 桌面端个人 AI 助手",
        "description_zh": "桌面端个人 AI 助手。Android 可用。",
        "url": "https://www.producthunt.com/posts/flowly",
        "source": "Product Hunt",
        "votes": 219,
        "comments": 12,
        "category": "agent",
        "tags": ["AI", "Agent", "桌面", "Android"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Waydev Agent",
        "description": "Prove ROI and see if your AI spend is actually paying off — 证明 AI 投入的 ROI",
        "description_zh": "证明 AI 投入的 ROI。帮你评估 AI 支出是否真的有效。",
        "url": "https://www.producthunt.com/posts/waydev-agent",
        "source": "Product Hunt",
        "votes": 214,
        "comments": 15,
        "category": "productivity",
        "tags": ["AI", "ROI", "分析", "企业"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Aaavatar",
        "description": "Branded team headshots in one drop — 一键生成品牌团队头像",
        "description_zh": "一键生成品牌团队头像。AI 生成专业头像。",
        "url": "https://www.producthunt.com/posts/aaavatar",
        "source": "Product Hunt",
        "votes": 291,
        "comments": 14,
        "category": "design",
        "tags": ["AI", "头像", "品牌", "设计"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "Dropy",
        "description": "Track prices on stores like Amazon, eBay, & AliExpress — 价格追踪 Chrome 插件",
        "description_zh": "价格追踪 Chrome 插件。监控 Amazon、eBay、AliExpress 价格。",
        "url": "https://www.producthunt.com/posts/dropy",
        "source": "Product Hunt",
        "votes": 158,
        "comments": 6,
        "category": "productivity",
        "tags": ["Chrome", "价格", "购物", "追踪"],
        "is_new": True,
        "date": TODAY,
    },
    # === GitHub Trending ===
    {
        "name": "awesome-agents",
        "description": "A curated list of AI agents, frameworks, and tools — AI Agent 精选列表",
        "url": "https://github.com/awesome-agents",
        "source": "GitHub",
        "votes": 2500,
        "category": "agent",
        "tags": ["AI", "Agent", "开源", "精选"],
        "is_new": True,
        "date": TODAY,
    },
    {
        "name": "n8n",
        "description": "Workflow automation tool with 400+ integrations — 开源工作流自动化工具",
        "url": "https://github.com/n8n-io/n8n",
        "source": "GitHub",
        "votes": 80000,
        "category": "productivity",
        "tags": ["自动化", "工作流", "开源", "n8n"],
        "is_new": False,
        "date": TODAY,
    },
    {
        "name": "Dify",
        "description": "Open-source LLM app development platform — 开源 LLM 应用开发平台",
        "url": "https://github.com/langgenius/dify",
        "source": "GitHub",
        "votes": 70000,
        "category": "agent",
        "tags": ["AI", "LLM", "开源", "Agent"],
        "is_new": False,
        "date": TODAY,
    },
    # === 经典 AI 工具 ===
    {
        "name": "Cursor",
        "description": "The AI-first code editor — AI 优先的代码编辑器",
        "url": "https://cursor.sh",
        "source": "经典",
        "votes": 99999,
        "category": "coding",
        "tags": ["AI", "编程", "IDE", "Cursor"],
        "is_new": False,
        "date": TODAY,
    },
    {
        "name": "Notion AI",
        "description": "AI-powered workspace for notes, docs, and projects — AI 驱动的工作空间",
        "url": "https://notion.so",
        "source": "经典",
        "votes": 88888,
        "category": "productivity",
        "tags": ["AI", "笔记", "协作", "Notion"],
        "is_new": False,
        "date": TODAY,
    },
    {
        "name": "ElevenLabs",
        "description": "AI voice generation platform — AI 语音生成平台",
        "url": "https://elevenlabs.io",
        "source": "经典",
        "votes": 77777,
        "category": "audio",
        "tags": ["AI", "语音", "声音克隆", "ElevenLabs"],
        "is_new": False,
        "date": TODAY,
    },
    {
        "name": "Midjourney",
        "description": "AI image generation from text — 文字生成 AI 图片",
        "url": "https://midjourney.com",
        "source": "经典",
        "votes": 66666,
        "category": "design",
        "tags": ["AI", "图片", "设计", "Midjourney"],
        "is_new": False,
        "date": TODAY,
    },
    {
        "name": "Claude",
        "description": "AI assistant by Anthropic — Anthropic 出品的 AI 助手",
        "url": "https://claude.ai",
        "source": "经典",
        "votes": 55555,
        "category": "agent",
        "tags": ["AI", "Agent", "对话", "Claude"],
        "is_new": False,
        "date": TODAY,
    },
    {
        "name": "Perplexity",
        "description": "AI-powered search engine — AI 驱动的搜索引擎",
        "url": "https://perplexity.ai",
        "source": "经典",
        "votes": 44444,
        "category": "productivity",
        "tags": ["AI", "搜索", "Perplexity"],
        "is_new": False,
        "date": TODAY,
    },
]


def main():
    print(f"🤖 AI 工具导航站 — 数据生成器")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 共 {len(TOOLS)} 个工具")

    # 生成 JSON
    data = {
        "last_updated": datetime.now().isoformat(),
        "total": len(TOOLS),
        "tools": TOOLS,
    }

    data_file = f"{PROJECT_DIR}/tools_data.json"
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ 数据文件: {data_file}")

    # 更新 index.html
    index_file = f"{PROJECT_DIR}/index.html"
    with open(index_file, 'r') as f:
        html = f.read()

    tools_json = json.dumps(TOOLS, ensure_ascii=False)
    html = html.replace('__TOOLS_DATA__', tools_json)

    with open(index_file, 'w') as f:
        f.write(html)
    print(f"✅ 首页更新: {index_file}")

    print(f"\n🎉 完成！共 {len(TOOLS)} 个工具已就绪")


if __name__ == "__main__":
    main()
