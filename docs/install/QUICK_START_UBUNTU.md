# MDViewer - Ubuntu 快速开始指南

## 🚀 5 分钟快速启动

### 方案 1: 自动安装 (推荐)

最简单的方法，自动完成所有配置。

```bash
# 进入项目目录
cd ~/MDViewer

# 运行自动安装脚本 (需要输入密码)
bash ubuntu_install.sh

# 或使用 Python 版本
python3 ubuntu_install.py
```

脚本将：
✅ 安装系统依赖  
✅ 创建虚拟环境  
✅ 安装 Python 包  
✅ 运行测试  
✅ 生成可执行档 (可选)  

### 方案 2: 手动安装

如果自动脚本失败，按以下步骤手动操作。

#### 步骤 1: 安装系统依赖

```bash
# 更新包管理器
sudo apt-get update

# 一键安装所有依赖
sudo apt-get install -y \
  python3-dev \
  python3-pip \
  python3-venv \
  python3-pyqt5 \
  python3-pyqt5.qtwebengine \
  build-essential \
  libssl-dev \
  libffi-dev \
  libpango1.0-0 \
  libpango1.0-dev \
  libcairo2 \
  libcairo2-dev
```

#### 步骤 2: 创建虚拟环境

```bash
cd ~/MDViewer
python3 -m venv venv
source venv/bin/activate
```

确认激活 (终端提示符前会显示 `(venv)`):
```
(venv) user@ubuntu:~/MDViewer$
```

#### 步骤 3: 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 步骤 4: 运行应用

```bash
python src/main.py
```

## 🎯 常用命令

### 运行应用

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行 GUI 应用
python src/main.py

# 或构建后运行可执行档
./dist/MDViewer
```

### 退出虚拟环境

```bash
deactivate
```

### 构建可执行档

```bash
source venv/bin/activate
pip install pyinstaller
bash build.sh

# 或手动构建
python -m PyInstaller MDViewer.spec
```

### 查看日志

```bash
# 运行时查看详细输出
python src/main.py 2>&1 | tee mdviewer.log
```

## ⌨️ 应用快捷键

| 快捷键 | 功能 |
|--------|------|
| **Ctrl+O** | 打开文件 |
| **Ctrl+E** | 导出 PDF |
| **Ctrl+Q** | 退出应用 |
| **F5** | 刷新预览 |
| **Ctrl+Shift+C** | 清空编辑器 |

## 🔧 故障排查

### 问题: "Display server not available"

**原因**: 远程 SSH 会话

**解决**:
```bash
# 启用 X11 转发
ssh -X user@host

# 然后运行应用
python src/main.py
```

### 问题: "ImportError: No module named 'PyQt5'"

**原因**: 虚拟环境未激活或依赖未安装

**解决**:
```bash
# 激活虚拟环境
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

### 问题: "weasyprint" 安装失败

**原因**: 缺少系统库

**解决**:
```bash
# 安装 weasyprint 依赖
sudo apt-get install -y libpango1.0-0 libpango1.0-dev libcairo2 libcairo2-dev

# 重新安装
pip install weasyprint --no-cache-dir
```

### 问题: "Cannot connect to X display"

**原因**: 没有图形界面

**解决**: 使用 SSH X11 转发或在本地运行

### 问题: 应用启动很慢

**原因**: 首次启动或大文件渲染

**解决**: 耐心等待，或尝试更小的文件

### 问题: PDF 导出失败

**原因**: weasyprint 或图片路径问题

**解决**:
```bash
# 检查 weasyprint 是否正确安装
python -c "from weasyprint import HTML; print('OK')"

# 查看详细错误信息
python src/main.py 2>&1 | grep -i error
```

## 📦 需要重新安装?

### 完全清理

```bash
# 删除虚拟环境
rm -rf venv

# 清理编译文件
find . -type d -name __pycache__ -exec rm -r {} +
rm -rf build/ dist/ *.egg-info

# 重新创建
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📱 安装到应用菜单

创建桌面快捷方式，可从应用菜单启动：

```bash
# 构建可执行档 (如果还没有)
source venv/bin/activate
bash build.sh

# 创建桌面文件
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
Comment=A Markdown Viewer with PDF export
Terminal=false
EOF

# 更新应用缓存
update-desktop-database ~/.local/share/applications/
chmod +x ~/.local/share/applications/mdviewer.desktop
```

然后可以从应用菜单找到 MDViewer。

## 🎓 下一步

1. 打开 `test_sample.md` 查看演示
2. 编辑 Markdown 查看实时预览
3. 尝试导出为 PDF
4. 查看 [README.md](README.md) 了解全部功能
5. 查看 [DEVELOPMENT.md](DEVELOPMENT.md) 了解如何贡献

## 📞 获取帮助

- 查看 [UBUNTU_SETUP.md](UBUNTU_SETUP.md) - 完整安装指南
- 查看 [README.md](README.md) - 功能说明
- 检查 [DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南

## 一行命令快速参考

```bash
# 完整安装和运行流程
cd ~/MDViewer && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python src/main.py
```

---

**版本**: 1.0  
**日期**: 2026-04-16  
**系统**: Ubuntu 20.04+ LTS
