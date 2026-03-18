# 🛡️ PDF Watermark Master | PDF 批量水印大师
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
