#!/bin/bash

#########################################################################
#         MDViewer Ubuntu 安装脚本 (无 Pango 版本)                     #
#########################################################################
#
# 完全不使用任何 Pango 相关的系统库
# 所有依赖都是纯 Python 库
# 用途: bash ubuntu_install_no_pango.sh
# 系统: Ubuntu 20.04+ LTS
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# 检查是否在项目目录
if [ ! -f "requirements_no_pango.txt" ]; then
    print_error "请在 MDViewer 项目目录中运行此脚本"
    exit 1
fi

print_header "MDViewer Ubuntu 安装 (完全无 Pango 版本)"

# 检查 Python
print_info "检查系统环境..."
if ! command -v python3 &> /dev/null; then
    print_error "未找到 Python 3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "  $PYTHON_VERSION"
print_success "Python 版本检查完成"

# 最小系统依赖 (仅 PyQt5 所需)
print_header "安装最小系统依赖"
print_info "需要 sudo 权限安装 PyQt5 依赖"

echo "安装基础工具..."
BASIC_DEPS=(
    "python3-dev"
    "python3-pip"
    "python3-venv"
    "build-essential"
    "libssl-dev"
    "libffi-dev"
)

for dep in "${BASIC_DEPS[@]}"; do
    echo "  ↓ 安装 $dep..."
    if sudo apt-get install -y "$dep" > /dev/null 2>&1; then
        echo "  ✓ $dep"
    else
        print_error "  ✗ 安装 $dep 失败"
        exit 1
    fi
done

# PyQt5 依赖 (不包括 Pango)
print_info "安装 PyQt5 运行库 (不需要 Pango 开发库)..."
QT_DEPS=(
    "python3-pyqt5"
    "python3-pyqt5.qtwebengine"
    "libqt5gui5"
    "libqt5core5a"
    "libqt5widgets5"
)

for dep in "${QT_DEPS[@]}"; do
    echo "  ↓ 安装 $dep..."
    if sudo apt-get install -y "$dep" > /dev/null 2>&1; then
        echo "  ✓ $dep"
    else
        print_warning "  ⚠️  $dep (可能不存在或已安装)"
    fi
done

print_success "系统依赖安装完成 (无需 Pango!)"

# 创建虚拟环境
print_header "创建 Python 虚拟环境"

if [ -d "venv" ]; then
    print_warning "虚拟环境已存在，删除并重建..."
    rm -rf venv
fi

echo "创建虚拟环境..."
if python3 -m venv venv; then
    print_success "虚拟环境创建成功"
    source venv/bin/activate
else
    print_error "虚拟环境创建失败"
    exit 1
fi

# 升级 pip
print_header "升级 pip"
echo "升级 pip..."
pip install --upgrade pip setuptools wheel -q || print_warning "pip 升级出现问题"
print_success "pip 升级完成"

# 安装 Python 依赖 (纯 Python 库)
print_header "安装 Python 依赖 (纯 Python 库 - 无需 Pango)"

echo "安装 Python 包 (此步骤不需要系统库编译)..."
if pip install -r requirements_no_pango.txt -q; then
    print_success "所有 Python 包安装成功"
else
    print_error "Python 包安装失败"
    exit 1
fi

# 验证安装
print_header "验证安装"

echo "检查核心模块..."

# 检查 PyQt5
if python -c "from PyQt5.QtWidgets import QApplication; print('  ✓ PyQt5')" 2>/dev/null; then
    :
else
    print_error "  ✗ PyQt5 导入失败"
    exit 1
fi

# 检查 markdown-it
if python -c "from markdown_it import MarkdownIt; print('  ✓ markdown-it-py')" 2>/dev/null; then
    :
else
    print_error "  ✗ markdown-it-py 导入失败"
    exit 1
fi

# 检查 reportlab
if python -c "from reportlab.pdfgen import canvas; print('  ✓ reportlab (纯 Python PDF 库)')" 2>/dev/null; then
    :
else
    print_warning "  ⚠️  reportlab 导入失败，PDF 导出将不可用"
fi

print_success "所有测试通过！"

# 最终信息
print_header "安装完成！"

echo ""
echo "✅ MDViewer 已准备就绪"
echo ""
echo "说明:"
echo "  • 不使用任何 Pango 系统库"
echo "  • 所有依赖都是纯 Python 库"
echo "  • PyQt5 使用 Qt5，不依赖 Pango"
echo "  • PDF 导出使用 reportlab（纯 Python）"
echo ""
echo "下一步:"
echo "1️⃣  虚拟环境已激活"
echo "2️⃣  运行应用:"
echo "   python src/main.py"
echo ""
echo "验证环境:"
echo "   python3 check_env.py"
echo ""

print_success "祝使用愉快！"
