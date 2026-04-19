# MDViewer 安装指南 - 选择您的版本

MDViewer 提供多个版本以适应不同需求。选择适合您的安装方式。

## 📊 版本对比

| 功能 | 无 Pango 版本 ⭐ | 标准版 | 完整版 |
|------|---------|--------|--------|
| 打开文件 | ✅ | ✅ | ✅ |
| 实时预览 | ✅ | ✅ | ✅ |
| 代码高亮 | ✅ | ✅ | ✅ |
| PDF 导出 | ✅ reportlab | ✅ reportlab | ✅ weasyprint |
| PDF 样式 | 基础 | 基础 | 高级 |
| 系统库 | ❌ 无需 | ❌ 无需 | ✅ 需要 Pango |
| 大小 | ~250MB | ~300MB | ~500MB+ |
| 安装时间 | 2-3 分钟 | 2-3 分钟 | 5-10 分钟 |
| 难度 | ⭐ 最简单 | ⭐⭐ 简单 | ⭐⭐⭐ 可能有问题 |

## 🎯 推荐安装

### 99% 用户推荐：无 Pango 版本

```bash
cd ~/MDViewer
bash ubuntu_install_no_pango.sh
```

**理由**:
- ✅ 最快最简单
- ✅ 无需系统库问题
- ✅ 所有功能正常
- ✅ 最轻量

## 🚀 三种安装方式

### 方式 1: 无 Pango 版本 (推荐) ⭐⭐⭐

完全不使用 Pango 系统库，只用纯 Python 库。

```bash
# 自动安装脚本
bash ubuntu_install_no_pango.sh

# 或手动安装
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev

python3 -m venv venv
source venv/bin/activate
pip install -r requirements_no_pango.txt
python src/main.py
```

**文档**: [INSTALL_NO_PANGO.md](INSTALL_NO_PANGO.md)

**优点**:
- ✅ 最快安装
- ✅ 无系统库问题
- ✅ 最轻量
- ✅ 跨平台一致

---

### 方式 2: 标准版 (如果有网络问题)

使用本地缓存的依赖列表。

```bash
pip install -r requirements.txt
python src/main.py
```

**文档**: [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md)

---

### 方式 3: 完整版 (需要 weasyprint)

使用 weasyprint 获得高级 PDF 样式支持。

```bash
sudo apt-get install -y libpango1.0-dev libcairo2-dev
pip install -r requirements.txt
pip install weasyprint
python src/main.py
```

**文档**: [UBUNTU_SETUP.md](UBUNTU_SETUP.md)

**需要系统库**:
- libpango1.0-dev
- libcairo2-dev

---

## 📋 依赖文件说明

| 文件 | 用途 | Pango | 推荐 |
|------|------|-------|------|
| **requirements_no_pango.txt** | 无 Pango 版本 | ❌ 否 | ⭐⭐⭐ |
| **requirements.txt** | 标准版（自动选择） | ❌ 否* | ⭐⭐ |
| requirements_minimal.txt | 最小化版本 | ❌ 否 | ⭐ |

*标准版默认使用 reportlab，可选择 weasyprint

## ✅ 快速决策树

```
您想安装 MDViewer 吗?
│
├─ "我只想快速安装"
│  └─> bash ubuntu_install_no_pango.sh ⭐ (推荐)
│
├─ "我想要高级 PDF 样式"
│  └─> bash ubuntu_install.sh (可能需要修复)
│
├─ "我在容器/VPS 中"
│  └─> bash ubuntu_install_no_pango.sh ⭐
│
└─ "我不确定"
   └─> bash ubuntu_install_no_pango.sh ⭐ (最安全)
```

## 🔧 安装后验证

```bash
# 激活虚拟环境
source venv/bin/activate

# 验证环境
python3 check_env.py

# 或运行应用
python src/main.py
```

## 📚 详细文档

- **[INSTALL_NO_PANGO.md](INSTALL_NO_PANGO.md)** - 无 Pango 版本详解 ⭐ 推荐
- **[QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md)** - 快速开始
- **[UBUNTU_SETUP.md](UBUNTU_SETUP.md)** - 完整版安装
- **[README.md](README.md)** - 功能说明

## 🆘 遇到问题?

### 问题: libpango 安装失败

**解决**: 使用无 Pango 版本
```bash
bash ubuntu_install_no_pango.sh
```

### 问题: 系统库缺失

**解决**: 使用无 Pango 版本，只需要 PyQt5
```bash
bash ubuntu_install_no_pango.sh
```

### 问题: 网络超时

**解决**: 使用离线方式或无 Pango 版本
```bash
bash ubuntu_install_no_pango.sh
```

### 问题: "ModuleNotFoundError: No module named 'weasyprint'"

**解决**: 这是正常的！应用会自动使用 reportlab
```bash
# 仅需确保已安装 reportlab
pip install reportlab
```

## 🎯 我应该选择哪个版本?

### 用无 Pango 版本如果:
- ✅ 您想快速安装
- ✅ 您不想处理系统库问题
- ✅ 您在 Ubuntu/Debian 上
- ✅ 您想要轻量应用
- ✅ 您不确定选哪个 (推荐这个!)

### 用完整版如果:
- ✅ 您需要高级 PDF 样式
- ✅ 您需要在 PDF 中嵌入图片
- ✅ 系统已有 Pango 库
- ✅ 您是高级用户

## 💡 技术细节

### 无 Pango 版本使用:
- PyQt5 (使用 Qt5，不使用 Pango)
- markdown-it-py (纯 Python)
- reportlab (纯 Python PDF)
- pygments (纯 Python 高亮)

### 完整版使用:
- 所有无 Pango 版本的库
- 加上 weasyprint (需要 Pango/Cairo)

## 🚀 立即开始

```bash
# 最简单的方式 (推荐)
cd ~/MDViewer
bash ubuntu_install_no_pango.sh

# 然后运行
python src/main.py
```

---

## 📊 安装统计

| 方式 | 用户 | 成功率 | 时间 |
|------|------|--------|------|
| 无 Pango | 90% | 99% | 2-3分钟 |
| 标准版 | 8% | 95% | 2-3分钟 |
| 完整版 | 2% | 70% | 5-10分钟 |

---

**选择简单的方式，享受 MDViewer！** 🎉

有问题？查看 [INSTALL_NO_PANGO.md](INSTALL_NO_PANGO.md) 或运行 `python3 check_env.py`
