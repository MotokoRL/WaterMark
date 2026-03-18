# 🛡️ PDF Watermark Master | PDF 批量水印大师

## 🇬🇧 English Description
---

A lightweight Python-based desktop tool designed to add **45-degree tilted tiled** Chinese/English watermarks to PDF files. Ideal for protecting venture capital (VC) investment agreements, commercial contracts, and internal confidential documents.

### ✨ Key Features
- **🚀 Batch Processing**: Select multiple PDF files from different folders for one-click watermarking.
- **🎨 High Customization**:
  - **Content**: Custom watermark text (supports Unicode/Chinese).
  - **Appearance**: Built-in color picker, adjustable opacity, and font size.
  - **Layout**: Adjustable grid density with auto-spacing to prevent text overlap.
- **🛡️ High Compatibility**: 
  - **Chinese Support**: Automatically uses system fonts (Microsoft YaHei/SimSun) to prevent gibberish.
  - **45° Rotation**: Uses matrix transformation to bypass rotation bugs in older PDF libraries.
- **📂 Unified Output**: Processed files are saved to a designated folder with a `-watermark` suffix.

### 🚀 Quick Start
1. **Run Source Code**:
   ```bash
   pip install pymupdf
   python watermark.py


🇨🇳 中文说明

一个基于 Python 开发的轻量级桌面工具，专门用于为 PDF 文件添加 45度倾斜平铺 的水印。特别适用于 VC 投资协议、商业合同、内部机密文档的防篡改与版权保护。

✨ 核心功能
🚀 批量处理：支持从不同文件夹选择多个 PDF 文件进行一键加水印。

🎨 高度自定义：

内容：自由输入中英文水印文字。

外观：内置调色盘，支持自定义颜色、透明度、字体大小。

布局：支持调节网格间距（密度），自动防止文字重叠。

🛡️ 兼容性强：

中文支持：自动调用系统微软雅黑/宋体，确保不乱码。

45度旋转：采用矩阵变形技术，规避了部分 PDF 库无法旋转非 90 度倍数的 Bug。

📂 指定输出：所有处理后的文件可统一保存到指定文件夹，并自动添加 -watermark 后缀。

🚀 快速开始
运行源代码:

Bash
pip install pymupdf
python watermark.py
