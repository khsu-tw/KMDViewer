#!/usr/bin/env python3

"""
MDViewer Ubuntu 安装程序
用途: 在 Ubuntu 系统上自动安装和配置 MDViewer
使用: python3 ubuntu_install.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 颜色定义
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """打印标题"""
    print(f"\n{Colors.OKBLUE}{'='*50}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'='*50}{Colors.ENDC}\n")


def print_success(text):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_error(text):
    """打印错误信息"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_info(text):
    """打印信息"""
    print(f"{Colors.WARNING}ℹ️  {text}{Colors.ENDC}")


def print_step(text):
    """打印步骤"""
    print(f"{Colors.OKCYAN}→ {text}{Colors.ENDC}")


def run_command(cmd, description="", show_output=False):
    """运行系统命令"""
    try:
        if show_output:
            print_step(description)
            result = subprocess.run(cmd, shell=True, check=True)
            return result.returncode == 0
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
            return result.returncode == 0
    except Exception as e:
        print_error(f"命令执行失败: {str(e)}")
        return False


def check_system():
    """检查系统环境"""
    print_header("系统环境检查")

    # 检查 Python 版本
    if sys.version_info < (3, 10):
        print_error(f"Python 版本过低 ({sys.version})")
        print_info("需要 Python 3.10 或更高版本")
        return False
    print_success(f"Python 版本: {sys.version.split()[0]}")

    # 检查 Ubuntu
    if not os.path.exists("/etc/os-release"):
        print_error("无法识别操作系统")
        return False

    with open("/etc/os-release") as f:
        os_info = f.read()
        if "Ubuntu" not in os_info and "ubuntu" not in os_info:
            print_error("此脚本仅支持 Ubuntu")
            return False

    if "22.04" in os_info or "20.04" in os_info or "24.04" in os_info:
        print_success("检测到 Ubuntu LTS 版本")
    else:
        print_info("检测到 Ubuntu 版本")

    # 检查必要的命令
    commands = ["git", "pip3", "python3"]
    for cmd in commands:
        if shutil.which(cmd):
            print_success(f"找到: {cmd}")
        else:
            print_info(f"未找到: {cmd} (部分功能可能不可用)")

    return True


def install_system_deps():
    """安装系统依赖"""
    print_header("安装系统依赖")

    print_info("需要 sudo 权限来安装系统包")
    print_info("将要安装以下包：")
    print("  • Python 开发工具")
    print("  • PyQt5 和 WebEngine")
    print("  • 构建工具")
    print("  • 图形库 (Cairo, Pango)")

    # 检查是否可以不输入密码运行 sudo
    if not run_command("sudo -n true 2>/dev/null", "", False):
        print_info("您可能需要输入密码")

    # 更新包列表
    print_step("更新包列表...")
    if not run_command("sudo apt-get update -qq", "", False):
        print_error("apt-get update 失败")
        return False

    # 安装依赖
    deps = [
        "python3-dev",
        "python3-pip",
        "python3-venv",
        "python3-pyqt5",
        "python3-pyqt5.qtwebengine",
        "build-essential",
        "libssl-dev",
        "libffi-dev",
        "libpango1.0-0",
        "libpango1.0-dev",
        "libcairo2",
        "libcairo2-dev",
        "libgdk-pixbuf2.0-0",
    ]

    print_step("安装依赖包...")
    for dep in deps:
        if run_command(f"dpkg -l | grep -q '^ii.*{dep}'", "", False):
            print(f"  ✓ {dep} (已安装)")
        else:
            result = run_command(f"sudo apt-get install -y {dep}", "", False)
            if result:
                print(f"  ✓ {dep} (已安装)")
            else:
                print_error(f"  ✗ {dep} (安装失败)")

    print_success("系统依赖安装完成")
    return True


