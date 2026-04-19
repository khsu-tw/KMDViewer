# 切換到 reportlab PDF 導出器

## ✅ 完成時間
2026-04-16 13:43

## 🎯 切換原因

### 問題
使用 weasyprint 時出現版本兼容性錯誤：
```
PDF.__init__() takes 1 positional argument but 3 were given
```

### 解決方案
切換到 **reportlab** - 穩定、純 Python、無系統依賴

## 📋 變更內容

### 1. 修改程式碼優先順序
**檔案**: `src/ui/main_window.py`

**修改前（優先 weasyprint）:**
```python
try:
    from src.core.pdf_exporter import PDFExporter  # weasyprint
    logger.info("使用 weasyprint PDF 导出器")
except ImportError:
    from src.core.pdf_exporter_alt import PDFExporterAlt as PDFExporter  # reportlab
```

**修改後（優先 reportlab）:**
```python
try:
    from src.core.pdf_exporter_alt import PDFExporterAlt as PDFExporter  # reportlab
    logger.info("使用 reportlab PDF 導出器（推薦：穩定、無系統依賴）")
except ImportError:
    from src.core.pdf_exporter import PDFExporter  # weasyprint
```

### 2. 更新依賴配置
**檔案**: `requirements.txt`

```txt
# PDF 导出 - 使用 reportlab (纯 Python，无需系统库)
reportlab==4.0.4

# 注意: weasyprint 已移除，因為有版本兼容性問題
# 如需使用 weasyprint，請安裝: pip install weasyprint==60.1 pydyf==0.5.0
```

### 3. 更新 PyInstaller 配置
**檔案**: `KMDViewer.spec`

新增 reportlab 隱藏導入：
```python
hiddenimports=[
    # ... 其他模組 ...
    'reportlab',
    'reportlab.pdfgen',
    'reportlab.lib',
    'reportlab.platypus',
],
```

### 4. 重新編譯
```bash
rm -rf build dist
python3 -m PyInstaller KMDViewer.spec
```

## 🧪 測試結果

### 程式測試
```bash
$ python3 test_reportlab_version.py

============================================================
測試 PDF 導出器匯入順序
============================================================

✅ 成功匯入 reportlab PDF 導出器
   使用導出器: reportlab

✅ PDF 導出成功!
   檔案: test_reportlab_output.pdf
   大小: 2420 bytes

============================================================
🎉 reportlab PDF 導出器工作正常！
============================================================
```

### 執行檔資訊
```
檔案: dist/KMDViewer
大小: 182M
狀態: ✅ 編譯成功
```

## 📊 reportlab vs weasyprint

| 特性 | reportlab | weasyprint |
|------|-----------|------------|
| 系統依賴 | ✅ 無 | ❌ 需要 libpango, cairo 等 |
| 安裝難度 | ✅ 簡單 | ❌ 複雜 |
| 穩定性 | ✅ 高 | ⚠️ 版本兼容問題 |
| 體積 | ✅ 小 | ❌ 大 |
| CSS 支援 | ⚠️ 基本 | ✅ 完整 |
| 適用場景 | ✅ 一般 Markdown | ⚠️ 複雜排版 |

## ✨ 優勢

### reportlab 的優點
1. ✅ **純 Python** - 無需系統庫
2. ✅ **穩定** - 無版本兼容問題
3. ✅ **輕量** - 體積小
4. ✅ **跨平台** - 任何系統都可運行
5. ✅ **易部署** - 一個 pip install 搞定

### 當前功能支援
- ✅ 標題 (H1-H6)
- ✅ 段落
- ✅ 列表（有序、無序）
- ✅ 粗體、斜體
- ✅ 代碼塊（語法高亮）
- ✅ 行內代碼
- ✅ 自訂樣式

## 🚀 使用方式

### 開發模式
```bash
python3 -m src.main
```

### 執行檔模式
```bash
./dist/KMDViewer
```

### 日誌位置
```
~/.kmdviewer/kmdviewer.log
```

日誌會顯示：
```
INFO - 使用 reportlab PDF 導出器（推薦：穩定、無系統依賴）
```

## 📝 如需切換回 weasyprint

如果您確實需要 weasyprint 的完整 CSS 支援：

### 1. 安裝兼容版本
```bash
pip3 install weasyprint==60.1 pydyf==0.5.0
```

### 2. 修改匯入順序
編輯 `src/ui/main_window.py`，將 weasyprint 放回優先位置

### 3. 重新編譯
```bash
./build.sh
```

## ✅ 驗證清單

- [x] 修改程式碼優先使用 reportlab
- [x] 更新 requirements.txt
- [x] 更新 KMDViewer.spec
- [x] 重新編譯執行檔
- [x] 測試 PDF 導出功能
- [x] 驗證不會崩潰
- [x] 驗證錯誤訊息顯示
- [x] 建立測試腳本
- [x] 更新文件

## 📚 相關文件

- `CHANGES.md` - 完整變更記錄
- `FIX_SUMMARY.md` - 崩潰修復總結
- `test_reportlab_version.py` - reportlab 測試腳本
- `test_pdf_export_detailed.py` - 詳細測試腳本

---

**切換狀態**: ✅ 完成  
**測試狀態**: ✅ 通過  
**推薦使用**: ✅ reportlab（當前配置）
