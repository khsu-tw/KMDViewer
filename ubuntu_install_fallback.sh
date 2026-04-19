#!/bin/bash

#########################################################################
#         MDViewer Ubuntu 安装脚本 (自动降级版本)                       #
#########################################################################
#
# 如果 libpango 安装失败，自动降级到最小依赖版本
# 用途: bash ubuntu_install_fallback.sh
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
if [ ! -f "requirements.txt" ]; then
    print_error "请在 MDViewer 项目目录中运行此脚本"
    exit 1
fi

print_header "MDViewer Ubuntu 自动安装 (带自动降级)"

# 检查系统
print_info "检查系统环境..."
if ! command -v python3 &> /dev/null; then
    print_error "未找到 Python 3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "  $PYTHON_VERSION"

# 更新包列表
print_header "更新包列表"
echo "执行: sudo apt-get update"
if sudo apt-get update -qq 2>/dev/null; then
    print_success "包列表已更新"
else
    print_warning "包列表更新出现问题，继续..."
fi

# 尝试安装完整依赖 (包括 weasyprint)
print_header "尝试完整安装"

INSTALL_MODE="full"

echo "第一步: 安装基础依赖..."
BASIC_DEPS=(
    "python3-dev"
    "python3-pip"
    "python3-venv"
    "python3-pyqt5"
    "python3-pyqt5.qtwebengine"
    "build-essential"
    "libssl-dev"
    "libffi-dev"
)

for dep in "${BASIC_DEPS[@]}"; do
    if ! sudo apt-get install -y "$dep" > /dev/null 2>&1; then
        print_warning "  安装 $dep 时出现问题"
    else
        echo "  ✓ $dep"
    fi
done

print_success "基础依赖安装完成"

# 尝试安装 Pango 相关库
print_header "尝试安装 Pango 相关库"

PANGO_DEPS=(
    "libpango1.0-0"
    "libpango1.0-dev"
    "libcairo2"
    "libcairo2-dev"
    "libgdk-pixbuf2.0-0"
)

PANGO_SUCCESS=true
for dep in "${PANGO_DEPS[@]}"; do
    if sudo apt-get install -y "$dep" > /dev/null 2>&1; then
        echo "  ✓ $dep"
    else
        print_warning "  ✗ $dep (不可用)"
        PANGO_SUCCESS=false
    fi
done

if [ "$PANGO_SUCCESS" = true ]; then
    print_success "所有 Pango 库安装成功 - 将使用完整模式"
    INSTALL_MODE="full"
else
    print_warning "部分 Pango 库不可用 - 将使用最小依赖模式"
    INSTALL_MODE="minimal"
fi

# 创建虚拟环境
print_header "创建 Python 虚拟环境"

if [ -d "venv" ]; then
    print_warning "虚拟环境已存在，删除并重建..."
    rm -rf venv
fi

if python3 -m venv venv; then
    print_success "虚拟环境创建成功"
    source venv/bin/activate
else
    print_error "虚拟环境创建失败"
    exit 1
fi

# 升级 pip
print_header "升级 pip"
pip install --upgrade pip setuptools wheel -q || print_warning "pip 升级出现问题"

# 安装 Python 依赖
print_header "安装 Python 依赖 (模式: $INSTALL_MODE)"

if [ "$INSTALL_MODE" = "full" ]; then
    echo "使用完整依赖: requirements.txt"
    if pip install -r requirements.txt -q; then
        print_success "完整依赖安装成功"
    else
        print_warning "完整依赖安装失败，尝试最小模式..."
        INSTALL_MODE="minimal"
    fi
fi

if [ "$INSTALL_MODE" = "minimal" ]; then
    echo "使用最小依赖: requirements_minimal.txt"
    if [ ! -f "requirements_minimal.txt" ]; then
        print_warning "创建最小依赖文件..."
        cat > requirements_minimal.txt << 'EOF'
PyQt5==5.15.9
PyQt5-sip==12.13.0
markdown-it-py==3.0.0
mdit-py-plugins==0.4.0
pygments==2.17.2
Pillow==10.1.0
reportlab==4.0.4
EOF
    fi

    if pip install -r requirements_minimal.txt -q; then
        print_success "最小依赖安装成功"
    else
        print_error "最小依赖安装也失败了"
        exit 1
    fi
fi

# 测试安装
print_header "测试安装"

TEST_OK=true

# 测试 PyQt5
if python -c "from PyQt5.QtWidgets import QApplication; print('  ✓ PyQt5')" 2>/dev/null; then
    :
else
    print_error "  ✗ PyQt5 导入失败"
    TEST_OK=false
fi

# 测试 markdown-it
if python -c "from markdown_it import MarkdownIt; print('  ✓ markdown-it-py')" 2>/dev/null; then
    :
else
    print_error "  ✗ markdown-it-py 导入失败"
    TEST_OK=false
fi

# 测试 PDF 库
if [ "$INSTALL_MODE" = "full" ]; then
    if python -c "from weasyprint import HTML; print('  ✓ weasyprint')" 2>/dev/null; then
        echo "  PDF 模式: weasyprint (完整功能)"
    elif python -c "from reportlab.pdfgen import canvas; print('  ✓ reportlab')" 2>/dev/null; then
        echo "  PDF 模式: reportlab (简化功能)"
    else
        print_warning "  ⚠️  未找到 PDF 库，将禁用 PDF 导出"
    fi
else
    if python -c "from reportlab.pdfgen import canvas; print('  ✓ reportlab')" 2>/dev/null; then
        echo "  PDF 模式: reportlab (简化功能)"
    else
        print_warning "  ⚠️  未找到 PDF 库，将禁用 PDF 导出"
    fi
fi

if [ "$TEST_OK" = false ]; then
    print_error "某些模块测试失败"
    exit 1
fi

print_success "所有测试通过"

# 显示使用说明
print_header "安装完成！"

echo ""
if [ "$INSTALL_MODE" = "full" ]; then
    echo "✓ 完整模式安装"
    echo "  - 所有功能可用"
    echo "  - PDF 导出: weasyprint (完整功能)"
else
    echo "⚠️  最小模式安装"
    echo "  - 核心功能正常"
    echo "  - PDF 导出: reportlab (简化功能，仅文本)"
    echo "  - 如要升级到完整模式，查看 INSTALL_WITHOUT_LIBPANGO.md"
fi

echo ""
echo "下一步操作:"
echo "1️⃣  虚拟环境已激活，直接运行应用:"
echo "   python src/main.py"
echo ""
echo "2️⃣  或验证环境:"
echo "   python3 check_env.py"
echo ""
echo "📚 文档:"
echo "   • 快速开始: QUICK_START_UBUNTU.md"
echo "   • 完整指南: UBUNTU_SETUP.md"
echo "   • 最小安装: INSTALL_WITHOUT_LIBPANGO.md"
echo ""

print_success "MDViewer 已准备就绪！"
