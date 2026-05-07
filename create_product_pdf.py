#!/usr/bin/env python3
"""将产品 HTML 转换为可销售的 PDF"""

import re
import os
from fpdf import FPDF

class ProductPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, 'AI 赚钱工具包 | 50 个高转化 ChatGPT 商业 Prompts', 0, 1, 'C')
        self.set_draw_color(0, 212, 255)
        self.set_line_width(0.5)
        self.line(10, 18, 200, 18)
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'AI 赚钱工具包 2026 | 第 {self.page_no()} 页', 0, 0, 'C')

def html_to_text(html):
    """简单 HTML 转纯文本"""
    # 移除 script 和 style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    # 转换常见标签
    html = re.sub(r'<h1[^>]*>', '\n\n# ', html)
    html = re.sub(r'</h1>', '\n', html)
    html = re.sub(r'<h2[^>]*>', '\n\n## ', html)
    html = re.sub(r'</h2>', '\n', html)
    html = re.sub(r'<h3[^>]*>', '\n\n### ', html)
    html = re.sub(r'</h3>', '\n', html)
    html = re.sub(r'<li[^>]*>', '\n  - ', html)
    html = re.sub(r'</li>', '', html)
    html = re.sub(r'<br[^>]*/>', '\n', html)
    html = re.sub(r'<br>', '\n', html)
    html = re.sub(r'<p[^>]*>', '\n\n', html)
    html = re.sub(r'</p>', '', html)
    html = re.sub(r'<strong[^>]*>', '**', html)
    html = re.sub(r'</strong>', '**', html)
    html = re.sub(r'<code[^>]*>', '`', html)
    html = re.sub(r'</code>', '`', html)
    html = re.sub(r'<pre[^>]*>', '\n```\n', html)
    html = re.sub(r'</pre>', '\n```\n', html)
    html = re.sub(r'<div[^>]*>', '\n', html)
    html = re.sub(r'</div>', '\n', html)
    html = re.sub(r'<span[^>]*>', '', html)
    html = re.sub(r'</span>', '', html)
    html = re.sub(r'<table[^>]*>', '\n', html)
    html = re.sub(r'</table>', '\n', html)
    html = re.sub(r'<tr[^>]*>', '\n', html)
    html = re.sub(r'</tr>', '', html)
    html = re.sub(r'<td[^>]*>', ' | ', html)
    html = re.sub(r'</td>', '', html)
    html = re.sub(r'<th[^>]*>', ' | ', html)
    html = re.sub(r'</th>', '', html)
    html = re.sub(r'<ul[^>]*>', '\n', html)
    html = re.sub(r'</ul>', '\n', html)
    html = re.sub(r'<ol[^>]*>', '\n', html)
    html = re.sub(r'</ol>', '\n', html)
    
    # 移除所有剩余标签
    html = re.sub(r'<[^>]+>', '', html)
    
    # 清理空白
    html = re.sub(r'\n{3,}', '\n\n', html)
    
    # HTML 实体
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&amp;', '&')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&#39;', "'")
    html = html.replace('&quot;', '"')
    
    return html.strip()

def create_pdf():
    input_file = '/data/data/com.termux/files/home/workspace/ai-navigator/product-prompts.html'
    output_file = '/data/data/com.termux/files/home/workspace/ai-navigator/AI_Prompt_Product.pdf'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    text_content = html_to_text(html_content)
    
    pdf = ProductPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # 封面
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(26, 26, 46)
    pdf.ln(40)
    pdf.multi_cell(0, 15, '50 个高转化\nChatGPT 商业 Prompts', align='C')
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 8, 'AI 赚钱工具包 · 2026 版\n即拿即用 · 中英双语', align='C')
    pdf.ln(20)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6, '包含：营销 + 生产力 + 编程 + 创意 + 教育\n共 50 个即用型高级 Prompt', align='C')
    
    # 内容页
    pdf.add_page()
    
    # 按 Prompt 分割内容
    prompts = re.split(r'(?=### \d+\.)', text_content)
    
    for prompt in prompts:
        if not prompt.strip():
            continue
        
        # 检查是否需要新页面
        if pdf.get_y() > 250:
            pdf.add_page()
        
        lines = prompt.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                pdf.ln(3)
                continue
            
            # 标题检测
            if line.startswith('# '):
                if pdf.get_y() > 240:
                    pdf.add_page()
                pdf.set_font('Helvetica', 'B', 16)
                pdf.set_text_color(26, 26, 46)
                pdf.ln(5)
                pdf.multi_cell(0, 8, line[2:])
                pdf.ln(2)
            elif line.startswith('## '):
                if pdf.get_y() > 245:
                    pdf.add_page()
                pdf.set_font('Helvetica', 'B', 13)
                pdf.set_text_color(22, 33, 62)
                pdf.ln(3)
                pdf.multi_cell(0, 6, line[3:])
            elif line.startswith('### '):
                if pdf.get_y() > 250:
                    pdf.add_page()
                pdf.set_font('Helvetica', 'B', 11)
                pdf.set_text_color(50, 50, 50)
                pdf.ln(2)
                pdf.multi_cell(0, 5, line[4:])
            elif line.startswith('**') and line.endswith('**'):
                pdf.set_font('Helvetica', 'B', 9)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 5, line[2:-2])
            elif line.startswith('- ') or line.startswith('  - '):
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 4, '  ' + line)
            elif line.startswith('|'):
                # 表格行简化显示
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(80, 80, 80)
                cells = [c.strip() for c in line.split('|') if c.strip()]
                pdf.multi_cell(0, 4, '  ' + ' | '.join(cells))
            else:
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 4.5, line)
    
    pdf.output(output_file)
    size_kb = os.path.getsize(output_file) / 1024
    print(f"✅ PDF 已生成: {output_file}")
    print(f"   文件大小: {size_kb:.1f} KB")
    return output_file

if __name__ == '__main__':
    create_pdf()
