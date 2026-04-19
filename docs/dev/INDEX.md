# MDViewer 项目文档索引

欢迎使用 MDViewer！这是所有文档、指南和工具的完整索引。

## 🚀 快速开始

### 对于 Ubuntu 用户 (推荐)
1. **[QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md)** - 5分钟快速开始
2. **[ubuntu_install.sh](ubuntu_install.sh)** - 自动安装脚本
3. **[check_env.py](check_env.py)** - 环境检查工具

### 对于其他平台
- **[README.md](README.md)** - 通用指南
- **[INSTALLATION.md](INSTALLATION.md)** - 详细安装步骤

---

## 📚 完整文档

### 用户文档

| 文档 | 用途 | 读者 |
|------|------|------|
| [README.md](README.md) | 项目概述、功能说明 | 所有用户 |
| [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md) | Ubuntu 快速参考卡片 | Ubuntu 用户 |
| [UBUNTU_SETUP.md](UBUNTU_SETUP.md) | Ubuntu 完整安装指南 | Ubuntu 用户 |
| [UBUNTU_READY.md](UBUNTU_READY.md) | Ubuntu 就绪检查清单 | Ubuntu 用户 |
| [INSTALLATION.md](INSTALLATION.md) | 通用安装和故障排查 | 所有用户 |

### 开发文档

| 文档 | 用途 | 读者 |
|------|------|------|
| [DEVELOPMENT.md](DEVELOPMENT.md) | 开发指南、架构说明 | 开发者 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目完成总结 | 项目管理 |

### 工具和配置

| 文件 | 用途 | 类型 |
|------|------|------|
| [Workplan.md](Workplan.md) | 原始项目计划 | 计划文档 |

---

## 🔧 安装工具

### Ubuntu 安装 (推荐)

**自动安装脚本**

```bash
# 使用 Bash
bash ubuntu_install.sh

# 或使用 Python
python3 ubuntu_install.py
```

特点：
- ✅ 自动检查系统环境
- ✅ 自动安装系统依赖
- ✅ 自动创建虚拟环境
- ✅ 自动验证安装
- ✅ 支持可执行档生成
- ✅ 支持应用菜单集成

### 环境检查工具

```bash
python3 check_env.py
```

检查项目：
- Python 版本
- 项目文件完整性
- 系统环境配置
- 显示服务器
- Python 包安装情况

### 构建工具

**创建独立可执行档**

```bash
# macOS/Linux
bash build.sh

# Windows
build.bat
```

配置文件：
- [MDViewer.spec](MDViewer.spec) - PyInstaller 配置

---

## 🎯 常见任务

### 任务 1: 第一次使用

1. 阅读 [README.md](README.md) 了解功能
2. 运行 [ubuntu_install.sh](ubuntu_install.sh) 安装
3. 执行 [check_env.py](check_env.py) 验证
4. 运行 `python src/main.py` 启动应用

### 任务 2: 故障排查

1. 首先运行 [check_env.py](check_env.py)
2. 查看 [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md) 的故障排查部分
3. 查看 [UBUNTU_SETUP.md](UBUNTU_SETUP.md) 的完整故障排查
4. 查看 [INSTALLATION.md](INSTALLATION.md) 的通用解决方案

### 任务 3: 了解项目架构

1. 阅读 [DEVELOPMENT.md](DEVELOPMENT.md) 的项目概述
2. 查看项目结构说明
3. 查看关键组件说明

### 任务 4: 贡献代码

1. 阅读 [DEVELOPMENT.md](DEVELOPMENT.md) 的完整指南
2. 按照编码标准和测试要求
3. 提交 Pull Request

---

## 📁 项目结构

```
MDViewer/
├── src/                           # 源代码
│   ├── main.py                   # 应用入口
│   ├── core/                     # 核心模块
│   │   ├── markdown_processor.py # MD→HTML 转换
│   │   ├── pdf_exporter.py       # HTML→PDF 导出
│   │   └── file_manager.py       # 文件操作
│   └── ui/                       # 用户界面
│       ├── main_window.py        # 主窗口
│       └── preview_viewer.py     # 预览窗口
│
├── 📖 文档
│   ├── README.md                 # 项目概述
│   ├── QUICK_START_UBUNTU.md     # Ubuntu 快速开始
│   ├── UBUNTU_SETUP.md           # Ubuntu 安装指南
│   ├── UBUNTU_READY.md           # Ubuntu 就绪清单
│   ├── INSTALLATION.md           # 通用安装指南
│   ├── DEVELOPMENT.md            # 开发指南
│   ├── PROJECT_SUMMARY.md        # 项目总结
│   └── INDEX.md                  # 本文件
│
├── 🔧 工具
│   ├── ubuntu_install.sh         # Ubuntu Bash 安装脚本
│   ├── ubuntu_install.py         # Ubuntu Python 安装脚本
│   ├── check_env.py              # 环境检查工具
│   ├── build.sh                  # macOS/Linux 构建脚本
│   └── build.bat                 # Windows 构建脚本
│
├── ⚙️ 配置
│   ├── requirements.txt           # Python 依赖
│   ├── setup.py                   # 项目配置
│   ├── MDViewer.spec              # PyInstaller 配置
│   └── .gitignore                 # Git 忽略规则
│
└── 📄 其他
    ├── Workplan.md               # 项目计划
    ├── test_sample.md            # 测试示例文件
    └── resources/                # 资源目录
```

