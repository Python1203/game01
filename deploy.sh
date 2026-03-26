#!/bin/bash
# deploy.sh - 自动化部署脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 设置脚本选项
set -e  # 遇到错误时退出
set -u  # 使用未定义变量时退出

# 定义变量
PROJECT_ROOT="/Users/zzw868/PycharmProjects/PythonProject"
CNAME_FILE="$PROJECT_ROOT/CNAME"
OUTPUT_DIR="$PROJECT_ROOT/out"
BRANCH_NAME="gh-pages"

log() {
    echo -e "${GREEN}✅ $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# 主要部署函数
deploy() {
    log "开始自动化部署流程"
    
    # 进入项目根目录
    cd "$PROJECT_ROOT"
    log "进入项目目录：$PROJECT_ROOT"
    
    # 清理之前的构建文件
    if [ -d "$OUTPUT_DIR" ]; then
        rm -rf "$OUTPUT_DIR"
        log "清理之前的构建文件"
    fi
    
    # 构建项目
    info "正在构建项目..."
    export EXPORT=true
    yarn build || error "构建失败"
    log "项目构建完成"
    
    # 清理中文命名的目录（Next.js 静态导出会产生重复的中文和 URL 编码目录）
    # 只保留 URL 编码的目录以避免客户端预取 404 错误
    info "清理冗余的中文目录..."
    python3 "$PROJECT_ROOT/scripts/clean-chinese-dirs.py" "$PROJECT_ROOT"
    log "中文目录清理完成"
    
    # 验证输出目录
    if [ ! -d "$OUTPUT_DIR" ]; then
        error "构建失败：输出目录不存在"
    fi
    
    # 复制CNAME文件
    if [ -f "$CNAME_FILE" ]; then
        cp "$CNAME_FILE" "$OUTPUT_DIR/CNAME"
        log "CNAME文件已配置"
    else
        warn "警告：CNAME文件不存在"
    fi
    
    # 验证关键文件
    if [ ! -f "$OUTPUT_DIR/index.html" ]; then
        error "部署失败：未生成index.html文件"
    fi
    
    log "部署准备就绪"
    echo ""
    info "📌 部署文件位置：$OUTPUT_DIR"
    info "🌐 访问地址：http://869.us.ci"
    echo ""
    
    # 提供部署选项
    cat << EOF
🚀 部署选项：
1. GitHub Pages (推荐):
   git subtree push --prefix=out origin gh-pages

2. 手动部署:
   将 out 目录中的所有文件上传到您的服务器

3. 本地预览:
   npx serve -s out
EOF
}

# 调用主函数
deploy

exit 0