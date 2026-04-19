# 诊断 libpango 安装失败

## 🔴 问题症状

```
❌ 安装 libpango1.0-dev...
❌ 安装 libpango1.0-dev 失败
❌ 系统依赖安装失败
```

## 🔍 诊断步骤

### 步骤 1: 检查 Ubuntu 版本

```bash
# 显示 Ubuntu 版本详情
lsb_release -a

# 显示 Ubuntu 代号
cat /etc/os-release | grep VERSION_CODENAME
```

### 步骤 2: 检查包是否存在

```bash
# 搜索 libpango 包
apt-cache search libpango | head -20

# 搜索具体的包
apt-cache search "^libpango1.0" 

# 检查 dev 包
apt-cache policy libpango1.0-dev
```

### 步骤 3: 更新包列表

```bash
# 完整更新
sudo apt-get update --fix-missing
sudo apt-get upgrade
```

### 步骤 4: 检查包管理器错误

```bash
# 检查是否有损坏的依赖
sudo apt-get check

# 修复损坏的依赖
sudo apt --fix-broken install
```

### 步骤 5: 尝试不同的包名

```bash
# Ubuntu 20.04
sudo apt-get install -y libpango-1.0-dev

# Ubuntu 22.04/24.04
sudo apt-get install -y libpango1.0-dev

# 或尝试这个
sudo apt-get install -y libpango1.0-dev:amd64
```

## 🟢 替代方案

如果以上都失败，有多个替代方案：

### 方案 A: 跳过 libpango，使用系统 weasyprint

```bash
# Ubuntu 官方包通常已包含所有依赖
sudo apt-get install -y python3-weasyprint

# 检查是否安装成功
python3 -c "from weasyprint import HTML; print('OK')"
```

### 方案 B: 使用其他 PDF 库

修改 `requirements.txt`，用其他 PDF 库替代 weasyprint：

**选项 1: 使用 reportlab** (更轻量)
```bash
pip install reportlab markdown2
```

**选项 2: 使用 pypdf** (更稳定)
```bash
pip install pypdf markdown2
```

### 方案 C: Docker 容器化

使用预配置的 Docker 镜像避免依赖问题：

```bash
# 创建 Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.10

RUN apt-get update && apt-get install -y \
    python3-pyqt5 python3-pyqt5.qtwebengine \
    libpango1.0-0 libpango1.0-dev \
    libcairo2 libcairo2-dev

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "src/main.py"]
EOF

# 构建并运行
docker build -t mdviewer .
docker run -it -e DISPLAY=$DISPLAY mdviewer
```

### 方案 D: 修改 requirements.txt

如果 weasyprint 无法安装，替换为其他库：

```bash
# 备份原文件
cp requirements.txt requirements.txt.bak

# 创建简化版本 (不需要 weasyprint)
cat > requirements.txt << 'EOF'
PyQt5==5.15.9
PyQt5-sip==12.13.0
markdown-it-py==3.0.0
mdit-py-plugins==0.4.0
pygments==2.17.2
Pillow==10.1.0
EOF

# 或使用 reportlab
cat > requirements.txt << 'EOF'
PyQt5==5.15.9
PyQt5-sip==12.13.0
markdown-it-py==3.0.0
mdit-py-plugins==0.4.0
pygments==2.17.2
reportlab==4.0.4
markdown2==2.4.9
Pillow==10.1.0
EOF
```

### 方案 E: 手动安装所需库

```bash
# 一个一个地安装，找出哪个失败
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo apt-get install -y python3-pyqt5
sudo apt-get install -y python3-pyqt5.qtwebengine
sudo apt-get install -y build-essential
sudo apt-get install -y libssl-dev
sudo apt-get install -y libffi-dev

# 然后尝试安装 Cairo 相关
sudo apt-get install -y libcairo2
sudo apt-get install -y libcairo2-dev

# 最后尝试 Pango - 用多个选项试试
sudo apt-get install -y libpango1.0-0 || true
sudo apt-get install -y libpango1.0-dev || true
sudo apt-get install -y libpango-1.0-0 || true
sudo apt-get install -y libpango-1.0-dev || true

# 检查 Pango 是否安装了
dpkg -l | grep pango
```

