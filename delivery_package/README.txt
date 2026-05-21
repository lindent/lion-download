# Temu 图片下载工具 - 使用说明

## 📦 交付内容

本文件夹包含完整的 Temu 图片下载工具源代码和打包脚本。

### 文件说明

- `temu_downloader.py` - 主程序源代码
- `build.bat` - 一键打包脚本（生成exe文件）
- `run.bat` - 快速启动脚本（需要先安装Python）
- `temu_data_1778315436173.txt` - 示例数据文件
- `requirements.txt` - Python依赖文件

---

## 🚀 快速开始

### 方法一：直接运行Python脚本（推荐）

1. 确保Windows系统已安装Python 3.8或更高版本
   - 下载地址：https://www.python.org/downloads/
   - 安装时请勾选 "Add Python to PATH"

2. 双击运行 `run.bat`

### 方法二：打包成exe独立程序

1. 确保Windows系统已安装Python 3.8或更高版本

2. 双击运行 `build.bat`

3. 等待打包完成（通常需要3-5分钟）

4. 打包完成后，exe文件位于：
   ```
   dist\TemuDownloader\TemuDownloader.exe
   ```

5. 将整个 `TemuDownloader` 文件夹复制到目标电脑即可使用
   - 无需安装Python
   - 无需安装任何依赖

---

## 📖 使用说明

1. **选择输出目录**：点击"浏览..."按钮，选择图片保存位置

2. **选择数据文件**：
   - 方法一：点击"选择文件..."按钮，选择txt文件
   - 方法二：直接将txt文件拖放到虚线框区域

3. **开始下载**：点击"开始下载"按钮

4. **查看进度**：日志区域实时显示下载进度

5. **停止下载**：如需中途停止，点击"停止"按钮

---

## 📋 数据文件格式

输入文件每行格式：
```
ID-----图片URL-----产品描述
```

使用 `-----` (5个连字符) 作为分隔符

### 示例：
```
601101871919552-----https://img.kwcdn.com/product/...-----Men'S Fashion 3D Funny Dog Pattern Shirt
```

---

## 📁 输出目录结构

程序会为每个产品创建独立目录：
```
输出根目录/
├── 601101871919552/
│   ├── image.jpg
│   └── description.txt
├── 601099567193312/
│   ├── image.jpg
│   └── description.txt
└── ...
```

---

## ⚠️ 常见问题

### Q: 运行时报错"找不到Python"
**A**: 请先安装Python，并确保安装时勾选了"Add Python to PATH"

### Q: 打包时报错
**A**: 
1. 确保网络连接正常
2. 确保有足够的磁盘空间（至少2GB）
3. 尝试以管理员身份运行 build.bat

### Q: 下载失败
**A**: 
1. 检查网络连接
2. 检查图片URL是否有效
3. 部分图片可能已失效，请查看日志中的错误信息

---

## 🔧 技术规格

- **编程语言**: Python 3.8+
- **GUI框架**: tkinter (Python内置)
- **打包工具**: PyInstaller
- **支持的操作系统**: Windows 10/11

---

## 📞 技术支持

如有问题，请联系开发者。

---

*最后更新: 2026-05-21*
