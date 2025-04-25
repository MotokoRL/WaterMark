# WaterMarkMaker

A Python GUI application for adding watermarks to PowerPoint (.pptx), and PDF files.

## Features

- Add customizable text watermarks to documents
- Supports multiple file formats: PPTX, PDF
- Adjustable watermark properties:
  - Text content
  - Font style and size
  - Color (RGB values)
  - Transparency (0.0-1.0)
  - Density (1-10)
- Simple graphical interface

## Requirements

- Python 3.6+
- Required packages:
  - tkinter (usually included with Python)
  - Pillow (`pip install pillow`)
  - python-pptx (`pip install python-pptx`)
  - PyPDF2 (`pip install pypdf2`)
  - reportlab (`pip install reportlab`)

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```bash
   pip install pillow python-docx python-pptx pypdf2 reportlab
   ```

## Usage

1. Run the application:
   ```bash
   python WaterMarkMaker.py
   ```

2. The application window will appear with the following fields:

   ![Application Screenshot](screenshot.png)

   - **Input File**: Select the document you want to watermark
   - **Save Path**: Choose where to save the watermarked file
   - **Watermark Text**: Enter the text you want to use as watermark
   - **Font File**: Select a .ttf font file
   - **Font Size**: Set the font size (e.g., 24)
   - **Font Color**: Enter RGB values (e.g., "200,200,200" for light gray)
   - **Opacity**: Set transparency (0.0 = fully transparent, 1.0 = fully opaque)
   - **Density**: Control how densely the watermark is repeated (1-10)

3. Click "Add Watermark" to process the file

## Supported File Formats

- **PowerPoint (.pptx)**: Watermark appears on all slides
- **PDF**: Watermark appears diagonally across each page

## Example Usage

1. Adding a confidential notice to a PDF:
   - Text: "CONFIDENTIAL"
   - Font: Times New Roman
   - Size: 36
   - Color: 255,0,0 (red)
   - Opacity: 0.5
   - Density: 5

## Notes

- For best results with PDFs, use a TrueType (.ttf) font file
- Higher density values will create more watermark repetitions
- The application will validate all inputs before processing

## Troubleshooting

- If you get font-related errors, try a different .ttf font file
- Make sure the output file path has the correct extension (.pptx, or .pdf)
- For large PDF files, processing may take some time