## 📋 具体 Ubuntu 版本的解决方案

### Ubuntu 20.04 LTS

```bash
sudo apt-get update
sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  libpango-1.0-0 libpango-1.0-dev \
  libcairo2 libcairo2-dev
```

### Ubuntu 22.04 LTS

```bash
sudo apt-get update
sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  libcairo2 libcairo2-dev libgdk-pixbuf2.0-0

# 如果上面的 libpango 包失败，尝试这个
sudo apt-get install -y python3-weasyprint
```

### Ubuntu 24.04 LTS (新版本)

```bash
sudo apt-get update
sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  python3-weasyprint
```

## 🛠️ 最小依赖安装 (MDViewer 核心功能)

如果某些包无法安装，可以只安装核心依赖：

```bash
# 最小依赖 (不包括 PDF 导出)
sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine

# 然后安装 Python 包
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_minimal.txt
```

创建 `requirements_minimal.txt`:
```
PyQt5==5.15.9
PyQt5-sip==12.13.0
markdown-it-py==3.0.0
mdit-py-plugins==0.4.0
pygments==2.17.2
Pillow==10.1.0
```

此时 MDViewer 可以打开和预览文件，但 PDF 导出功能会禁用。

## 🔧 修复脚本

保存为 `fix_install.sh`:

```bash
#!/bin/bash

echo "诊断系统..."
lsb_release -a

echo ""
echo "尝试多种方式安装依赖..."

# 更新
sudo apt-get update --fix-missing

# 尝试方案 1: 标准包名
echo "尝试标准包名..."
sudo apt-get install -y libpango1.0-dev 2>/dev/null && echo "✓ libpango1.0-dev 成功" || echo "✗ libpango1.0-dev 失败"

# 尝试方案 2: 旧包名
echo "尝试旧包名..."
sudo apt-get install -y libpango-1.0-dev 2>/dev/null && echo "✓ libpango-1.0-dev 成功" || echo "✗ libpango-1.0-dev 失败"

# 尝试方案 3: 系统 weasyprint
echo "尝试系统 weasyprint..."
sudo apt-get install -y python3-weasyprint 2>/dev/null && echo "✓ python3-weasyprint 成功" || echo "✗ python3-weasyprint 失败"

# 安装其他库
echo "安装其他依赖..."
sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  libcairo2 libcairo2-dev 2>/dev/null && echo "✓ 核心依赖安装成功" || echo "⚠ 部分依赖安装失败"

echo ""
echo "诊断完成！"
```

使用：
```bash
chmod +x fix_install.sh
./fix_install.sh
```

## ⚡ 快速修复流程

1. **确认 Ubuntu 版本**
   ```bash
   lsb_release -a
   ```

2. **选择对应方案**
   ```bash
   # 根据你的 Ubuntu 版本选择上面的方案
   ```

3. **验证安装**
   ```bash
   python3 -c "from weasyprint import HTML; print('✓ OK')" 2>/dev/null || echo "✗ weasyprint 未安装"
   ```

4. **继续安装 MDViewer**
   ```bash
   cd ~/MDViewer
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python src/main.py
   ```

## 📞 需要帮助？

请提供以下信息：

```bash
# 1. Ubuntu 版本
lsb_release -a

# 2. 错误信息
sudo apt-get install -y libpango1.0-dev 2>&1

# 3. 已安装的 Pango 相关包
dpkg -l | grep pango

# 4. 包可用性
apt-cache policy libpango1.0-dev
apt-cache policy libpango-1.0-dev
```

---

**版本**: 1.0  
**日期**: 2026-04-16
