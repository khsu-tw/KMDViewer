# Unicode 字符支援修復

## 🐛 問題描述

在 PDF 輸出中，ASCII 藝術字符（如 `│`、`─`、`┌`、`┐` 等）顯示為方塊 `■`，完全無法辨識。

### 受影響的字符
- **框線字符**: `│ ─ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`
- **普通線條**: `| -`
- **其他 Unicode 符號**: 各種特殊字符

### 原因分析
reportlab 的默認等寬字體 **Courier** 不支援這些 Unicode 字符，導致顯示為方塊。

## ✅ 解決方案

### 使用 DejaVu Sans Mono 字體

**DejaVu Sans Mono** 是一個支援大量 Unicode 字符的等寬字體，包括：
- ✅ 完整的框線字符集
- ✅ 中文字符（基本支援）
- ✅ 各種特殊符號
- ✅ 西歐、東歐字符

### 實現方式

#### 1. 自動檢測並註冊字體

```python
# 檢查系統中是否有 DejaVu Sans Mono
dejavu_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
if os.path.exists(dejavu_path):
    pdfmetrics.registerFont(TTFont('DejaVuSansMono', dejavu_path))
    mono_font_name = 'DejaVuSansMono'
else:
    mono_font_name = 'Courier'  # 降級到 Courier
```

#### 2. 在代碼塊中使用

```python
styles.add(ParagraphStyle(
    name='CodeBlock',
    fontName=mono_font_name,  # 使用 DejaVu Sans Mono
    wordWrap='CJK'  # 支持中文字符換行
))
```

#### 3. 在行內代碼中使用

```python
# 行內代碼也使用相同字體
data = f'<font name="{self.mono_font}" color="darkred">{text}</font>'
```

## 🧪 測試

### 測試文件

```markdown
# Unicode 字符測試

## 框線字符

\`\`\`
┌─────────┬─────────┐
│ 項目    │ 值      │
├─────────┼─────────┤
│ 測試1   │ 100     │
└─────────┴─────────┘
\`\`\`

## 簡單線條

\`\`\`
|-------|
| Test  |
|-------|
\`\`\`

## 行內代碼

這裡有框線: \`│─┼\` 和線條: \`|---|\`
```

### 測試命令

```bash
# 使用開發模式測試
python3 -c "
from src.core.pdf_exporter_alt import PDFExporterAlt
from src.core.markdown_processor import MarkdownProcessor

with open('test_unicode.md', 'r') as f:
    content = f.read()

processor = MarkdownProcessor()
html = processor.get_styled_html(content)

exporter = PDFExporterAlt()
success, error = exporter.export_to_file(html, 'test_unicode_output.pdf')
print(f'結果: {success}')
"
```

### 預期結果

- ✅ 框線字符正確顯示為 `┌─┐` 而非 `■■■`
- ✅ 垂直線 `│` 正確顯示
- ✅ 水平線 `─` 正確顯示
- ✅ 所有連接符號正確顯示

## 📋 修改清單

### 修改的檔案
- `src/core/pdf_exporter_alt.py`

### 修改內容

#### 1. 新增字體註冊邏輯 (行 ~220)
```python
# 註冊支持 Unicode 的等寬字體
mono_font_name = 'Courier'
try:
    dejavu_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    if os.path.exists(dejavu_path):
        pdfmetrics.registerFont(TTFont('DejaVuSansMono', dejavu_path))
        mono_font_name = 'DejaVuSansMono'
        logger.info("使用 DejaVu Sans Mono 字體（支援 Unicode 字符）")
except Exception as e:
    logger.warning(f"無法註冊字體: {e}")
```

#### 2. 修改 HTMLToReportlabParser 類 (行 ~16)
```python
def __init__(self, mono_font='Courier'):
    super().__init__()
    # ...
    self.mono_font = mono_font  # 保存字體名稱
```

#### 3. 更新代碼塊樣式 (行 ~274)
```python
styles.add(ParagraphStyle(
    name='CodeBlock',
    fontName=mono_font_name,  # 使用 Unicode 字體
    wordWrap='CJK'  # 支持中文換行
))
```

#### 4. 更新行內代碼 (行 ~111)
```python
elif self.in_code:
    data = f'<font name="{self.mono_font}" ...>{text}</font>'
```

#### 5. 傳遞字體名稱給 parser (行 ~292)
```python
parser = HTMLToReportlabParser(mono_font=mono_font_name)
```

## 🎯 效果對比

### 修復前
```
代碼塊:
■■■■■■■■■■■■■
■ 項目    ■ 值      ■
■■■■■■■■■■■■■
```

### 修復後
```
代碼塊:
┌─────────┬─────────┐
│ 項目    │ 值      │
└─────────┴─────────┘
```

## 📝 注意事項

### 字體降級
如果系統中沒有 DejaVu Sans Mono：
1. 程式會自動降級到 Courier
2. 記錄警告訊息到日誌
3. Unicode 字符可能仍顯示為方塊

### 安裝 DejaVu Sans Mono

**Ubuntu/Debian:**
```bash
sudo apt-get install fonts-dejavu
```

**已安裝的系統:**
```bash
fc-list | grep -i dejavu
# 應該看到:
# /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf
```

### 驗證字體
```bash
python3 -c "
import os
path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
print('✅ DejaVu Sans Mono 可用' if os.path.exists(path) else '❌ 字體不存在')
"
```

## 🚀 使用新版本

### 重新編譯
```bash
./build.sh
```

### 執行
```bash
./dist/KMDViewer
```

### 查看日誌
```bash
tail -f ~/.kmdviewer/kmdviewer.log
# 應該看到:
# INFO - 使用 DejaVu Sans Mono 字體（支援 Unicode 字符）
```

## 🎨 支援的字符範圍

### DejaVu Sans Mono 支援
- ✅ **ASCII** (0x00-0x7F)
- ✅ **Latin-1 補充** (0x80-0xFF)
- ✅ **框線繪製** (0x2500-0x257F)
- ✅ **幾何形狀** (0x25A0-0x25FF)
- ✅ **基本中文** (部分常用字)
- ✅ **希臘字母** (0x0370-0x03FF)
- ✅ **西里爾字母** (0x0400-0x04FF)

### 框線字符集
```
┌ ┬ ┐   ╔ ╦ ╗   ╭─╮
├ ┼ ┤   ╠ ╬ ╣   │ │
└ ┴ ┘   ╚ ╩ ╝   ╰─╯

─ │ ═ ║
```

## ✨ 額外改進

### wordWrap='CJK'
新增中文、日文、韓文字符的換行支援，避免長字串在 PDF 中溢出。

### 向後兼容
- 如果 DejaVu 不可用，自動降級到 Courier
- 不會影響現有功能
- 日誌會記錄使用的字體

## 📚 相關資源

- [DejaVu Fonts](https://dejavu-fonts.github.io/)
- [Unicode Box Drawing](https://en.wikipedia.org/wiki/Box-drawing_character)
- [reportlab Font Support](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

**修復日期**: 2026-04-16  
**版本**: v1.0  
**狀態**: ✅ 已修復並測試通過
