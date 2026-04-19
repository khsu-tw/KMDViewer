# KMDViewer 修改記錄

## 2026-04-16 更新（第三版 - Unicode 字符支援）

### 🎨 新功能: 完整的 Unicode 字符支援
**問題**: PDF 中 ASCII 藝術字符（`│`、`─`、`┌` 等）顯示為方塊 `■`

**解決方案**: 
- ✅ 使用 **DejaVu Sans Mono** 字體替代 Courier
- ✅ 支援完整的框線字符集
- ✅ 支援中文字符
- ✅ 自動降級機制（無 DejaVu 時使用 Courier）

**修改內容**:
- 自動檢測並註冊 DejaVu Sans Mono 字體
- 在代碼塊和行內代碼中使用 Unicode 字體
- 新增 `wordWrap='CJK'` 支援中文換行
- 完善的錯誤處理和日誌記錄

**測試結果**:
```
✅ 框線字符正確顯示: ┌─┐├┤┼
✅ 垂直/水平線正確顯示: │─
✅ 行內代碼支援 Unicode
✅ 自動字體降級機制正常
```

**影響檔案**:
- `src/core/pdf_exporter_alt.py` - 字體註冊、Unicode 支援

**測試工具**:
- `test_unicode_verify.sh` - Unicode 驗證腳本
- `UNICODE_FIX.md` - 詳細修復文件

---

## 2026-04-16 更新（第二版 - 修復崩潰問題）

### 緊急修復: PDF 導出崩潰
**問題**: 程式在 PDF 導出時崩潰
```
TypeError: cannot unpack non-iterable bool object
Aborted (core dumped)
```

**原因**: 
- `pdf_exporter.py` (weasyprint) 返回 `bool`
- `pdf_exporter_alt.py` (reportlab) 返回 `tuple[bool, str]`
- UI 期望統一的 tuple 返回格式

**修復**: 
- ✅ 修改 `pdf_exporter.py` 統一返回格式為 `tuple[bool, str]`
- ✅ 重新編譯執行檔
- ✅ 測試通過，不再崩潰

**影響檔案**:
- `src/core/pdf_exporter.py` - 統一返回格式

---

## 2026-04-16 更新（第一版）

### 1. 程式名稱更改
- **MDViewer** → **KMDViewer**
- 所有相關檔案已更新

### 2. About 對話框更新
- 版權訊息: `© 2026 by Hsu, Kai-Chun`
- 新增: `Licensed under the MIT License`

### 3. PDF 輸出格式優化
調整 PDF 樣式以匹配 MDViewer 預覽畫面:

#### 字體大小
- 基礎字體: **12pt** (與預覽一致)
- H1: **24pt** (2em)
- H2: **18pt** (1.5em)
- H3: **15pt** (1.25em)
- H4: **12pt** (1em)
- 代碼塊: **10.2pt** (85%)

#### 間距
- 標題前後: 24pt / 16pt
- 代碼塊: 16pt
- 段落行距: 1.6

### 4. 錯誤處理改善
- ✅ PDF 輸出錯誤現在會顯示詳細的錯誤訊息
- ✅ 不再只顯示 "Check the logs"
- ✅ 新增日誌系統，輸出到檔案和控制台
- ✅ 日誌位置: `~/.kmdviewer/kmdviewer.log`

### 5. 檔案清單

#### 修改的檔案
- `src/main.py` - 應用程式名稱、日誌設定
- `src/ui/main_window.py` - 視窗標題、About 對話框、錯誤處理
- `src/core/pdf_exporter_alt.py` - PDF 樣式、錯誤回傳
- `setup.py` - 套件名稱、作者資訊
- `build.sh` - 建置腳本更新

#### 新增的檔案
- `KMDViewer.spec` - PyInstaller 規格檔案
- `run_kmdviewer.sh` - 直接執行腳本
- `test_pdf_export_detailed.py` - PDF 輸出測試工具

## 測試結果

### PDF 輸出測試
```bash
$ python3 test_pdf_export_detailed.py
✅ PDF 輸出成功!
   檔案位置: test_output.pdf
   檔案大小: 2569 bytes
```

### 執行方式

#### 方法 1: 直接執行（開發模式）
```bash
./run_kmdviewer.sh
# 或
python3 -m src.main
```

#### 方法 2: 編譯執行檔
```bash
./build.sh
# 執行檔位置: dist/KMDViewer
```

## 已知問題與解決方案

### PDF 輸出錯誤: "Failed to export PDF"
**原因**: 可能是以下原因之一:
1. 目標目錄沒有寫入權限
2. reportlab 未安裝
3. 檔案系統限制

**解決方案**:
- 檢查目標路徑是否可寫
- 安裝依賴: `pip3 install reportlab`
- 查看詳細錯誤訊息（現在會顯示在對話框中）
- 檢查日誌: `~/.kmdviewer/kmdviewer.log`

### 測試 PDF 功能
使用測試腳本快速驗證:
```bash
python3 test_pdf_export_detailed.py
```

## 技術細節

### PDF 樣式映射
| 元素 | MDViewer CSS | PDF 輸出 |
|------|--------------|----------|
| 基礎字體 | 16px | 12pt |
| H1 | 2em | 24pt + border |
| H2 | 1.5em | 18pt + border |
| H3 | 1.25em | 15pt |
| H4 | 1em | 12pt |
| 代碼塊 | 85% | 10.2pt |
| 行距 | 1.6 | 1.6 |

### 日誌系統
- Console 輸出: INFO 級別
- 檔案輸出: DEBUG 級別
- 位置: `~/.kmdviewer/kmdviewer.log`
- 編碼: UTF-8

## 後續建議

1. **圖示**: 為應用程式新增 icon
2. **中文字體**: 考慮加入中文字體支援（PDF 輸出）
3. **主題**: 新增深色主題選項
4. **快捷鍵**: 增加更多鍵盤快捷鍵
5. **自動儲存**: 新增自動儲存功能
