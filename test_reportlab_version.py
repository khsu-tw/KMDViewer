#!/usr/bin/env python3
"""測試 reportlab 版本的 PDF 導出"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 測試匯入順序
print("=" * 60)
print("測試 PDF 導出器匯入順序")
print("=" * 60)
print()

try:
    from src.core.pdf_exporter_alt import PDFExporterAlt as PDFExporter
    print("✅ 成功匯入 reportlab PDF 導出器")
    exporter_type = "reportlab"
except ImportError as e:
    print(f"❌ 無法匯入 reportlab: {e}")
    try:
        from src.core.pdf_exporter import PDFExporter
        print("✅ 成功匯入 weasyprint PDF 導出器")
        exporter_type = "weasyprint"
    except ImportError as e2:
        print(f"❌ 無法匯入 weasyprint: {e2}")
        sys.exit(1)

print(f"   使用導出器: {exporter_type}")
print()

# 測試導出
from src.core.markdown_processor import MarkdownProcessor

print("測試 PDF 導出功能...")
md_content = """# KMDViewer 測試

## 功能測試

這是一個測試文件，用於驗證 PDF 導出功能。

### 特點

- ✅ 使用 reportlab
- ✅ 純 Python 實現
- ✅ 無系統依賴
- ✅ 穩定可靠

### 代碼示例

```python
def hello():
    print("Hello, KMDViewer!")
```

**結論**: 如果您看到這個 PDF，表示導出成功！
"""

processor = MarkdownProcessor()
html = processor.get_styled_html(md_content)

exporter = PDFExporter()
output_file = Path(__file__).parent / "test_reportlab_output.pdf"

print(f"輸出位置: {output_file}")
success, error_msg = exporter.export_to_file(html, str(output_file))

print()
if success:
    print("✅ PDF 導出成功!")
    print(f"   檔案: {output_file}")
    print(f"   大小: {output_file.stat().st_size} bytes")
    print()
    print("=" * 60)
    print("🎉 reportlab PDF 導出器工作正常！")
    print("=" * 60)
else:
    print("❌ PDF 導出失敗!")
    print(f"   錯誤: {error_msg}")
    sys.exit(1)
