#!/bin/bash
# 足球预测生成器 - 快速构建脚本

echo "⚽ 足球预测内容生成器 - 双引擎架构"
echo "=================================="
echo ""

# 1. 检查环境
echo "📋 检查环境配置..."
if [ ! -f ".env" ]; then
    echo "❌ 错误：未找到 .env 文件"
    echo "请先复制 .env.example 并配置 API Keys"
    exit 1
fi

# 2. 安装依赖
echo "📦 检查 Python 依赖..."
pip3 install -q requests python-dotenv jinja2

# 3. 运行构建
echo ""
echo "🚀 开始生成预测内容..."
python3 build_football_predictions.py

# 4. 检查结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 构建完成！"
    echo ""
    echo "📁 生成的文件:"
    ls -lh src/pages/predictions/*.md 2>/dev/null || echo "   (无新文件)"
    echo ""
    echo "🎯 下一步操作:"
    echo "   1. 预览效果：npx astro dev"
    echo "   2. 提交代码：./push.sh"
    echo "   3. 查看 Vercel 部署日志"
else
    echo ""
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi
