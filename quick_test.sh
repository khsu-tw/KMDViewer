#!/bin/bash
# 快速測試 KMDViewer PDF 導出功能

echo "======================================"
echo "KMDViewer PDF 導出功能測試"
echo "======================================"
echo ""

# 檢查執行檔是否存在
if [ ! -f "dist/KMDViewer" ]; then
    echo "❌ 錯誤: 找不到 dist/KMDViewer"
    echo "請先執行: ./build.sh"
    exit 1
fi

echo "✅ 執行檔存在"
echo "   位置: dist/KMDViewer"
echo "   大小: $(ls -lh dist/KMDViewer | awk '{print $5}')"
echo ""

# 檢查 Python 模組
echo "檢查依賴..."
python3 -c "
import sys
try:
    from src.core.pdf_exporter import PDFExporter
    print('✅ weasyprint PDF 導出器可用')

    # 測試返回格式
    exporter = PDFExporter()
    result = exporter.export_to_file('<html><body><h1>Test</h1></body></html>', 'test_quick.pdf')
    if isinstance(result, tuple) and len(result) == 2:
        print('✅ 返回格式正確: tuple[bool, str]')
        success, error_msg = result
        print(f'   成功: {success}, 錯誤訊息: \"{error_msg}\"')
    else:
        print('❌ 返回格式錯誤!')
        sys.exit(1)
except ImportError as e:
    print(f'⚠️  weasyprint 不可用: {e}')
    try:
        from src.core.pdf_exporter_alt import PDFExporterAlt
        print('✅ reportlab PDF 導出器可用')
    except ImportError as e2:
        print(f'❌ reportlab 也不可用: {e2}')
        sys.exit(1)
except Exception as e:
    print(f'❌ 測試失敗: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ 所有測試通過！"
    echo "======================================"
    echo ""
    echo "您現在可以執行："
    echo "  ./dist/KMDViewer"
    echo ""
    echo "或使用開發模式："
    echo "  python3 -m src.main"
    exit 0
else
    echo ""
    echo "======================================"
    echo "❌ 測試失敗"
    echo "======================================"
    exit 1
fi
