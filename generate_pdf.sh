#!/bin/bash
# 将 HTML 产品文件转换为 PDF（用于销售）
# 使用 wkhtmltopdf 或 pandoc

cd /data/data/com.termux/files/home/workspace/ai-navigator

# 检查是否有 wkhtmltopdf
if command -v wkhtmltopdf &> /dev/null; then
    wkhtmltopdf --page-size A4 --margin-top 15mm --margin-bottom 15mm --margin-left 15mm --margin-right 15mm product-prompts.html product-prompts.pdf
    echo "✅ PDF 已生成: product-prompts.pdf"
elif command -v pandoc &> /dev/null; then
    pandoc product-prompts.html -o product-prompts.pdf --pdf-engine=xelatex -V mainfont="Noto Sans CJK SC" -V geometry:margin=1in
    echo "✅ PDF 已生成: product-prompts.pdf"
else
    echo "⚠️ 未找到 PDF 转换工具"
    echo "HTML 文件已就绪，可使用在线工具转换为 PDF:"
    echo "https://www.sejda.com/html-to-pdf"
fi

ls -lh product-prompts.pdf 2>/dev/null || echo "PDF 文件大小: N/A"
