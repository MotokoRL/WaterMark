# PDF Watermark Tool

A simple web-based PDF watermark tool built with **Python** and **Streamlit**.

Upload a PDF, customize watermark text and styling, then download the processed file.

## Features

- Upload PDF files
- Add tiled text watermarks
- Customize watermark text
- Adjust font size
- Adjust opacity
- Change watermark color
- Control horizontal / vertical spacing
- Offset tiling for better coverage
- Auto-download as `original_filename-watermark.pdf`

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- Pillow

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run WaterMarkMaker.py
```

## Usage

1. Upload a PDF  
2. Set watermark text and style  
3. Click **Generate PDF**  
4. Download the processed file  

## Deployment

This app can be deployed easily on **Streamlit Cloud**.

## Notes

- Supports Chinese watermark text
- Built-in Chinese font included
- Works on desktop and mobile browsers
