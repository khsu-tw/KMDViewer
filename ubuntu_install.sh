#!/bin/bash

#########################################################################
#                    MDViewer Ubuntu 一键安装脚本                        #
#########################################################################
#
# 用途: 在 Ubuntu 系统上自动安装 MDViewer
# 使用: bash ubuntu_install.sh
# 系统: Ubuntu 20.04+ LTS
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
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

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# 检查 Ubuntu 版本
check_ubuntu() {
    print_header "检查系统环境"

    if ! command -v lsb_release &> /dev/null; then
        print_error "无法检测 Ubuntu 版本"
        return 1
    fi

    UBUNTU_VERSION=$(lsb_release -rs)
    echo "Ubuntu 版本: $UBUNTU_VERSION"

    if ! command -v python3 &> /dev/null; then
        print_error "未找到 Python 3"
        return 1
    fi

    PYTHON_VERSION=$(python3 --version)
    echo "Python 版本: $PYTHON_VERSION"
    print_success "系统检查通过"
}

# 安装系统依赖
install_system_deps() {
    print_header "安装系统依赖"

    print_info "需要输入密码来安装系统包..."

    echo "执行: sudo apt-get update"
    sudo apt-get update -qq || {
        print_error "apt-get update 失败"
        return 1
    }

    echo "正在安装依赖包..."

    DEPS_TO_INSTALL=(
        "python3-dev"
        "python3-pip"
        "python3-venv"
        "python3-pyqt5"
        "python3-pyqt5.qtwebengine"
        "build-essential"
        "libssl-dev"
        "libffi-dev"
        "libpango1.0-0"
        "libpango1.0-dev"
        "libcairo2"
        "libcairo2-dev"
        "libgdk-pixbuf2.0-0"
    )

    for package in "${DEPS_TO_INSTALL[@]}"; do
        if dpkg -l | grep -q "^ii.*$package"; then
            echo "  ✓ $package (已安装)"
        else
            echo "  ↓ 安装 $package..."
            sudo apt-get install -y "$package" > /dev/null 2>&1 || {
                print_error "安装 $package 失败"
                return 1
            }
        fi
    done

    print_success "系统依赖安装完成"
}

# 创建虚拟环境
create_venv() {
    print_header "创建 Python 虚拟环境"

    if [ -d "venv" ]; then
        print_info "虚拟环境已存在，跳过..."
        return 0
    fi

    echo "创建虚拟环境..."
    python3 -m venv venv || {
        print_error "虚拟环境创建失败"
        return 1
    }

    print_success "虚拟环境创建完成"
}

# 安装 Python 依赖
install_python_deps() {
    print_header "安装 Python 依赖"

    echo "激活虚拟环境..."
    source venv/bin/activate || {
        print_error "虚拟环境激活失败"
        return 1
    }

    echo "升级 pip..."
    pip install --upgrade pip setuptools wheel -q || {
        print_error "pip 升级失败"
        return 1
    }

    echo "安装项目依赖 (这可能需要几分钟)..."
    pip install -r requirements.txt -q || {
        print_error "Python 依赖安装失败"
        return 1
    }

    print_success "Python 依赖安装完成"

    # 显示已安装的包版本
    echo ""
    echo "已安装的包版本:"
    pip list | grep -E "PyQt5|markdown-it|weasyprint|Pillow" || true
}

# 构建可执行档 (可选)
build_executable() {
    print_header "构建独立可执行档 (可选)"

    read -p "是否构建独立可执行档? (y/n) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "安装 PyInstaller..."
        source venv/bin/activate
        pip install pyinstaller -q || {
            print_error "PyInstaller 安装失败"
            return 1
        }

        echo "构建可执行档 (这可能需要 2-3 分钟)..."
        python -m PyInstaller MDViewer.spec || {
            print_error "构建失败"
            return 1
        }

        print_success "可执行档构建完成: ./dist/MDViewer"

        # 创建应用快捷方式
        read -p "是否创建应用菜单快捷方式? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            create_desktop_shortcut
        fi
    fi
}

# 创建桌面快捷方式
create_desktop_shortcut() {
    INSTALL_DIR=$(pwd)
    DESKTOP_FILE="$HOME/.local/share/applications/mdviewer.desktop"

    mkdir -p "$HOME/.local/share/applications"

    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Name=MDViewer
Exec=$INSTALL_DIR/dist/MDViewer
Icon=accessories-text-editor
Type=Application
Categories=Office;WordProcessor;Utility;
Comment=A Markdown Viewer with PDF export
Terminal=false
EOF

    chmod +x "$DESKTOP_FILE"
    update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

    print_success "应用快捷方式已创建"
    print_info "可从应用菜单启动 MDViewer"
}

# 测试安装
test_installation() {
    print_header "测试安装"

    source venv/bin/activate

    echo "测试 Python 模块导入..."

    python -c "from src.core.markdown_processor import MarkdownProcessor; print('  ✓ MarkdownProcessor')" || {
        print_error "MarkdownProcessor 导入失败"
        return 1
    }

    python -c "from src.core.pdf_exporter import PDFExporter; print('  ✓ PDFExporter')" || {
        print_error "PDFExporter 导入失败"
        return 1
    }

    python -c "from PyQt5.QtWidgets import QApplication; print('  ✓ PyQt5')" || {
        print_error "PyQt5 导入失败"
        return 1
    }

    print_success "所有模块导入成功"
}

# 显示使用说明
show_usage() {
    print_header "安装完成！"

    echo ""
    echo "下一步操作:"
    echo ""
    echo "1️⃣  激活虚拟环境:"
    echo "   source venv/bin/activate"
    echo ""
    echo "2️⃣  运行应用:"
    echo "   python src/main.py"
    echo ""

    if [ -f "dist/MDViewer" ]; then
        echo "3️⃣  或运行可执行档:"
        echo "   ./dist/MDViewer"
        echo ""
    fi

    echo "📚 更多信息:"
    echo "   - 查看 README.md 了解功能说明"
    echo "   - 查看 UBUNTU_SETUP.md 了解详细配置"
    echo "   - 查看 DEVELOPMENT.md 了解开发指南"
    echo ""
    echo "⌨️  快速参考:"
    echo "   Ctrl+O - 打开文件"
    echo "   Ctrl+E - 导出 PDF"
    echo "   F5     - 刷新预览"
    echo "   Ctrl+Q - 退出应用"
    echo ""
    print_success "MDViewer 已准备就绪！"
}

# 错误处理
error_exit() {
    print_error "$1"
    echo ""
    echo "故障排查:"
    echo "1. 确保运行的是 Ubuntu 20.04 或更新版本"
    echo "2. 检查网络连接"
    echo "3. 查看 UBUNTU_SETUP.md 的故障排查部分"
    exit 1
}

# 主函数
main() {
    print_header "MDViewer - Ubuntu 自动安装程序"

    # 检查是否在项目目录
    if [ ! -f "requirements.txt" ]; then
        error_exit "请在 MDViewer 项目目录中运行此脚本"
    fi

    # 执行各个步骤
    check_ubuntu || error_exit "系统检查失败"
    install_system_deps || error_exit "系统依赖安装失败"
    create_venv || error_exit "虚拟环境创建失败"
    install_python_deps || error_exit "Python 依赖安装失败"
    test_installation || error_exit "安装测试失败"
    build_executable
    show_usage
}

# 运行主函数
main