def create_venv():
    """创建虚拟环境"""
    print_header("创建 Python 虚拟环境")

    venv_path = Path("venv")

    if venv_path.exists():
        print_info("虚拟环境已存在")
        return True

    print_step("创建虚拟环境...")
    if not run_command("python3 -m venv venv", "Creating virtual environment...", False):
        print_error("虚拟环境创建失败")
        return False

    print_success("虚拟环境创建完成")
    return True


def install_python_deps():
    """安装 Python 依赖"""
    print_header("安装 Python 依赖")

    # 确定 Python 可执行文件路径
    if os.path.exists("venv/bin/python"):
        python_exe = "venv/bin/python"
        pip_exe = "venv/bin/pip"
    else:
        python_exe = "python3"
        pip_exe = "pip3"

    # 升级 pip
    print_step("升级 pip...")
    if not run_command(f"{pip_exe} install --upgrade pip setuptools wheel -q", "", False):
        print_warning("pip 升级可能失败，继续安装...")

    # 安装依赖
    print_step("安装项目依赖 (这可能需要几分钟)...")
    if not run_command(f"{pip_exe} install -r requirements.txt -q", "", False):
        print_error("Python 依赖安装失败")
        print_info("请检查网络连接或运行:")
        print(f"  {pip_exe} install -r requirements.txt")
        return False

    print_success("Python 依赖安装完成")

    # 显示已安装的包
    print_step("已安装的包版本:")
    packages = ["PyQt5", "markdown-it-py", "weasyprint", "Pillow", "pygments"]
    for pkg in packages:
        run_command(f"{pip_exe} show {pkg} | grep Version", "", False)

    return True


def test_installation():
    """测试安装"""
    print_header("测试安装")

    if os.path.exists("venv/bin/python"):
        python_exe = "venv/bin/python"
    else:
        python_exe = "python3"

    tests = [
        ("src.core.markdown_processor", "MarkdownProcessor"),
        ("src.core.pdf_exporter", "PDFExporter"),
        ("PyQt5.QtWidgets", "PyQt5"),
    ]

    for module, name in tests:
        cmd = f"{python_exe} -c \"from {module} import *; print('  ✓ {name}')\" 2>/dev/null"
        if run_command(cmd, "", False):
            print(f"  ✓ {name}")
        else:
            print_error(f"  ✗ {name} 导入失败")
            return False

    print_success("所有模块导入成功")
    return True


def show_usage():
    """显示使用说明"""
    print_header("安装完成！")

    print("下一步操作:\n")
    print("1️⃣  激活虚拟环境:")
    print("   source venv/bin/activate\n")
    print("2️⃣  运行应用:")
    print("   python src/main.py\n")
    print("📚 更多信息:")
    print("   • README.md - 功能说明")
    print("   • UBUNTU_SETUP.md - 详细配置")
    print("   • DEVELOPMENT.md - 开发指南\n")
    print("⌨️  快速参考:")
    print("   Ctrl+O - 打开文件")
    print("   Ctrl+E - 导出 PDF")
    print("   F5 - 刷新预览")
    print("   Ctrl+Q - 退出应用\n")
    print_success("MDViewer 已准备就绪！")


def main():
    """主函数"""
    print_header("MDViewer - Ubuntu 安装程序")

    # 检查是否在项目目录
    if not Path("requirements.txt").exists():
        print_error("请在 MDViewer 项目目录中运行此脚本")
        sys.exit(1)

    # 执行安装步骤
    steps = [
        ("系统检查", check_system),
        ("安装系统依赖", install_system_deps),
        ("创建虚拟环境", create_venv),
        ("安装 Python 依赖", install_python_deps),
        ("测试安装", test_installation),
    ]

    for step_name, step_func in steps:
        try:
            if not step_func():
                print_error(f"{step_name} 失败")
                print_info("请查看 UBUNTU_SETUP.md 中的故障排查部分")
                sys.exit(1)
        except KeyboardInterrupt:
            print_error("\n安装被中断")
            sys.exit(1)
        except Exception as e:
            print_error(f"{step_name} 出错: {str(e)}")
            sys.exit(1)

    show_usage()


if __name__ == "__main__":
    main()
