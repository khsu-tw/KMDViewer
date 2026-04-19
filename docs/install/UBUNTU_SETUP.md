# MDViewer - Ubuntu 安装和运行指南

本指南提供了在 Ubuntu 系统上安装和运行 MDViewer 的详细步骤。

## 系统要求

- **操作系统**: Ubuntu 20.04 LTS 或更新版本
- **Python**: 3.10 或更高版本
- **RAM**: 最少 2GB
- **磁盘空间**: 1GB (用于依赖和应用)

## 方案 1: 从源码运行 (推荐用于开发)

### 步骤 1: 安装系统依赖

打开终端，运行以下命令：

```bash
# 更新包管理器
sudo apt-get update

# 安装 Python 开发工具
sudo apt-get install -y python3-dev python3-pip python3-venv

# 安装 PyQt5 及其依赖
sudo apt-get install -y python3-pyqt5 python3-pyqt5.qtwebengine

# 安装构建工具 (用于编译某些 Python 包)
sudo apt-get install -y build-essential libssl-dev libffi-dev

# 安装 weasyprint 所需的系统库
sudo apt-get install -y libpango1.0-0 libpango1.0-dev libcairo2 libcairo2-dev libgdk-pixbuf2.0-0
```

### 步骤 2: 克隆或下载项目

```bash
# 克隆项目 (如果有 Git)
git clone https://github.com/yourusername/MDViewer.git
cd MDViewer

# 或者手动下载后解压
cd /path/to/MDViewer
```

### 步骤 3: 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

激活后，终端提示符应显示 `(venv)` 前缀：
```
(venv) user@ubuntu:~/MDViewer$
```

### 步骤 4: 安装 Python 依赖

```bash
# 升级 pip
pip install --upgrade pip setuptools wheel

# 安装项目依赖
pip install -r requirements.txt
```

这将安装以下包：
- PyQt5 - GUI 框架
- markdown-it-py - Markdown 解析
- pygments - 代码高亮
- weasyprint - PDF 生成
- Pillow - 图像处理

### 步骤 5: 运行应用

```bash
# 确保虚拟环境已激活 (显示 (venv) 提示符)
python src/main.py
```

应用窗口将打开。如果没有打开，请检查终端输出中的错误信息。

### 故障排查

**问题**: 虚拟环境激活失败
```bash
# 重新创建虚拟环境
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

**问题**: PyQt5 导入错误
```bash
# 在虚拟环境中重新安装 PyQt5
pip uninstall PyQt5 -y
pip install PyQt5
```

**问题**: weasyprint 安装失败
```bash
# 确保已安装所有系统依赖
sudo apt-get install -y libpango1.0-0 libpango1.0-dev libcairo2 libcairo2-dev
# 然后重试
pip install weasyprint --no-cache-dir
```

**问题**: "Display server not available"
```bash
# 如果在远程 SSH 会话中，需要转发 X11
ssh -X user@host
```

## 方案 2: 构建可执行档 (用于分发)

### 步骤 1: 安装依赖 (同上)

### 步骤 2: 激活虚拟环境

```bash
source venv/bin/activate
```

### 步骤 3: 安装 PyInstaller

```bash
pip install pyinstaller
```

### 步骤 4: 构建可执行档

```bash
bash build.sh
```

或者手动构建：

```bash
python -m PyInstaller MDViewer.spec
```

### 步骤 5: 运行可执行档

```bash
# 直接运行
./dist/MDViewer

# 或添加到 PATH
export PATH=$PATH:$(pwd)/dist
MDViewer
```

### 创建应用快捷方式 (可选)

创建桌面文件用于应用菜单：

```bash
cat > ~/.local/share/applications/mdviewer.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Name=MDViewer
Exec=/home/YOUR_USERNAME/MDViewer/dist/MDViewer
Icon=accessories-text-editor
Type=Application
Categories=Office;WordProcessor;
Comment=A Markdown Viewer with PDF export
Terminal=false
EOF

# 使桌面文件可执行
chmod +x ~/.local/share/applications/mdviewer.desktop

# 更新应用缓存
update-desktop-database ~/.local/share/applications/
```

然后可以从应用菜单启动 MDViewer。

## 方案 3: 使用 pip 安装

如果项目发布到 PyPI (未来):

```bash
# 直接安装
pip install mdviewer

# 运行
mdviewer
```

## 常见命令

### 进入虚拟环境

```bash
source venv/bin/activate
```

### 退出虚拟环境

```bash
deactivate
```

### 运行应用

```bash
# 从源码
python src/main.py

# 从可执行档
./dist/MDViewer
```

### 更新依赖

```bash
pip install -r requirements.txt --upgrade
```

### 清理编译文件

```bash
find . -type d -name __pycache__ -exec rm -r {} +
rm -rf build/ dist/ *.egg-info
```

## 使用建议

### 首次使用

1. 打开应用后，选择 **File > Open File**
2. 选择 `test_sample.md` 或任何 Markdown 文件
3. 在预览窗口查看渲染结果
4. 在编辑器修改内容，预览实时更新
5. 使用 **File > Export as PDF** 导出为 PDF

### 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+O | 打开文件 |
| Ctrl+E | 导出 PDF |
| Ctrl+Q | 退出应用 |
| F5 | 刷新预览 |
| Ctrl+Shift+C | 清空编辑器 |

### 性能优化

- **大文件**: 编辑特别大的 Markdown 文件时，预览更新可能会有延迟
- **代码块**: 代码高亮会增加渲染时间
- **图片**: 包含大量图片时 PDF 导出可能较慢

## 系统集成

### 将文件与 MDViewer 关联

```bash
# 设置默认打开方式
xdg-mime default mdviewer.desktop text/markdown

# 验证
xdg-mime query default text/markdown
```

### 从终端打开文件

```bash
# 从终端直接打开文件
mdviewer document.md

# 或指定完整路径
./dist/MDViewer /path/to/document.md
```

## 卸载

### 卸载虚拟环境安装

```bash
cd ~/MDViewer
rm -rf venv
```

### 卸载系统包 (可选)

```bash
# 只有在不需要这些包用于其他应用时才卸载
sudo apt-get remove python3-pyqt5 python3-pyqt5.qtwebengine
```

## 获取帮助

### 查看应用日志

```bash
# 运行时查看详细输出
python src/main.py 2>&1 | tee mdviewer.log
```

### 检查依赖

```bash
pip show PyQt5 markdown-it-py weasyprint
```

### 验证安装

```bash
# 测试导入
python -c "from src.core.markdown_processor import MarkdownProcessor; print('OK')"
python -c "from PyQt5.QtWidgets import QApplication; print('OK')"
```

## 更新 MDViewer

### 从源码更新

```bash
cd ~/MDViewer
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### 重建可执行档

```bash
source venv/bin/activate
bash build.sh
```

## 下一步

- 查看 [README.md](README.md) 了解功能说明
- 查看 [DEVELOPMENT.md](DEVELOPMENT.md) 了解开发指南
- 查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 了解项目详情

---

**版本**: Ubuntu 22.04 LTS 及更新版本  
**最后更新**: 2026-04-16

## 快速参考

```bash
# 完整安装流程
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip python3-venv python3-pyqt5 python3-pyqt5.qtwebengine build-essential libssl-dev libffi-dev libpango1.0-0 libpango1.0-dev libcairo2 libcairo2-dev

cd ~/MDViewer
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 运行应用
python src/main.py
```
