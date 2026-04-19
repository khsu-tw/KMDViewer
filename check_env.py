#!/usr/bin/env python3

"""
MDViewer 环境检测工具
检查系统是否满足运行 MDViewer 的要求
"""

import sys
import os
from pathlib import Path

class Colors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    INFO = '\033[94m'
    END = '\033[0m'


def check_python_version():
    """检查 Python 版本"""
    print(f"\n{Colors.INFO}检查 Python 版本...{Colors.END}")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"  Python 版本: {version_str}")

    if version < (3, 10):
        print(f"  {Colors.FAIL}✗ 需要 Python 3.10 或更高版本{Colors.END}")
        return False
    else:
        print(f"  {Colors.OK}✓ 版本满足要求{Colors.END}")
        return True


def check_project_files():
    """检查项目文件"""
    print(f"\n{Colors.INFO}检查项目文件...{Colors.END}")

    required_files = [
        "src/main.py",
        "src/core/markdown_processor.py",
        "src/core/pdf_exporter.py",
        "src/core/file_manager.py",
        "src/ui/main_window.py",
        "src/ui/preview_viewer.py",
        "requirements.txt",
        "setup.py",
    ]

    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  {Colors.OK}✓ {file_path}{Colors.END}")
        else:
            print(f"  {Colors.FAIL}✗ {file_path} (缺失){Colors.END}")
            all_exist = False

    return all_exist


def check_python_packages():
    """检查 Python 包"""
    print(f"\n{Colors.INFO}检查 Python 包...{Colors.END}")

    packages = [
        "PyQt5",
        "markdown_it",
        "pygments",
        "weasyprint",
        "PIL",
    ]

    installed_packages = []
    missing_packages = []

    for package in packages:
        try:
            __import__(package)
            installed_packages.append(package)
            print(f"  {Colors.OK}✓ {package}{Colors.END}")
        except ImportError:
            missing_packages.append(package)
            print(f"  {Colors.FAIL}✗ {package} (未安装){Colors.END}")

    if missing_packages:
        print(f"\n  {Colors.WARNING}缺失的包: {', '.join(missing_packages)}{Colors.END}")
        print(f"  {Colors.INFO}运行以下命令安装:{Colors.END}")
        print(f"  pip install -r requirements.txt")

    return len(missing_packages) == 0


def check_system_packages():
    """检查系统包 (仅信息用)"""
    print(f"\n{Colors.INFO}检查系统环境...{Colors.END}")

    # 检查 Ubuntu
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            content = f.read()
            if "Ubuntu" in content:
                for line in content.split('\n'):
                    if "VERSION=" in line:
                        version = line.split('=')[1].strip('"')
                        print(f"  {Colors.OK}✓ Ubuntu {version}{Colors.END}")
                        return True
    else:
        print(f"  {Colors.WARNING}! 非 Ubuntu 系统{Colors.END}")

    return True


def check_display():
    """检查显示服务器"""
    print(f"\n{Colors.INFO}检查显示服务器...{Colors.END}")

    if "DISPLAY" in os.environ or "WAYLAND_DISPLAY" in os.environ:
        display = os.environ.get("DISPLAY", os.environ.get("WAYLAND_DISPLAY", "unknown"))
        print(f"  {Colors.OK}✓ 显示服务器: {display}{Colors.END}")
        return True
    else:
        print(f"  {Colors.WARNING}! 未检测到显示服务器{Colors.END}")
        print(f"  {Colors.INFO}  (如果通过 SSH 连接，使用 ssh -X user@host){Colors.END}")
        return False


def main():
    """主函数"""
    print(f"\n{Colors.INFO}{'='*50}{Colors.END}")
    print(f"{Colors.INFO}MDViewer 环境检测工具{Colors.END}")
    print(f"{Colors.INFO}{'='*50}{Colors.END}")

    checks = [
        ("Python 版本", check_python_version),
        ("项目文件", check_project_files),
        ("系统环境", check_system_packages),
        ("显示服务器", check_display),
        ("Python 包", check_python_packages),
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"  {Colors.WARNING}! 检查出错: {str(e)}{Colors.END}")
            results[name] = False

    # 总结
    print(f"\n{Colors.INFO}{'='*50}{Colors.END}")
    print(f"{Colors.INFO}检查总结{Colors.END}")
    print(f"{Colors.INFO}{'='*50}{Colors.END}\n")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    for name, result in results.items():
        status = f"{Colors.OK}✓ 通过{Colors.END}" if result else f"{Colors.FAIL}✗ 未通过{Colors.END}"
        print(f"  {name}: {status}")

    print()

    if passed == total:
        print(f"{Colors.OK}{'='*50}{Colors.END}")
        print(f"{Colors.OK}✓ 所有检查通过！可以运行 MDViewer{Colors.END}")
        print(f"{Colors.OK}{'='*50}{Colors.END}\n")
        print(f"运行应用:")
        print(f"  python src/main.py\n")
        return 0
    else:
        print(f"{Colors.FAIL}{'='*50}{Colors.END}")
        print(f"{Colors.FAIL}✗ 部分检查未通过{Colors.END}")
        print(f"{Colors.FAIL}{'='*50}{Colors.END}\n")
        print(f"请查看上面的错误信息并按照提示修复。\n")
        print(f"快速帮助:")
        print(f"  1. 查看 QUICK_START_UBUNTU.md")
        print(f"  2. 运行 bash ubuntu_install.sh")
        print(f"  3. 或查看 UBUNTU_SETUP.md 了解详细步骤\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
