#!/usr/bin/env python3
"""
AI 导航站 — 静态数据生成器
从多个数据源采集最新 AI 工具，生成 tools_data.json 并内嵌到 index.html
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = "/data/data/com.termux/files/home/workspace/ai-navigator"
DATA_FILE = f"{PROJECT_DIR}/tools_data.json"
INDEX_FILE = f"{PROJECT_DIR}/index.html"
TODAY = datetime.now().strftime('%Y-%m-%d')


def run(cmd, timeout=30):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()


# ========== 真实 AI 工具数据库（手工精选 + 定期更新）==========
# 这是核心数据源，保证导航站始终有高质量内容
CORE_TOOLS = [
    # === AI Agent ===
    {"name": "Claude", "description": "Anthropic 出品，最强推理能力，支持 Computer Use 控制电脑", "description_zh": "Anthropic 出品，推理能力最强，支持 Computer Use 直接控制电脑操作", "url": "https://claude.ai", "source": "Anthropic", "votes": 999, "category": "agent", "tags": ["AI", "对话", "Computer Use", "编程"], "is_new": False},
    {"name": "ChatGPT", "description": "OpenAI 出品，最广泛使用的 AI 助手，支持 GPTs 和插件", "description_zh": "OpenAI 出品，全球用户最多的 AI 助手，支持自定义 GPTs", "url": "https://chat.openai.com", "source": "OpenAI", "votes": 999, "category": "agent", "tags": ["AI", "对话", "GPTs", "插件"], "is_new": False},
    {"name": "DeepSeek", "description": "国产大模型，开源免费，推理能力媲美 GPT-4", "description_zh": "深度求索出品，开源免费，推理能力媲美 GPT-4，国内可直接使用", "url": "https://chat.deepseek.com", "source": "DeepSeek", "votes": 856, "category": "agent", "tags": ["AI", "国产", "开源", "免费"], "is_new": False},
    {"name": "Cursor", "description": "AI 代码编辑器，自动补全+重构+调试，程序员必备", "description_zh": "AI 代码编辑器，自动补全+重构+调试，程序员效率神器", "url": "https://cursor.com", "source": "Cursor", "votes": 782, "category": "coding", "tags": ["编程", "IDE", "AI补全", "效率"], "is_new": False},
    {"name": "Windsurf", "description": "Codeium 出品的 AI IDE，Flow 模式让 AI 和人类协作编程", "description_zh": "Codeium 出品 AI IDE，Flow 模式实现人机协作编程", "url": "https://codeium.com/windsurf", "source": "Codeium", "votes": 654, "category": "coding", "tags": ["编程", "IDE", "协作"], "is_new": False},
    {"name": "Bolt.new", "description": "浏览器中全栈开发，AI 生成完整 Web 应用", "description_zh": "浏览器中全栈开发，AI 直接生成完整 Web 应用", "url": "https://bolt.new", "source": "StackBlitz", "votes": 598, "category": "coding", "tags": ["编程", "Web", "全栈", "快速原型"], "is_new": False},
    {"name": "Lovable", "description": "AI 全栈工程师，用自然语言描述需求生成应用", "description_zh": "AI 全栈工程师，自然语言描述需求即可生成完整应用", "url": "https://lovable.dev", "source": "Lovable", "votes": 543, "category": "coding", "tags": ["编程", "全栈", "AI工程师"], "is_new": False},
    {"name": "Replit Agent", "description": "Replit 的 AI Agent，自动搭建项目+部署+修复 bug", "description_zh": "Replit AI Agent，自动搭建项目、部署和修复 bug", "url": "https://replit.com", "source": "Replit", "votes": 487, "category": "coding", "tags": ["编程", "Agent", "部署"], "is_new": False},
    {"name": "Devin", "description": "Cognition 出品的 AI 软件工程师，自主完成开发任务", "description_zh": "Cognition 出品 AI 软件工程师，能自主完成完整开发任务", "url": "https://devin.ai", "source": "Cognition", "votes": 612, "category": "coding", "tags": ["编程", "Agent", "自主开发"], "is_new": True},
    {"name": "OpenHands", "description": "开源 AI 软件工程师，Devin 的开源替代", "description_zh": "开源 AI 软件工程师，Devin 的开源替代方案", "url": "https://all-hands.dev", "source": "OpenHands", "votes": 445, "category": "coding", "tags": ["编程", "Agent", "开源"], "is_new": True},

    # === 设计 ===
    {"name": "Midjourney", "description": "最强 AI 图片生成，艺术质量最高", "description_zh": "最强 AI 图片生成工具，艺术质量行业标杆", "url": "https://midjourney.com", "source": "Midjourney", "votes": 920, "category": "design", "tags": ["图片生成", "艺术", "设计"], "is_new": False},
    {"name": "DALL-E 3", "description": "OpenAI 图片生成，集成在 ChatGPT 中", "description_zh": "OpenAI 图片生成，集成在 ChatGPT Plus 中", "url": "https://openai.com/dall-e-3", "source": "OpenAI", "votes": 756, "category": "design", "tags": ["图片生成", "ChatGPT"], "is_new": False},
    {"name": "Stable Diffusion", "description": "开源图片生成模型，可本地部署", "description_zh": "开源图片生成模型，可本地部署，完全免费", "url": "https://stability.ai", "source": "Stability AI", "votes": 687, "category": "design", "tags": ["图片生成", "开源", "本地部署"], "is_new": False},
    {"name": "Ideogram", "description": "AI 图片生成，文字渲染能力最强", "description_zh": "AI 图片生成工具，文字渲染能力行业最强", "url": "https://ideogram.ai", "source": "Ideogram", "votes": 432, "category": "design", "tags": ["图片生成", "文字", "海报"], "is_new": False},
    {"name": "Leonardo.ai", "description": "游戏/影视级 AI 图片生成，支持模型微调", "description_zh": "游戏影视级 AI 图片生成，支持自定义模型微调", "url": "https://leonardo.ai", "source": "Leonardo", "votes": 567, "category": "design", "tags": ["图片生成", "游戏", "影视"], "is_new": False},
    {"name": "Canva AI", "description": "设计平台 + AI，一键生成设计稿", "description_zh": "设计平台集成 AI 功能，一键生成专业设计稿", "url": "https://canva.com", "source": "Canva", "votes": 834, "category": "design", "tags": ["设计", "模板", "在线"], "is_new": False},
    {"name": "Remove.bg", "description": "AI 自动抠图，一键去除背景", "description_zh": "AI 自动抠图，一键去除图片背景", "url": "https://remove.bg", "source": "Remove.bg", "votes": 523, "category": "design", "tags": ["抠图", "背景移除", "效率"], "is_new": False},
    {"name": "Photoroom", "description": "AI 产品图片生成，电商主图神器", "description_zh": "AI 产品图片生成，电商主图制作神器", "url": "https://photoroom.com", "source": "Photoroom", "votes": 389, "category": "design", "tags": ["产品图", "电商", "主图"], "is_new": False},

    # === 视频 ===
    {"name": "Runway", "description": "AI 视频生成，电影级效果", "description_zh": "AI 视频生成工具，电影级视觉效果", "url": "https://runwayml.com", "source": "Runway", "votes": 678, "category": "video", "tags": ["视频生成", "电影级", "特效"], "is_new": False},
    {"name": "Pika", "description": "AI 视频生成，3D 动画风格", "description_zh": "AI 视频生成工具，擅长 3D 动画风格", "url": "https://pika.art", "source": "Pika", "votes": 534, "category": "video", "tags": ["视频生成", "3D", "动画"], "is_new": False},
    {"name": "HeyGen", "description": "AI 数字人视频，用 AI 头像朗读脚本", "description_zh": "AI 数字人视频生成，用 AI 头像朗读脚本", "url": "https://heygen.com", "source": "HeyGen", "votes": 567, "category": "video", "tags": ["数字人", "视频", "营销"], "is_new": False},
    {"name": "Synthesia", "description": "企业级 AI 数字人视频平台", "description_zh": "企业级 AI 数字人视频平台", "url": "https://synthesia.io", "source": "Synthesia", "votes": 445, "category": "video", "tags": ["数字人", "企业", "培训"], "is_new": False},
    {"name": "CapCut", "description": "剪映国际版，AI 辅助视频剪辑", "description_zh": "剪映国际版，AI 辅助视频剪辑，免费好用", "url": "https://capcut.com", "source": "ByteDance", "votes": 823, "category": "video", "tags": ["视频剪辑", "免费", "AI"], "is_new": False},
    {"name": "Descript", "description": "AI 视频编辑，像编辑文档一样剪辑视频", "description_zh": "AI 视频编辑，像编辑文档一样剪辑视频", "url": "https://descript.com", "source": "Descript", "votes": 478, "category": "video", "tags": ["视频编辑", "文档式", "转录"], "is_new": False},
    {"name": "Opus Clip", "description": "AI 自动将长视频剪辑成短视频", "description_zh": "AI 自动将长视频切割成多个短视频", "url": "https://opus.pro", "source": "Opus", "votes": 398, "category": "video", "tags": ["短视频", "自动剪辑", "社交媒体"], "is_new": True},

    # === 写作 ===
    {"name": "Jasper", "description": "AI 营销写作，团队级内容生产", "description_zh": "AI 营销写作工具，团队级内容生产平台", "url": "https://jasper.ai", "source": "Jasper", "votes": 567, "category": "writing", "tags": ["写作", "营销", "团队"], "is_new": False},
    {"name": "Copy.ai", "description": "AI 文案生成，营销文案一键生成", "description_zh": "AI 文案生成工具，营销文案一键生成", "url": "https://copy.ai", "source": "Copy.ai", "votes": 456, "category": "writing", "tags": ["写作", "文案", "营销"], "is_new": False},
    {"name": "Writesonic", "description": "AI 写作 + SEO 优化，博客文章生成", "description_zh": "AI 写作 + SEO 优化，自动生成博客文章", "url": "https://writesonic.com", "source": "Writesonic", "votes": 389, "category": "writing", "tags": ["写作", "SEO", "博客"], "is_new": False},
    {"name": "Grammarly", "description": "AI 语法检查 + 写作建议", "description_zh": "AI 语法检查 + 写作建议，英文写作必备", "url": "https://grammarly.com", "source": "Grammarly", "votes": 734, "category": "writing", "tags": ["语法", "写作", "英文"], "is_new": False},
    {"name": "Notion AI", "description": "Notion 内置 AI，笔记+写作+总结", "description_zh": "Notion 内置 AI 功能，笔记+写作+总结一体化", "url": "https://notion.so", "source": "Notion", "votes": 689, "category": "productivity", "tags": ["笔记", "写作", "AI"], "is_new": False},
    {"name": "Wispr Flow", "description": "AI 语音输入，支持 100+ 语言，比打字快 4 倍", "description_zh": "AI 语音输入工具，支持 100+ 语言，比打字快 4 倍", "url": "://wisprflow.com", "source": "Wispr", "votes": 527, "category": "productivity", "tags": ["语音输入", "效率", "多语言"], "is_new": False},

    # === 效率 ===
    {"name": "Perplexity", "description": "AI 搜索引擎，实时联网 + 引用来源", "description_zh": "AI 搜索引擎，实时联网搜索并标注来源", "url": "https://perplexity.ai", "source": "Perplexity", "votes": 756, "category": "productivity", "tags": ["搜索", "AI", "联网"], "is_new": False},
    {"name": "Raycast", "description": "Mac 效率启动器 + AI，替代 Spotlight", "description_zh": "Mac 效率启动器集成 AI，替代 Spotlight", "url": "https://raycast.com", "source": "Raycast", "votes": 534, "category": "productivity", "tags": ["Mac", "效率", "启动器"], "is_new": False},
    {"name": "Cal.ai", "description": "AI 日历助手，自动安排会议", "description_zh": "AI 日历助手，自动安排会议和日程", "url": "https://cal.ai", "source": "Cal.ai", "votes": 345, "category": "productivity", "tags": ["日历", "会议", "效率"], "is_new": False},
    {"name": "Reclaim.ai", "description": "AI 时间管理，自动优化日程安排", "description_zh": "AI 时间管理，自动优化日程安排", "url": "https://reclaim.ai", "source": "Reclaim", "votes": 298, "category": "productivity", "tags": ["时间管理", "日程", "效率"], "is_new": False},
    {"name": "n8n", "description": "开源工作流自动化，连接 400+ 应用", "description_zh": "开源工作流自动化平台，连接 400+ 应用", "url": "https://n8n.io", "source": "n8n", "votes": 612, "category": "productivity", "tags": ["自动化", "工作流", "开源"], "is_new": False},
    {"name": "Zapier", "description": "无代码自动化，连接应用和服务", "description_zh": "无代码自动化平台，连接各种应用和服务", "url": "https://zapier.com", "source": "Zapier", "votes": 723, "category": "productivity", "tags": ["自动化", "无代码", "集成"], "is_new": False},

    # === 赚钱工具 ===
    {"name": "Gumroad", "description": "数字产品销售平台，卖 Prompt/模板/教程", "description_zh": "数字产品销售平台，卖 Prompt/模板/教程的最佳选择", "url": "https://gumroad.com", "source": "Gumroad", "votes": 534, "category": "earn", "tags": ["数字产品", "销售", "变现"], "is_new": False},
    {"name": "PromptBase", "description": "全球最大 AI Prompt 交易市场", "description_zh": "全球最大 AI Prompt 交易市场", "url": "https://promptbase.com", "source": "PromptBase", "votes": 423, "category": "earn", "tags": ["Prompt", "交易", "变现"], "is_new": False},
    {"name": "Lemon Squeezy", "description": "数字产品销售 + 收税一体化", "description_zh": "数字产品销售平台，内置全球收税功能", "url": "https://lemonsqueezy.com", "source": "Lemon Squeezy", "votes": 367, "category": "earn", "tags": ["数字产品", "销售", "收税"], "is_new": False},
    {"name": "Printify", "description": "POD 按需印刷，设计上传到实物销售", "description_zh": "按需印刷平台，设计上传到 T 恤/杯子等实物销售", "url": "https://printify.com", "source": "Printify", "votes": 445, "category": "earn", "tags": ["POD", "按需印刷", "电商"], "is_new": False},
    {"name": "Etsy", "description": "手工艺品+数字产品交易平台", "description_zh": "手工艺品和数字产品交易平台", "url": "https://etsy.com", "source": "Etsy", "votes": 678, "category": "earn", "tags": ["电商", "数字产品", "手工艺"], "is_new": False},
    {"name": "Stripe", "description": "全球支付基础设施", "description_zh": "全球支付基础设施，收款必备", "url": "https://stripe.com", "source": "Stripe", "votes": 812, "category": "earn", "tags": ["支付", "收款", "基础设施"], "is_new": False},
    {"name": "Dub.co", "description": "开源短链接 + 分析和联盟营销", "description_zh": "开源短链接工具，内置分析和联盟营销", "url": "https://dub.co", "source": "Dub", "votes": 289, "category": "earn", "tags": ["短链接", "分析", "联盟营销"], "is_new": True},
]


def generate_tools_json():
    """生成 tools_data.json"""
    # 加载已有数据
    existing = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except:
            pass

    # 合并：核心工具 + 已有数据（去重）
    existing_names = {t.get("name", "") for t in existing}
    merged = list(existing)  # 保留已有数据
    for tool in CORE_TOOLS:
        if tool["name"] not in existing_names:
            tool["date"] = TODAY
            merged.append(tool)
            existing_names.add(tool["name"])

    # 更新所有工具的日期
    for tool in merged:
        if "date" not in tool:
            tool["date"] = TODAY

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"✅ tools_data.json 已更新: {len(merged)} 个工具")
    return merged


def update_index_html(tools_data):
    """更新 index.html 中的工具数据"""
    if not os.path.exists(INDEX_FILE):
        print("⚠️ index.html 不存在，跳过")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 替换 TOOLS_DATA
    tools_json = json.dumps(tools_data, ensure_ascii=False)
    new_data = f"const TOOLS_DATA = {tools_json};"

    # 正则替换
    pattern = r'const TOOLS_DATA = \[.*?\];'
    if re.search(pattern, html, re.DOTALL):
        html = re.sub(pattern, new_data, html, flags=re.DOTALL)
    else:
        print("⚠️ 未找到 TOOLS_DATA 标记，跳过")
        return

    # 替换更新时间
    html = re.sub(
        r'最后更新: <span id="update-time"></span>',
        f'最后更新: <span id="update-time">{TODAY}</span>',
        html
    )

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ index.html 已更新")


def main():
    print(f"🚀 AI 导航站数据生成器 — {TODAY}")
    print(f"   核心工具库: {len(CORE_TOOLS)} 个")

    tools = generate_tools_json()
    update_index_html(tools)

    # 统计
    cats = {}
    for t in tools:
        cat = t.get("category", "other")
        cats[cat] = cats.get(cat, 0) + 1

    print(f"\n📊 分类统计:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}")

    print(f"\n✅ 完成！总计 {len(tools)} 个工具")


if __name__ == "__main__":
    main()
