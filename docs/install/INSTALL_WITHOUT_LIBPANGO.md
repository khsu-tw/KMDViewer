# 不使用 libpango 安装 MDViewer

如果 `libpango1.0-dev` 安装失败，可以使用此指南进行安装。

## 🎯 快速开始 (3 步)

### 步骤 1: 安装最小系统依赖

```bash
# 不包括 Pango 相关的库
sudo apt-get update
sudo apt-get install -y \
  python3-dev \
  python3-pip \
  python3-venv \
  python3-pyqt5 \
  python3-pyqt5.qtwebengine \
  build-essential \
  libssl-dev \
  libffi-dev
```

### 步骤 2: 创建虚拟环境并安装依赖

```bash
cd ~/MDViewer

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装最小依赖 (不包括 weasyprint)
pip install -r requirements_minimal.txt
```

### 步骤 3: 运行应用

```bash
# 确保虚拟环境已激活
python src/main.py
```

## ✨ 可用功能

### ✅ 完全支持
- ✓ 打开 Markdown 文件
- ✓ 实时预览
- ✓ 代码高亮
- ✓ 格式化显示
- ✓ 最近文件列表

### ⚠️ 有限支持
- ⚠️ PDF 导出 (简化版本)
  - 使用 reportlab 生成 PDF
  - 支持基本文本和排版
  - 不支持复杂样式

### ❌ 不支持
- ✗ 高级 PDF 样式
- ✗ 图片在 PDF 中的嵌入 (仅文本)

## 📋 两种安装方案

### 方案 A: 最小安装 (推荐)

使用 `requirements_minimal.txt` - 只安装必要的包：

```bash
pip install -r requirements_minimal.txt
```

**包含**:
- PyQt5 (GUI)
- markdown-it-py (Markdown 解析)
- pygments (代码高亮)
- reportlab (PDF 导出 - 简化版)

### 方案 B: 完整安装 (如果 libpango 可用)

如果后来 libpango 变得可用，使用完整配置：

```bash
sudo apt-get install -y libpango1.0-dev libcairo2-dev
pip install -r requirements.txt
```

## 🔧 修复 PDF 导出功能

如果想要完整的 PDF 功能，有两个选择：

### 选择 1: 安装 weasyprint (需要 libpango)

```bash
# 首先修复 libpango 问题
sudo apt-get install -y libpango1.0-dev libcairo2-dev

# 然后安装 weasyprint
pip install weasyprint

# 运行应用
python src/main.py
```

### 选择 2: 使用改进的 reportlab

```bash
# 已在 requirements_minimal.txt 中包含
pip install reportlab

# 应用中的 PDF 导出会使用 reportlab
```

## 📝 修改 requirements.txt (高级)

### 添加其他 PDF 库

你可以修改 `requirements_minimal.txt` 来使用其他 PDF 库：

**使用 pypdf + markdown2** (轻量级):
```bash
cat > requirements_minimal.txt << 'EOF'
PyQt5==5.15.9
PyQt5-sip==12.13.0
markdown-it-py==3.0.0
mdit-py-plugins==0.4.0
pygments==2.17.2
Pillow==10.1.0
pypdf==4.0.0
markdown2==2.4.9
EOF

pip install -r requirements_minimal.txt
```

**使用 xhtml2pdf** (简单):
```bash
pip install xhtml2pdf
```

## 🐛 故障排查

### 问题: "ModuleNotFoundError: No module named 'weasyprint'"

**原因**: weasyprint 未安装 (这是预期的)

**解决**: PDF 导出会使用 reportlab，功能正常

```bash
# 验证 reportlab 已安装
python -c "from reportlab.pdfgen import canvas; print('OK')"
```

### 问题: "No module named 'reportlab'"

**原因**: reportlab 未安装

**解决**:
```bash
pip install reportlab
```

### 问题: 应用无法启动

**原因**: 缺少必要的包

**解决**:
```bash
# 验证所有包
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5: OK')"
python -c "from markdown_it import MarkdownIt; print('markdown-it: OK')"
python -c "from pygments import highlight; print('pygments: OK')"
```

## 🎓 了解更多

### 如何使用最小安装

1. **打开文件**: File > Open File (所有功能正常)
2. **预览**: 左侧编辑，右侧预览 (完全支持)
3. **导出 PDF**: File > Export as PDF (简化版本 - 文本导出)

### 功能限制

- PDF 中只包含文本内容
- 不支持图片嵌入
- 样式简化 (无高级 CSS)
- 排版基本 (无精细控制)

但核心功能全部可用！

## ✅ 验证安装

运行以下命令验证：

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行检查脚本
python3 check_env.py

# 或手动检查
python -c "
from PyQt5.QtWidgets import QApplication
from markdown_it import MarkdownIt
from pygments import highlight
from reportlab.pdfgen import canvas

print('✓ 所有核心模块都已安装')
print('✓ 可以安全使用 MDViewer')
"
```

## 🚀 启动应用

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动应用
python src/main.py

# 现在可以使用所有功能！
```

## 📦 包大小对比

| 配置 | 大小 | 安装时间 |
|------|------|---------|
| requirements_minimal.txt | ~300MB | ~2分钟 |
| requirements.txt | ~500MB+ | ~5分钟 |

最小安装更快更轻！

## 🔄 从最小安装升级

如果后来想要完整功能：

```bash
source venv/bin/activate

# 安装完整依赖
pip install -r requirements.txt

# 或只安装 weasyprint
pip install weasyprint

# 之后 PDF 导出会自动使用 weasyprint
```

## 📞 需要帮助?

1. 查看 `DIAGNOSE_LIBPANGO.md` - 诊断工具
2. 查看 `FIX_LIBPANGO_ERROR.md` - 修复方案
3. 运行 `python3 check_env.py` - 环境检查

---

**版本**: 1.0  
**日期**: 2026-04-16

这是推荐的安装方式，当系统库有问题时！🚀
