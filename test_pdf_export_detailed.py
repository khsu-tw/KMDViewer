#!/usr/bin/env python3
"""測試 PDF 輸出功能並顯示詳細錯誤訊息"""

import sys
import logging
from pathlib import Path

# 設定日誌
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 加入路徑
sys.path.insert(0, str(Path(__file__).parent))

from src.core.pdf_exporter_alt import PDFExporterAlt
from src.core.markdown_processor import MarkdownProcessor

def test_pdf_export():
    """測試 PDF 輸出"""
    print("=" * 50)
    print("KMDViewer PDF 輸出測試")
    print("=" * 50)
    print()

    # 準備測試內容
    markdown_content = """# 測試標題 1

這是一個測試段落。

## 測試標題 2

- 列表項目 1
- 列表項目 2
- 列表項目 3

### 測試標題 3

這是一些**粗體**和*斜體*文字。

```python
def hello():
    print("Hello, World!")
```

#### 測試標題 4

這是另一個段落，包含 `行內程式碼`。
"""

    # 初始化處理器
    print("1. 初始化 Markdown 處理器...")
    md_processor = MarkdownProcessor()

    print("2. 轉換 Markdown 為 HTML...")
    html_content = md_processor.get_styled_html(markdown_content)

    print("3. 初始化 PDF 輸出器...")
    pdf_exporter = PDFExporterAlt()

    if not pdf_exporter.reportlab_available:
        print("❌ 錯誤: reportlab 未安裝")
        return False

    # 輸出路徑
    output_file = Path(__file__).parent / "test_output.pdf"
    print(f"4. 輸出 PDF 到: {output_file}")

    # 執行輸出
    success, error_msg = pdf_exporter.export_to_file(html_content, str(output_file))

    print()
    if success:
        print("✅ PDF 輸出成功!")
        print(f"   檔案位置: {output_file}")
        print(f"   檔案大小: {output_file.stat().st_size} bytes")
        return True
    else:
        print("❌ PDF 輸出失敗!")
        print(f"   錯誤訊息: {error_msg}")
        return False

if __name__ == "__main__":
    try:
        result = test_pdf_export()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ 發生異常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
