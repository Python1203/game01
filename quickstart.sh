#!/bin/bash

# Stock/Crypto/Casino 自动化系统 - 快速初始化脚本
# 使用方法：./quickstart.sh

set -e

echo "🚀 Stock/Crypto/Casino 自动化系统 - 快速初始化"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python
echo "📋 检查环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 版本：$(python3 --version)${NC}"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 pip3${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Pip 已安装${NC}"
echo ""

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install -r requirements.txt
echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# 创建 .env 文件
echo "⚙️  配置环境变量..."
if [ -f .env ]; then
    echo -e "${YELLOW}⚠️  .env 文件已存在，跳过${NC}"
else
    cp .env.example .env
    echo -e "${GREEN}✓ 已创建 .env 文件${NC}"
    echo ""
    echo -e "${YELLOW}📝 请编辑 .env 文件，填入以下信息:${NC}"
    echo "   1. OPENAI_API_KEY - 你的 OpenAI API Key"
    echo "   2. AFFILIATE_LINKS - 你的推广链接"
    echo "   3. (可选) ALPHA_VANTAGE_KEY - Alpha Vantage API Key"
    echo ""
    read -p "按回车键继续..."
fi
echo ""

# Git 初始化
echo "🔧 初始化 Git 仓库..."
if [ -d .git ]; then
    echo -e "${YELLOW}⚠️  Git 仓库已存在，跳过${NC}"
else
    git init
    git add .
    git commit -m "Initial commit: Stock/Crypto/Casino 自动化系统"
    echo -e "${GREEN}✓ Git 仓库初始化完成${NC}"
fi
echo ""

# 本地测试
echo "🧪 运行本地测试..."
read -p "是否运行本地测试？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if python3 test_local.py; then
        echo -e "${GREEN}✓ 测试通过!${NC}"
    else
        echo -e "${RED}❌ 测试失败，请检查配置${NC}"
        exit 1
    fi
fi
echo ""

# 部署指导
echo "🎉 初始化完成!"
echo ""
echo "================================================"
echo "📋 下一步操作:"
echo "================================================"
echo ""
echo "1️⃣  在 GitHub 创建新仓库"
echo "   访问：https://github.com/new"
echo ""
echo "2️⃣  关联远程仓库并推送"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "   git push -u origin main"
echo ""
echo "3️⃣  部署到 Vercel"
echo "   访问：https://vercel.com/new"
echo "   导入你的 GitHub 仓库"
echo ""
echo "4️⃣  配置环境变量 (在 Vercel)"
echo "   - OPENAI_API_KEY"
echo "   - AFFILIATE_LINKS"
echo ""
echo "5️⃣  配置自动触发"
echo "   - 获取 Vercel Deploy Hook URL"
echo "   - 添加到 GitHub Secrets: VERCEL_DEPLOY_HOOK"
echo ""
echo "📚 详细文档:"
echo "   - README.md - 完整说明"
echo "   - DEPLOY_GUIDE.md - 5 分钟快速部署"
echo "   - docs/ARCHITECTURE.md - 架构设计文档"
echo ""
echo "================================================"
echo -e "${GREEN}✨ 祝您使用愉快！${NC}"
echo "================================================"
