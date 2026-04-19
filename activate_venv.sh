#!/bin/bash
# 啟動 KMDViewer 虛擬環境

source /home/fae/Documents/GitHub/MDViewer/.venv/bin/activate

echo "✅ KMDViewer 虛擬環境已啟動"
echo ""
echo "Python: $(python3 --version)"
echo "位置: $(which python3)"
echo ""
echo "已安裝的套件:"
pip3 list | grep -E "PyQt5|markdown|pygments|reportlab|Pillow"
echo ""
echo "執行程式:"
echo "  python3 -m src.main"
echo ""
echo "離開虛擬環境:"
echo "  deactivate"
