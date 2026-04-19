# 標題邊框線移除

## 問題描述

在預覽和 PDF 輸出中，H1 和 H2 標題下方有明顯的灰色底線（border-bottom）。

### 範例
```
MDViewer Development Guide
─────────────────────────────  ← 這條線太明顯

Project Overview
─────────────────────────────  ← 這條線也太明顯
```

## 解決方案

已完全移除 H1 和 H2 標題的底線邊框。

### 修改內容

#### 1. 預覽畫面 (markdown_processor.py)
```css
/* 修改前 */
h1 { 
  font-size: 2em; 
  border-bottom: 1px solid #eaecef;  ← 移除
  padding-bottom: 0.3em; 
}

/* 修改後 */
h1 { 
  font-size: 2em; 
  padding-bottom: 0.3em; 
}
```

#### 2. PDF 輸出 (pdf_exporter_alt.py)
```python
# 修改前
styles.add(ParagraphStyle(
    name='CustomH1',
    borderWidth=1,        # ← 移除
    borderColor='#eaecef' # ← 移除
))

# 修改後
styles.add(ParagraphStyle(
    name='CustomH1',
    # 無邊框設定
))
```

## 效果對比

### 修改前
```
MDViewer Development Guide
═══════════════════════════  (灰色底線)

Project Overview
═══════════════════════════  (灰色底線)

Architecture
═══════════════════════════  (灰色底線)
```

### 修改後
```
MDViewer Development Guide
                            (無底線，乾淨)

Project Overview
                            (無底線，乾淨)

Architecture
                            (無底線，乾淨)
```

## 測試結果

### 測試檔案
- `test_no_borders.pdf` - 已生成

### 驗證項目
- ✅ H1 標題無底線
- ✅ H2 標題無底線
- ✅ H3-H6 標題正常（原本就無底線）
- ✅ 代碼塊背景正常 (#e8e8e8)
- ✅ 預覽與 PDF 樣式一致

## 使用新版本

### 啟動程式
```bash
./dist/KMDViewer
```

### 檢查效果
1. 開啟任何 Markdown 檔案
2. 查看 H1 和 H2 標題
3. 確認無底線邊框
4. 匯出 PDF 驗證

## 相關修改

### 受影響的元素
- ✅ H1 標題 - 已移除底線
- ✅ H2 標題 - 已移除底線
- ⚪ H3-H6 標題 - 無變更（原本就無底線）
- ⚪ 代碼塊 - 無變更（保持 #e8e8e8 背景）
- ⚪ 行內代碼 - 無變更（保持 #e8e8e8 背景）

### 檔案變更
- `src/core/markdown_processor.py` - CSS 樣式
- `src/core/pdf_exporter_alt.py` - PDF 樣式

## 版本資訊

- **修改版本**: v1.0
- **修改日期**: 2026-04-16
- **狀態**: ✅ 完成並測試通過

---

**總結**: H1 和 H2 標題的底線邊框已完全移除，介面更加簡潔乾淨。
