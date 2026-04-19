# 修复 libpango 安装失败

## 🔴 问题

Ubuntu 安装时出现错误：
```
E: Unable to locate package libpango-1.0-dev
```

## 🟢 原因

包名称在 Ubuntu 22.04+ 中已更改：
- ❌ 旧包名: `libpango-1.0-dev` (不存在)
- ✅ 新包名: `libpango1.0-dev` (正确)

## 解决方案

### 方案 1: 使用正确的包名 (推荐)

```bash
sudo apt-get update

# 安装正确的包名
sudo apt-get install -y \
  libpango1.0-0 \
  libpango1.0-dev \
  libcairo2 \
  libcairo2-dev \
  libgdk-pixbuf2.0-0
```

### 方案 2: 一键修复所有依赖

```bash
sudo apt-get update && sudo apt-get install -y \
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
  libcairo2-dev \
  libgdk-pixbuf2.0-0
```

### 方案 3: 使用 weasyprint 官方推荐的依赖

```bash
# 完整的 weasyprint 依赖 (Ubuntu 20.04+)
sudo apt-get install -y \
  python3-dev \
  python3-pip \
  python3-cffi \
  python3-brotli \
  libffi-dev \
  libcairo2 \
  libpango-1.0-0 \
  libpango-gobject-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libffi7 \
  shared-mime-info
```

### 方案 4: 使用系统包安装 weasyprint (最简单)

如果 pip 安装 weasyprint 仍然失败，可以使用 Ubuntu 官方包：

```bash
# 检查是否有 weasyprint 包
apt-cache search weasyprint

# 如果有，直接安装
sudo apt-get install -y python3-weasyprint
```

## 修复 MDViewer 安装

修复依赖后，重新安装 MDViewer：

### 步骤 1: 修复系统依赖

```bash
sudo apt-get update
sudo apt-get install -y \
  libpango1.0-dev \
  libcairo2 \
  libcairo2-dev
```

### 步骤 2: 删除旧的虚拟环境 (如果已创建)

```bash
cd ~/MDViewer
rm -rf venv
```

### 步骤 3: 重新安装

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装 MDViewer 依赖
pip install -r requirements.txt
```

### 步骤 4: 验证安装

```bash
python3 check_env.py
```

### 步骤 5: 运行应用

```bash
python src/main.py
```

## 常见错误和解决方案

### 错误 1: "E: Unable to locate package libpango-1.0-dev"

**解决**:
```bash
# 使用正确的包名
sudo apt-get install -y libpango1.0-dev
```

### 错误 2: "weasyprint" 导入失败

**解决**:
```bash
# 重新安装 weasyprint
pip uninstall weasyprint -y
pip install weasyprint --no-cache-dir

# 或使用系统包
sudo apt-get install -y python3-weasyprint
```

### 错误 3: "libffi.so.7" 未找到

**解决**:
```bash
sudo apt-get install -y libffi7 libffi-dev
```

### 错误 4: "cairo" 相关错误

**解决**:
```bash
sudo apt-get install -y \
  libcairo2 \
  libcairo2-dev \
  libcairo-gobject2
```

## 完整的 Ubuntu 包列表

### 对于 Ubuntu 20.04 LTS

```bash
sudo apt-get update && sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  libpango1.0-0 libpango1.0-dev \
  libcairo2 libcairo2-dev \
  libgdk-pixbuf2.0-0 libffi7
```

### 对于 Ubuntu 22.04 LTS

```bash
sudo apt-get update && sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  libpango1.0-0 libpango1.0-dev \
  libcairo2 libcairo2-dev \
  libgdk-pixbuf2.0-0
```

### 对于 Ubuntu 24.04 LTS (新版本)

```bash
sudo apt-get update && sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev \
  libpango-1.0-0 libpango-1.0-dev \
  libcairo2 libcairo2-dev \
  libgdk-pixbuf2.0-0
```

## 验证修复

运行以下命令验证所有依赖已正确安装：

```bash
# 检查 libpango
dpkg -l | grep libpango

# 检查 cairo
dpkg -l | grep libcairo

# 测试 weasyprint 导入
python3 -c "from weasyprint import HTML; print('✓ weasyprint 正常')"

# 完整环境检查
python3 check_env.py
```

## 快速修复脚本

将以下内容保存为 `fix_libpango.sh`：

```bash
#!/bin/bash

echo "修复 libpango 安装问题..."

# 更新包列表
sudo apt-get update

# 安装正确的包名
echo "安装 libpango1.0-dev..."
sudo apt-get install -y libpango1.0-dev

# 安装其他必要的库
echo "安装其他依赖库..."
sudo apt-get install -y \
  libcairo2 \
  libcairo2-dev \
  libgdk-pixbuf2.0-0

# 重新安装 weasyprint
echo "重新安装 weasyprint..."
pip install --upgrade weasyprint

# 验证
echo "验证安装..."
python3 -c "from weasyprint import HTML; print('✓ 修复成功！')"
```

使用方法：
```bash
chmod +x fix_libpango.sh
./fix_libpango.sh
```

## 后续步骤

修复后，继续安装 MDViewer：

```bash
cd ~/MDViewer

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 验证
python3 check_env.py

# 运行应用
python src/main.py
```

## 参考资源

- [Weasyprint 官方文档](https://weasyprint.readthedocs.io/)
- [Ubuntu 包搜索](https://packages.ubuntu.com/)
- [Pango 官方网站](https://pango.gnome.org/)

---

**如果问题仍未解决，请运行以下命令并提供输出**:

```bash
# 显示 Ubuntu 版本
lsb_release -a

# 显示已安装的 libpango 包
dpkg -l | grep libpango

# 尝试安装并显示错误信息
sudo apt-get install -y libpango1.0-dev 2>&1
```

**版本**: 1.0  
**日期**: 2026-04-16
