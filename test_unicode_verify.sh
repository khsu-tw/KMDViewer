#!/bin/bash
# Unicode 字符支援驗證腳本

echo "======================================"
echo "KMDViewer Unicode 字符支援測試"
echo "======================================"
echo ""

# 1. 檢查 DejaVu Sans Mono 字體
echo "1. 檢查系統字體..."
FONT_PATH="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
if [ -f "$FONT_PATH" ]; then
    echo "   ✅ DejaVu Sans Mono 字體存在"
    echo "      路徑: $FONT_PATH"
else
    echo "   ⚠️  DejaVu Sans Mono 字體不存在"
    echo "      將使用 Courier（不支援 Unicode 框線）"
fi
echo ""

# 2. 測試 PDF 生成
echo "2. 測試 PDF 生成..."
python3 << 'PYTHON_CODE'
from src.core.pdf_exporter_alt import PDFExporterAlt
from src.core.markdown_processor import MarkdownProcessor
import sys

test_content = """# Unicode 測試文件

## 框線字符測試

```
┌─────────────────┬─────────┐
│ 項目            │ 值      │
├─────────────────┼─────────┤
│ 測試 1          │ 100     │
│ 測試 2          │ 200     │
└─────────────────┴─────────┘
```

## 連接符號測試

```
├ 左連接
┤ 右連接
┬ 上連接
┴ 下連接
┼ 十字連接
```

## 簡單線條測試

```
|---------------|
| 普通表格      |
|---------------|
```

## 行內代碼測試

這裡有框線字符: `│─┼├┤┬┴` 在行內代碼中。
"""

processor = MarkdownProcessor()
html = processor.get_styled_html(test_content)

exporter = PDFExporterAlt()
success, error = exporter.export_to_file(html, 'test_unicode_verify.pdf')

if success:
    print("   ✅ PDF 生成成功")
    print("      檔案: test_unicode_verify.pdf")
    sys.exit(0)
else:
    print(f"   ❌ PDF 生成失敗: {error}")
    sys.exit(1)
PYTHON_CODE

if [ $? -eq 0 ]; then
    echo ""
    echo "3. 檢查生成的 PDF..."
    if [ -f "test_unicode_verify.pdf" ]; then
        SIZE=$(stat -c%s "test_unicode_verify.pdf")
        echo "   ✅ PDF 檔案已生成"
        echo "      大小: $SIZE bytes"
    else
        echo "   ❌ PDF 檔案不存在"
        exit 1
    fi
else
    echo ""
    echo "❌ 測試失敗"
    exit 1
fi

echo ""
echo "======================================"
echo "✅ 所有測試通過！"
echo "======================================"
echo ""
echo "請手動檢查 PDF 檔案："
echo "  test_unicode_verify.pdf"
echo ""
echo "確認以下內容："
echo "  1. 框線字符是否顯示為 ┌─┐ 而非 ■■■"
echo "  2. 垂直線 │ 是否正確顯示"
echo "  3. 水平線 ─ 是否正確顯示"
echo "  4. 行內代碼中的字符是否正確"
echo ""
echo "查看 PDF："
echo "  xdg-open test_unicode_verify.pdf"
echo ""
