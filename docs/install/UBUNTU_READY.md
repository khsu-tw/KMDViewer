# ✅ MDViewer - Ubuntu 就绪指南

MDViewer 已完全准备好在 Ubuntu 系统上使用！本文档总结了在 Ubuntu 上安装和使用 MDViewer 的最佳方式。

## 📋 目录

1. [快速开始](#快速开始)
2. [三种安装方式](#三种安装方式)
3. [验证安装](#验证安装)
4. [常见问题](#常见问题)
5. [后续步骤](#后续步骤)

## 🚀 快速开始

最快的启动方式（需要 5 分钟）：

```bash
# 1. 进入项目目录
cd ~/MDViewer

# 2. 运行自动安装脚本 (会要求输入密码)
bash ubuntu_install.sh

# 3. 脚本完成后，运行应用
source venv/bin/activate
python src/main.py
```

应用窗口将打开！

---

## 三种安装方式

### 方式 1: 自动安装 (⭐ 推荐)

最简单、最快速、最可靠。

**使用 Bash 脚本**:
```bash
bash ubuntu_install.sh
```

**或使用 Python 脚本**:
```bash
python3 ubuntu_install.py
```

**优点**:
- ✅ 自动检查系统
- ✅ 自动安装依赖
- ✅ 自动创建虚拟环境
- ✅ 自动验证安装
- ✅ 支持可执行档生成
- ✅ 支持应用菜单集成

**缺点**:
- 需要 sudo 密码

---

### 方式 2: 手动安装 (用于调试)

如果自动脚本失败，按步骤手动操作。

#### 步骤 1: 安装系统包

```bash
# 一条命令安装所有依赖
sudo apt-get update && sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  libpango1.0-0 libpango1.0-dev \
  libcairo2 libcairo2-dev libgdk-pixbuf2.0-0
```

#### 步骤 2: 虚拟环境

```bash
cd ~/MDViewer
python3 -m venv venv
source venv/bin/activate
```

#### 步骤 3: 安装 Python 包

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 步骤 4: 运行应用

```bash
python src/main.py
```

**优点**:
- ✅ 完全控制过程
- ✅ 易于调试
- ✅ 了解依赖关系

**缺点**:
- ✗ 步骤较多
- ✗ 容易出错

---

### 方式 3: 容器化 (用于分发)

使用 Docker 创建独立环境。

**创建 Dockerfile**:
```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3-dev python3-pip python3-venv \
    python3-pyqt5 python3-pyqt5.qtwebengine \
    build-essential libssl-dev libffi-dev \
    libpango1.0-0 libpango1.0-dev \
    libcairo2 libcairo2-dev

WORKDIR /app
COPY . .

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt

ENV DISPLAY=:0
CMD ["bash", "-c", "source venv/bin/activate && python src/main.py"]
```

**运行容器**:
```bash
docker build -t mdviewer .
docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix mdviewer
```

**优点**:
- ✅ 完全隔离
- ✅ 易于分发
- ✅ 跨系统一致

**缺点**:
- ✗ 需要 Docker
- ✗ 性能开销
- ✗ X11 配置复杂

---

## ✅ 验证安装

### 方式 1: 环境检查脚本

```bash
python3 check_env.py
```

这将检查：
- ✓ Python 版本
- ✓ 项目文件
- ✓ 系统环境
- ✓ 显示服务器
- ✓ 所有 Python 包

**预期输出**:
```
✓ Python 版本: 通过
✓ 项目文件: 通过
✓ 系统环境: 通过
✓ 显示服务器: 通过
✓ Python 包: 通过

✓ 所有检查通过！可以运行 MDViewer
```

### 方式 2: 导入测试

```bash
source venv/bin/activate

# 测试核心模块
python -c "from src.core.markdown_processor import MarkdownProcessor; print('✓ OK')"
python -c "from src.core.pdf_exporter import PDFExporter; print('✓ OK')"
python -c "from PyQt5.QtWidgets import QApplication; print('✓ OK')"
```

### 方式 3: 运行应用

```bash
source venv/bin/activate
python src/main.py
```

应用窗口打开即表示成功！

---

## 📱 完整功能验证

打开应用后，验证这些功能：

1. **打开文件** (Ctrl+O)
   - 选择 `test_sample.md`
   - 文件内容应显示在编辑器

2. **查看预览**
   - 编辑内容时预览应实时更新
   - 应看到格式化的 Markdown

3. **导出 PDF** (Ctrl+E)
   - 选择页面设置
   - 保存 PDF 文件
   - PDF 应包含正确的内容

如果这些都正常工作，说明安装完全成功！ ✅

---

## ❓ 常见问题

### Q: 如何升级 MDViewer?

```bash
cd ~/MDViewer
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Q: 如何卸载?

```bash
# 删除项目
rm -rf ~/MDViewer

# 或仅删除虚拟环境
rm -rf ~/MDViewer/venv
```

### Q: 能在树莓派上运行吗?

可以，但需要 Python 3.10+。Raspberry Pi OS 基于 Debian，安装方式类似。

### Q: 能在 WSL (Windows Subsystem for Linux) 上运行吗?

可以，但需要配置 X11 转发。参考 [WSL with GUI 指南](https://docs.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)。

### Q: 可以创建系统范围的快捷方式吗?

可以，安装脚本会提示创建。或手动运行：

```bash
# 创建应用菜单快捷方式
mkdir -p ~/.local/share/applications
INSTALL_DIR=$(pwd)

cat > ~/.local/share/applications/mdviewer.desktop << EOF
[Desktop Entry]
Version=1.0
Name=MDViewer
Exec=$INSTALL_DIR/dist/MDViewer
Icon=accessories-text-editor
Type=Application
Categories=Office;WordProcessor;
Comment=Markdown Viewer with PDF export
Terminal=false
EOF

update-desktop-database ~/.local/share/applications/
```

然后可从应用菜单启动 MDViewer。

### Q: 出现 "Display server not available"?

这通常发生在 SSH 连接中。使用：

```bash
# SSH 连接时启用 X11 转发
ssh -X user@host

# 然后运行
python src/main.py
```

### Q: 应用很慢?

- 关闭其他应用
- 尽量使用较小的文件测试
- 首次启动会较慢（加载库）

### Q: PDF 导出失败?

检查：
```bash
# 验证 weasyprint
python -c "from weasyprint import HTML; print('OK')"

# 查看具体错误
python src/main.py 2>&1 | grep -i error
```

参考 [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md) 的故障排查部分。

---

## 📚 后续步骤

### 立即尝试

1. 打开 `test_sample.md` 查看演示
2. 编辑文本看实时预览
3. 导出为 PDF

### 深入了解

- 📖 [README.md](README.md) - 完整功能说明
- 🚀 [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md) - 快速参考
- 📖 [UBUNTU_SETUP.md](UBUNTU_SETUP.md) - 详细配置指南
- 💻 [DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南

### 进阶使用

- 自定义样式表
- 创建插件
- 贡献代码

---

## 🎯 常用命令速查

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行应用
python src/main.py

# 退出虚拟环境
deactivate

# 检查环境
python3 check_env.py

# 构建可执行档
bash build.sh

# 清理缓存
find . -type d -name __pycache__ -exec rm -r {} +
```

---

## 🎓 系统要求回顾

✅ **已验证的配置**:
- Ubuntu 22.04.3 LTS
- Python 3.10.12
- PyQt5 已安装
- 所有依赖就绪

✅ **系统支持**:
- Ubuntu 20.04 LTS+
- Debian 11+
- Linux Mint
- Pop!_OS
- 其他基于 Debian 的系统

---

## 🔐 安全性说明

MDViewer 是开源应用，所有代码可审计。不包含：
- ❌ 跟踪代码
- ❌ 广告
- ❌ 恶意代码
- ❌ 后门

完全安全、私密、自由。

---

## 📞 需要帮助?

1. **快速问题**: 查看 [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md)
2. **详细问题**: 查看 [UBUNTU_SETUP.md](UBUNTU_SETUP.md)
3. **开发问题**: 查看 [DEVELOPMENT.md](DEVELOPMENT.md)
4. **功能问题**: 查看 [README.md](README.md)

---

## 🚀 准备好了吗?

**现在就开始使用 MDViewer**:

```bash
# 一行命令启动安装
cd ~/MDViewer && bash ubuntu_install.sh
```

或

```bash
# 一行命令运行 (假设已安装)
source venv/bin/activate && python src/main.py
```

祝使用愉快！🎉

---

**版本**: 1.0  
**日期**: 2026-04-16  
**系统**: Ubuntu 20.04+ LTS
