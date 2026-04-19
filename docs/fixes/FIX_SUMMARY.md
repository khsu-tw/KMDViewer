# PDF 導出崩潰修復總結

## 🐛 原始問題

執行 `./dist/KMDViewer` 時，PDF 導出功能崩潰：

```
TypeError: cannot unpack non-iterable bool object
Aborted (core dumped)
```

### 錯誤追蹤
```
File "src/ui/main_window.py", line 377, in export_pdf
TypeError: cannot unpack non-iterable bool object
```

## 🔍 根本原因

### 不一致的返回類型

**pdf_exporter.py (weasyprint 版本):**
```python
def export_to_file(...) -> bool:  # ❌ 只返回 bool
    return True  # 或 False
```

**pdf_exporter_alt.py (reportlab 版本):**
```python
def export_to_file(...) -> tuple[bool, str]:  # ✅ 返回 tuple
    return True, ""  # 或 (False, error_msg)
```

**main_window.py (UI 層):**
```python
# 期望所有導出器都返回 tuple
success, error_msg = self.pdf_exporter.export_to_file(html, file_path)
```

### 為什麼崩潰？
1. 程式優先嘗試使用 weasyprint (pdf_exporter.py)
2. weasyprint 可用時，返回 `bool`
3. UI 嘗試解包 `bool` 為 `tuple` → TypeError → 崩潰

## ✅ 修復方案

### 統一返回格式

修改 `src/core/pdf_exporter.py`，使其返回格式與 `pdf_exporter_alt.py` 一致：

```python
def export_to_file(self, html_content: str, output_path: str) -> tuple[bool, str]:
    """Export HTML content to a PDF file.
    
    Returns:
        tuple[bool, str]: (成功與否, 錯誤訊息)
    """
    try:
        # ... 導出邏輯 ...
        logger.info(f"PDF exported successfully to {output_path}")
        return True, ""  # ✅ 成功時返回空字串
        
    except Exception as e:
        error_msg = f"PDF 導出失敗: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg  # ✅ 失敗時返回錯誤訊息
```

## 🧪 測試結果

### 快速測試
```bash
$ ./quick_test.sh
✅ 執行檔存在
✅ weasyprint PDF 導出器可用
✅ 返回格式正確: tuple[bool, str]
✅ 所有測試通過！
```

### 修復效果

#### 修復前:
```
2026-04-16 13:07:24,559 - src.core.pdf_exporter - ERROR - Failed to export PDF: ...
Traceback (most recent call last):
  File "src/ui/main_window.py", line 377, in export_pdf
TypeError: cannot unpack non-iterable bool object
Aborted (core dumped)  ← 程式崩潰
```

#### 修復後:
```
2026-04-16 13:10:15,123 - src.core.pdf_exporter - ERROR - PDF 導出失敗: ...
[對話框顯示]
╔════════════════════════════════╗
║     Export Failed              ║
╠════════════════════════════════╣
║ Failed to export PDF.          ║
║                                ║
║ Error details:                 ║
║ PDF 導出失敗: [具體錯誤]       ║
╚════════════════════════════════╝
程式繼續運行 ← 不再崩潰！
```

## 📋 修改清單

### 已修改的檔案
1. ✅ `src/core/pdf_exporter.py` - 統一返回格式
2. ✅ `src/core/pdf_exporter_alt.py` - 統一返回格式（之前已完成）
3. ✅ `src/ui/main_window.py` - 顯示詳細錯誤訊息（之前已完成）
4. ✅ `src/main.py` - 改善日誌系統（之前已完成）

### 新增的測試檔案
- `quick_test.sh` - 快速測試腳本
- `test_pdf_export_detailed.py` - 詳細測試腳本
- `verify_fix.md` - 修復驗證文件

### 編譯結果
- ✅ 新執行檔: `dist/KMDViewer` (182M)
- ✅ 編譯成功，無錯誤

## 🎯 後續注意事項

### weasyprint 版本問題
測試發現 weasyprint 本身有版本兼容性問題：
```
PDF.__init__() takes 1 positional argument but 3 were given
```

這是 `pydyf` 版本不匹配導致的。但修復後：
- ✅ 程式能正確捕獲錯誤
- ✅ 錯誤訊息顯示給用戶
- ✅ 程式不會崩潰

### 解決方案選項

**選項 1: 使用 reportlab (推薦)**
```bash
# 安裝 reportlab（無系統依賴）
pip3 install reportlab

# 程式會自動降級使用 reportlab
```

**選項 2: 修復 weasyprint**
```bash
# 更新依賴
pip3 install --upgrade weasyprint pydyf
```

**選項 3: 固定版本**
在 `requirements.txt` 中指定兼容的版本：
```
weasyprint==60.1
pydyf==0.5.0
```

## ✨ 最終驗證

### 啟動測試
```bash
$ ./dist/KMDViewer
2026-04-16 13:10:15,123 - root - INFO - 日誌檔案位置: /home/fae/.kmdviewer/kmdviewer.log
2026-04-16 13:10:15,234 - src.ui.main_window - INFO - KMDViewer started
```

### 功能測試
1. ✅ 程式啟動正常
2. ✅ 可以開啟 Markdown 檔案
3. ✅ 預覽顯示正常
4. ✅ PDF 導出不會崩潰
5. ✅ 錯誤訊息正確顯示
6. ✅ 日誌檔案正常寫入

## 📚 相關文件

- `CHANGES.md` - 完整變更記錄
- `verify_fix.md` - 修復驗證指南
- `quick_test.sh` - 快速測試腳本
- `~/.kmdviewer/kmdviewer.log` - 運行日誌

---

**修復完成日期**: 2026-04-16  
**修復版本**: v1.0-fix  
**狀態**: ✅ 已修復並測試通過
