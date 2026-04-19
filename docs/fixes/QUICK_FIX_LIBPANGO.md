# libpango 安装失败 - 快速修复

**问题**: `libpango1.0-dev` 安装失败

## ✅ 快速修复 (选择一个)

### 方案 1: 使用自动降级脚本 (推荐) ⭐

```bash
cd ~/MDViewer
bash ubuntu_install_fallback.sh
```

这个脚本会：
- ✅ 尝试完整安装
- ✅ 如果失败，自动降级到最小模式
- ✅ 确保应用可用

### 方案 2: 手动最小安装

```bash
cd ~/MDViewer

# 1. 安装基础依赖 (不含 Pango)
sudo apt-get update
sudo apt-get install -y \
  python3-dev python3-pip python3-venv \
  python3-pyqt5 python3-pyqt5.qtwebengine \
  build-essential libssl-dev libffi-dev

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装最小依赖
pip install --upgrade pip
pip install -r requirements_minimal.txt

# 4. 运行应用
python src/main.py
```

### 方案 3: 诊断并修复

```bash
# 查看详细诊断
bash DIAGNOSE_LIBPANGO.md

# 或运行诊断脚本
python3 check_env.py
```

## 📊 对比

| 方案 | 安装时间 | 功能 | PDF 导出 |
|------|---------|------|---------|
| 方案 1 | 2-3分钟 | 完全 | 自动选择 |
| 方案 2 | 2分钟 | 完全 | 简化版 |
| 方案 3 | - | 诊断 | - |

## 🎯 应该选哪个?

- **第一次安装?** → 使用 `ubuntu_install_fallback.sh` ✅
- **快速修复?** → 使用方案 2 ✅
- **想诊断问题?** → 查看 `DIAGNOSE_LIBPANGO.md` ✅

## ⚡ 立即修复

```bash
# 一行命令 (使用自动脚本)
cd ~/MDViewer && bash ubuntu_install_fallback.sh

# 然后运行应用
python src/main.py
```

## 💡 重要信息

- ✅ 两种模式都能运行应用
- ✅ 文件打开、预览、格式化都正常
- ⚠️ PDF 导出在最小模式下是简化版本 (文本导出)
- ✅ 可以后期升级到完整模式

## 📝 最小模式的限制

| 功能 | 状态 |
|------|------|
| 打开文件 | ✅ 完全 |
| 实时预览 | ✅ 完全 |
| 代码高亮 | ✅ 完全 |
| 基本 PDF | ✅ 可用 |
| 高级 PDF 样式 | ✗ 不支持 |
| 图片嵌入 | ✗ 不支持 |

## 🚀 启动应用

```bash
# 激活虚拟环境
source ~/MDViewer/venv/bin/activate

# 运行应用
python ~/MDViewer/src/main.py
```

## 📞 需要更多帮助?

查看这些文件：
- `INSTALL_WITHOUT_LIBPANGO.md` - 详细的最小安装指南
- `DIAGNOSE_LIBPANGO.md` - 完整的诊断和修复
- `FIX_LIBPANGO_ERROR.md` - 错误详解和解决方案

---

**提示**: 大多数情况下，使用自动脚本是最简单的! 🎉
