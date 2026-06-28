# 📦 mac-pkg-history —— macOS PKG Install History TUI Viewer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos)

**mac-pkg-history** 是一个交互式命令行工具（TUI），用于查看 macOS 上通过 `.pkg` 安装包安装的所有软件及其详细文件清单。它基于系统自带的 `pkgutil` 命令，提供更直观、高效的浏览体验。

![image-20260628163038453](https://img.sky233.top/img/2026/06/09af3be103fb875fa2e93f885c27fedc7b6b1afb80ee83cee42c1d13821b69a5.png)


---

## ✨ 特性

- 📋 **全量扫描** – 自动列出所有已安装的 `.pkg` 包，显示标识符、版本和安装日期。
- 🔍 **快速检索** – 输入包 ID 的一部分即可模糊匹配，支持多选。
- 📂 **文件清单** – 查看指定包安装的所有文件路径（相当于 `pkgutil --files`）。
- 📄 **智能分页** – 文件较多时自动提供预览、`less` 分页器或跳过的选项。
- ⏱️ **时间排序** – 默认按安装时间正序排列，方便查看最近安装的包。
- 🔄 **刷新缓存** – 支持重新扫描系统（`r` 键），无需重启程序。
- 🎨 **美观界面** – 使用 [Rich](https://github.com/Textualize/rich) 库生成彩色表格和面板。

---

## 🚀 快速开始

### 前提条件

- macOS 10.13+（依赖 `pkgutil` 命令）
- Python 3.6 或更高版本
- （可选）`less` 分页器（系统自带）

### 安装

`pip install mac-pkg-history`

### 使用

启动后你会看到所有已安装包的表格。交互操作如下：

| 操作 | 说明 |
| :--- | :--- |
| 输入**包 ID 关键词** | 模糊匹配并查看详情（支持部分匹配） |
| 输入 `r` | 刷新列表（重新扫描系统） |
| 输入 `q` | 退出程序 |
| 在文件列表界面 | 选择 `1` 预览前30行，选择 `2` 用 `less` 分页查看，选择 `3` 跳过 |

---

## 🧩 原理与数据来源

本工具通过调用 macOS 内置的 `pkgutil` 命令获取数据：

- `pkgutil --pkgs` – 列出所有已安装包的标识符。
- `pkgutil --pkg-info <ID>` – 获取包的版本、安装时间戳等信息。
- `pkgutil --files <ID>` – 列出该包安装的所有文件路径（相对于根目录）。

所有数据均来自系统收据（receipts），不会修改任何系统文件，**只读安全**。

---

## 🛠️ 开发说明

### 技术栈

- **Python 3** – 核心逻辑
- **Rich** – TUI 渲染
- **subprocess** – 调用系统命令
- **datetime** – 时间戳转换

---

## 📝 声明

- **作者（Maintainer）**：[@Yalois](https://github.com/Yalois)
- **开发说明**：本项目在开发过程中借助了 AI 工具（DeepSeek）进行代码框架搭建和优化。所有功能整合、交互设计、测试及后续维护均由作者独立完成。
- **许可证**：MIT License – 你可以自由使用、修改、分发，但需保留版权声明。

---

## ⚠️ 免责声明

本工具仅用于查看系统安装记录，**不会**执行卸载或修改操作。请勿尝试通过本工具删除文件或收据，否则可能导致系统或应用程序异常。作者不对误操作造成的任何损失负责。

---

## 🙏 致谢

- [Rich](https://github.com/Textualize/rich) – 让终端变得如此多彩
- Apple 的 `pkgutil` – 提供了强大的包管理接口

---

**如果这个工具对你有帮助，请给它一个 ⭐ Star 支持一下！** 😊

---