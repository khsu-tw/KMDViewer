# KMDViewer 快速開始

## 🚀 快速啟動

### 使用編譯好的執行檔（推薦）
```bash
cd /home/fae/Documents/GitHub/MDViewer
./dist/KMDViewer
```

### 使用開發模式
```bash
python3 -m src.main
```

## 📖 基本使用

### 1. 開啟 Markdown 檔案
- **File → Open File** (Ctrl+O)
- 或點擊工具列的 **Open** 按鈕

### 2. 即時預覽
- 左側: Markdown 編輯器
- 右側: 即時預覽
- 自動更新預覽

### 3. 匯出 PDF
1. **File → Export as PDF** (Ctrl+E)
2. 選擇頁面設定（A4、邊距等）
3. 選擇儲存位置
4. 點擊 **Save**

## 🛠️ 功能特色

### Markdown 支援
- ✅ 標題 (H1-H6)
- ✅ 段落、引用
- ✅ 粗體、斜體
- ✅ 列表（有序、無序）
- ✅ 代碼塊（語法高亮）
- ✅ 連結、圖片
- ✅ 表格
- ✅ 任務清單

### PDF 導出
- ✅ 使用 reportlab（穩定、無系統依賴）
- ✅ 自訂頁面大小（A4、Letter、A3、Legal）
- ✅ 自訂邊距
- ✅ 與預覽畫面一致的格式
- ✅ 詳細的錯誤訊息

### 其他功能
- ✅ 最近開啟的檔案
- ✅ 清除編輯器 (Ctrl+Shift+C)
- ✅ 重新整理預覽 (F5)
- ✅ 即時自動預覽

## 🔧 快捷鍵

| 功能 | 快捷鍵 |
|------|--------|
| 開啟檔案 | Ctrl+O |
| 匯出 PDF | Ctrl+E |
| 清除編輯器 | Ctrl+Shift+C |
| 重新整理預覽 | F5 |
| 離開 | Ctrl+Q |

## 🧪 測試 PDF 功能

### 快速測試
```bash
./quick_test.sh
```

### 詳細測試
```bash
python3 test_reportlab_version.py
```

## 📝 日誌位置

```
~/.kmdviewer/kmdviewer.log
```

查看日誌：
```bash
tail -f ~/.kmdviewer/kmdviewer.log
```

## ❓ 常見問題

### PDF 導出失敗怎麼辦？
1. 檢查錯誤訊息（會顯示在對話框中）
2. 檢查目標路徑是否可寫
3. 查看日誌檔案
4. 運行測試腳本確認功能

### 如何切換 PDF 導出器？
- 當前使用: **reportlab**（推薦）
- 如需 weasyprint: 參考 `REPORTLAB_MIGRATION.md`

### 程式崩潰怎麼辦？
- 所有 PDF 錯誤已修復，不會崩潰
- 如仍有問題，查看日誌檔案

## 📚 更多資訊

- `CHANGES.md` - 完整變更記錄
- `FIX_SUMMARY.md` - 問題修復總結
- `REPORTLAB_MIGRATION.md` - PDF 導出器切換說明
- `README.md` - 完整說明文件

## 🎉 享受使用 KMDViewer！

---

**版本**: v1.0  
**PDF 導出器**: reportlab  
**狀態**: ✅ 穩定運行
