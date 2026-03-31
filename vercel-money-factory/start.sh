#!/bin/bash

echo "🚀 Astro Money Factory - 本地开发环境启动"
echo "=========================================="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

# 安装 Python 依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install -r requirements.txt

# 运行内容生成脚本
echo ""
echo "🤖 运行内容生成脚本..."
python3 build_content.py

# 安装 Node 依赖
echo ""
echo "📦 安装 Node 依赖..."
npm install

# 启动开发服务器
echo ""
echo "🌐 启动开发服务器..."
echo "访问地址：http://localhost:4321"
echo "按 Ctrl+C 停止服务"
echo ""
npm run dev
