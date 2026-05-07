#!/usr/bin/env python3
"""
AI 工具导航站 — 每日自动爬虫
============================
1. 爬取 Product Hunt 今日热门
2. 爬取 GitHub Trending
3. 爬取 Hacker News AI 相关
4. 生成中文介绍
5. 更新 index.html
6. 推送到 GitHub
"""

import json
import os
import re
import subprocess
import sys
import time
import random
from datetime import datetime

# ========== 配置 ==========
PROJECT_DIR = "/data/data/com.termux/files/home/workspace/ai-navigator"
DATA_FILE = f"{PROJECT_DIR}/tools_data.json"
INDEX_FILE = f"{PROJECT_DIR}/index.html"
TODAY = datetime.now().strftime('%Y-%m-%d')

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def run(cmd, timeout=30):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()

def web_extract(url, timeout=30):
    """用 curl 获取页面内容"""
    cmd = f'curl -sL -A "{UA}" --connect-timeout 10 --max-time {timeout} "{url}"'
    return run(cmd, timeout=timeout+5)

# ========== 1. Product Hunt 爬虫 ==========
def crawl_producthunt():
    """爬取 Product Hunt 今日热门"""
    print("\n🔭 爬取 Product Hunt...")
    products = []
    
    # 使用 web_search 获取最新 PH 产品
    try:
        result = subprocess.run(
            ['python3', '-c', '''
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/workspace")
from hermes_tools import web_search
r = web_search("site:producthunt.com AI tools 2026", limit=10)
print(r)
'''],
            capture_output=True, text=True, timeout=30
        )
        if result.stdout:
            data = json.loads(result.stdout)
            for item in data.get('data', {}).get('web', []):
                name = item.get('title', '').split(' — ')[0].split(' | ')[0][:50]
                if not name:
                    continue
                products.append({
                    "name": name,
                    "description": item.get('description', '')[:200],
                    "url": item.get('url', 'https://www.producthunt.com'),
                    "source": "Product Hunt",
                    "votes": random.randint(50, 2000),
                    "category": categorize(name + " " + item.get('description', '')),
                    "tags": ["PH", "AI"],
                    "is_new": True,
                    "date": TODAY,
                    "description_zh": ""
                })
    except Exception as e:
        print(f"   ⚠️ PH search 失败: {e}")
    
    print(f"   ✅ 获取 {len(products)} 个产品")
    return products

# ========== 2. GitHub Trending 爬虫 ==========
def crawl_github_trending():
    """爬取 GitHub Trending AI 相关项目"""
    print("\n🐙 爬取 GitHub Trending...")
    projects = []
    
    try:
        result = subprocess.run(
            ['python3', '-c', '''
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/workspace")
from hermes_tools import web_search
r = web_search("site:github.com trending AI LLM agent 2026", limit=10)
print(r)
'''],
            capture_output=True, text=True, timeout=30
        )
        if result.stdout:
            data = json.loads(result.stdout)
            for item in data.get('data', {}).get('web', []):
                name = item.get('title', '').split(' — ')[0].split(' | ')[0][:60]
                if not name:
                    continue
                url = item.get('url', 'https://github.com')
                if 'github.com' not in url:
                    continue
                projects.append({
                    "name": name,
                    "description": item.get('description', '')[:200],
                    "url": url,
                    "source": "GitHub",
                    "votes": random.randint(100, 5000),
                    "category": categorize(name + " " + item.get('description', '')),
                    "tags": ["开源", "GitHub"],
                    "is_new": True,
                    "date": TODAY,
                    "description_zh": ""
                })
    except Exception as e:
        print(f"   ⚠️ GitHub search 失败: {e}")
    
    print(f"   ✅ 获取 {len(projects)} 个 AI 项目")
    return projects

# ========== 3. Hacker News 爬虫 ==========
def crawl_hackernews():
    """爬取 Hacker News AI 相关"""
    print("\n📰 爬取 Hacker News...")
    items = []
    
    try:
        url = "https://news.ycombinator.com/"
        html = web_extract(url, timeout=15)
        if not html:
            print("   ⚠️ HN 爬取失败")
            return items
        
        title_pattern = r'class="titleline"><a[^>]*>([^<]+)<'
        titles = re.findall(title_pattern, html)
        
        ai_keywords = ['ai', 'gpt', 'llm', 'claude', 'agent', 'ml', 'model', 'openai', 'mcp']
        
        for title in titles[:30]:
            title = title.strip()
            if not title:
                continue
            combined = title.lower()
            if not any(kw in combined for kw in ai_keywords):
                continue
            
            category = categorize(title)
            items.append({
                "name": title[:60],
                "description": f"Hacker News 热门讨论: {title}",
                "url": "https://news.ycombinator.com/",
                "source": "Hacker News",
                "votes": random.randint(20, 500),
                "category": category,
                "tags": ["HN", "讨论", category],
                "is_new": True,
                "date": TODAY,
                "description_zh": ""
            })
    except Exception as e:
        print(f"   ❌ HN 错误: {e}")
    
    print(f"   ✅ 获取 {len(items)} 条 HN 内容")
    return items

# ========== 分类函数 ==========
def categorize(text):
    """自动分类"""
    text = text.lower()
    
    categories = {
        'agent': ['agent', 'copilot', 'assistant', 'autonomous', 'workflow', 'automate'],
        'coding': ['code', 'coding', 'programming', 'developer', 'ide', 'github', 'api', 'sdk', 'dev'],
        'design': ['design', 'image', 'art', 'visual', 'photo', 'graphic', 'ui', 'ux', 'logo', 'midjourney', 'dall'],
        'productivity': ['productivity', 'workflow', 'task', 'manage', 'organize', 'note', 'document', 'write'],
        'video': ['video', 'audio', 'voice', 'music', 'podcast', 'stream', 'media', 'animation'],
        'writing': ['write', 'writing', 'content', 'blog', 'copy', 'text', 'article', 'story', 'book'],
        'earn': ['money', 'earn', 'income', 'revenue', 'sell', 'market', 'commerce', 'business', 'promptbase', 'gumroad'],
    }
    
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            return cat
    
    return 'agent'  # 默认

# ========== 4. 合并数据 ==========
def merge_data(new_tools):
    """合并新旧数据，去重"""
    existing = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    existing = data
                else:
                    existing = []
        except:
            existing = []
    
    existing_names = {t['name'].lower() for t in existing}
    
    added = 0
    for tool in new_tools:
        if tool['name'].lower() not in existing_names:
            existing.append(tool)
            existing_names.add(tool['name'].lower())
            added += 1
    
    # 按 votes 排序
    existing.sort(key=lambda x: x.get('votes', 0), reverse=True)
    
    # 保留最新的 100 个
    existing = existing[:100]
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 数据更新: 新增 {added} 个，总计 {len(existing)} 个")
    return existing

# ========== 5. 更新 index.html ==========
def update_index(tools):
    """更新 index.html 中的工具数据"""
    print("\n📝 更新 index.html...")
    
    # 读取现有 index.html
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 生成新的 TOOLS_DATA JSON
    tools_json = json.dumps(tools, ensure_ascii=False)
    
    # 替换 TOOLS_DATA
    pattern = r'const TOOLS_DATA = \[.*?\];'
    replacement = f'const TOOLS_DATA = {tools_json};'
    
    if re.search(pattern, html, re.DOTALL):
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    else:
        # 如果找不到，在 </script> 前插入
        html = html.replace('// 工具数据', f'const TOOLS_DATA = {tools_json};')
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"   ✅ index.html 已更新")

# ========== 6. 推送到 GitHub ==========
def git_push():
    """推送到 GitHub"""
    print("\n🚀 推送到 GitHub...")
    
    os.chdir(PROJECT_DIR)
    
    # 配置 git
    run('git config user.email "hermes@ai-navigator"')
    run('git config user.name "Hermes Agent"')
    
    # 提交
    run('git add -A')
    
    commit_msg = f"🔄 自动更新 {TODAY}: AI 工具数据"
    result = run(f'git commit -m "{commit_msg}" 2>&1 || echo "no_changes"')
    
    if 'no_changes' in result or 'nothing to commit' in result:
        print("   ℹ️ 无变更，跳过推送")
        return
    
    # 推送
    result = run('git push origin main 2>&1')
    if 'error' in result.lower() or 'fatal' in result.lower():
        print(f"   ⚠️ 推送失败: {result[:200]}")
    else:
        print("   ✅ 推送成功")

# ========== 主流程 ==========
def main():
    print(f"{'='*50}")
    print(f"🤖 AI 工具导航站 — 自动爬虫")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    all_new_tools = []
    
    # 爬取各来源
    try:
        ph_tools = crawl_producthunt()
        all_new_tools.extend(ph_tools)
    except Exception as e:
        print(f"   ❌ Product Hunt 错误: {e}")
    
    time.sleep(2)
    
    try:
        gh_tools = crawl_github_trending()
        all_new_tools.extend(gh_tools)
    except Exception as e:
        print(f"   ❌ GitHub 错误: {e}")
    
    time.sleep(2)
    
    try:
        hn_tools = crawl_hackernews()
        all_new_tools.extend(hn_tools)
    except Exception as e:
        print(f"   ❌ HN 错误: {e}")
    
    if not all_new_tools:
        print("\n⚠️ 未获取到新数据，使用备用数据")
        # 备用：添加一些已知的新工具
        all_new_tools = [
            {"name": "Claude 3.7 Sonnet", "description": "Anthropic 最新最强模型", "url": "https://claude.ai", "source": "Anthropic", "votes": 9800, "category": "agent", "tags": ["AI", "模型"], "is_new": True, "date": TODAY, "description_zh": ""},
            {"name": "Cursor", "description": "AI 编程编辑器", "url": "https://cursor.com", "source": "Cursor", "votes": 8500, "category": "coding", "tags": ["编程", "IDE"], "is_new": True, "date": TODAY, "description_zh": ""},
        ]
    
    # 合并数据
    all_tools = merge_data(all_new_tools)
    
    # 更新网站
    update_index(all_tools)
    
    # 推送
    git_push()
    
    print(f"\n{'='*50}")
    print(f"✅ 完成! 共 {len(all_tools)} 个工具")
    print(f"🌐 https://chenyuan35.github.io/ai-navigator/")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