---

## 💡 按角色查找文档

### 👤 普通用户
- 想快速开始？→ [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md)
- 想了解功能？→ [README.md](README.md)
- 遇到问题？→ [UBUNTU_SETUP.md](UBUNTU_SETUP.md) 的故障排查
- 第一次使用？→ 按照上面"任务 1"的步骤

### 👨‍💻 开发者
- 想了解架构？→ [DEVELOPMENT.md](DEVELOPMENT.md)
- 想贡献代码？→ [DEVELOPMENT.md](DEVELOPMENT.md) 的"提交贡献"部分
- 想修改功能？→ [DEVELOPMENT.md](DEVELOPMENT.md) 的"常见任务"部分

### 🔧 系统管理员
- 想在服务器部署？→ [UBUNTU_SETUP.md](UBUNTU_SETUP.md)
- 想创建容器镜像？→ [UBUNTU_SETUP.md](UBUNTU_SETUP.md) 的"方案 3"
- 想系统集成？→ [INSTALLATION.md](INSTALLATION.md) 的"系统集成"

### 📦 维护者
- 想发布新版本？→ [DEVELOPMENT.md](DEVELOPMENT.md)
- 想了解项目状态？→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🔍 查找特定信息

### 安装相关
- 快速安装 → [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md)
- 详细安装 → [UBUNTU_SETUP.md](UBUNTU_SETUP.md)
- 故障排查 → [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md) 或 [UBUNTU_SETUP.md](UBUNTU_SETUP.md)

### 功能相关
- 打开文件 → [README.md](README.md) 的"使用"部分
- 导出 PDF → [README.md](README.md) 的"使用"部分
- 快捷键 → 任何文档中的"键盘快捷键"表格

### 开发相关
- 项目架构 → [DEVELOPMENT.md](DEVELOPMENT.md)
- 代码风格 → [DEVELOPMENT.md](DEVELOPMENT.md)
- 测试框架 → [DEVELOPMENT.md](DEVELOPMENT.md)

### 部署相关
- 创建可执行档 → [INSTALLATION.md](INSTALLATION.md) 或 [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md)
- 应用菜单集成 → [UBUNTU_SETUP.md](UBUNTU_SETUP.md)
- 容器化部署 → [UBUNTU_SETUP.md](UBUNTU_SETUP.md) 的"方案 3"

---

## 📞 获取帮助

### 第一步：自助
1. 运行 `python3 check_env.py`
2. 在上面的文档中查找相关部分
3. 检查 FAQ 和常见问题

### 第二步：查看日志
```bash
python src/main.py 2>&1 | tee mdviewer.log
```

### 第三步：社区
- 查看 GitHub Issues
- 提交 GitHub Discussions
- 创建 Pull Request

---

## ✨ 快速链接

**最常用的 3 个文件**
1. [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md) - 快速开始
2. [README.md](README.md) - 功能说明
3. [check_env.py](check_env.py) - 环境检查

**最常用的 3 个脚本**
1. [ubuntu_install.sh](ubuntu_install.sh) - 自动安装
2. [check_env.py](check_env.py) - 环境验证
3. [build.sh](build.sh) - 构建可执行档

**最常用的 3 个快捷键**
1. `Ctrl+O` - 打开文件
2. `Ctrl+E` - 导出 PDF
3. `Ctrl+Q` - 退出应用

---

## 📋 文件检查清单

本项目包含：
- ✅ 9 个 Python 模块
- ✅ 8 个用户文档
- ✅ 5 个安装/构建工具
- ✅ 1 个环境检查工具
- ✅ 39 个文件（总计）

---

## 🎯 推荐阅读顺序

### 新用户
1. [README.md](README.md) - 了解项目 (5 分钟)
2. [QUICK_START_UBUNTU.md](QUICK_START_UBUNTU.md) - 快速开始 (5 分钟)
3. 运行应用并尝试功能 (5 分钟)

### 开发者
1. [README.md](README.md) - 项目概览 (5 分钟)
2. [DEVELOPMENT.md](DEVELOPMENT.md) - 架构和指南 (20 分钟)
3. 浏览源代码 (30 分钟)

### 部署管理员
1. [UBUNTU_SETUP.md](UBUNTU_SETUP.md) - 完整指南 (15 分钟)
2. [ubuntu_install.sh](ubuntu_install.sh) - 自动安装 (5 分钟)
3. 测试部署流程 (10 分钟)

---

## 📝 版本信息

- **项目版本**: 0.1.0
- **文档版本**: 1.0
- **最后更新**: 2026-04-16
- **支持的 Python**: 3.10+
- **支持的系统**: Ubuntu 20.04+ (以及 macOS, Windows, Linux)

---

## 🚀 立即开始

```bash
# 最快的方法
cd ~/MDViewer
bash ubuntu_install.sh
```

祝您使用愉快！🎉

---

**需要帮助？** 查看本文档中的"获取帮助"部分，或阅读相关指南文档。
