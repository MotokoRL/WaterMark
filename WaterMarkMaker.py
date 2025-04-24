import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from pptx import Presentation
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color

def ask_for_watermark_details():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 获取水印内容
    watermark_text = simpledialog.askstring("输入水印内容", "请输入水印内容：")
    if not watermark_text:
        messagebox.showwarning("输入错误", "水印内容不能为空！")
        return None

    # 获取字体路径
    font_path = filedialog.askopenfilename(title="选择字体文件", filetypes=[("TrueType 字体", "*.ttf")])
    if not font_path:
        messagebox.showwarning("选择错误", "未选择字体文件！")
        return None

    # 获取字体大小
    try:
        font_size = int(simpledialog.askstring("输入字体大小", "请输入字体大小："))
    except ValueError:
        messagebox.showwarning("输入错误", "字体大小必须是整数！")
        return None

    # 获取字体颜色
    color_str = simpledialog.askstring("输入字体颜色", "请输入字体颜色（例如：255,0,0 表示红色）：")
    try:
        color = tuple(map(int, color_str.split(',')))
        if len(color) != 3 or any(c < 0 or c > 255 for c in color):
            raise ValueError
    except ValueError:
        messagebox.showwarning("输入错误", "颜色格式不正确！")
        return None

    # 获取透明度
    try:
        opacity = float(simpledialog.askstring("输入透明度", "请输入透明度（0.0 到 1.0）："))
        if not (0.0 <= opacity <= 1.0):
            raise ValueError
    except ValueError:
        messagebox.showwarning("输入错误", "透明度必须是 0.0 到 1.0 之间的数值！")
        return None

    # 获取密度
    try:
        density = int(simpledialog.askstring("输入密度", "请输入密度（1 到 10）："))
        if not (1 <= density <= 10):
            raise ValueError
    except ValueError:
        messagebox.showwarning("输入错误", "密度必须是 1 到 10 之间的整数！")
        return None

    return {
        "watermark_text": watermark_text,
        "font_path": font_path,
        "font_size": font_size,
        "color": color,
        "opacity": opacity,
        "density": density
    }

def add_watermark_to_image(image_path, watermark_details):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    watermark = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    font = ImageFont.truetype(watermark_details["font_path"], watermark_details["font_size"])

    text_width, text_height = draw.textsize(watermark_details["watermark_text"], font)
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    color_with_opacity = (*watermark_details["color"], int(watermark_details["opacity"] * 255))

    draw.text((x, y), watermark_details["watermark_text"], font=font, fill=color_with_opacity)

    watermarked_image = Image.alpha_composite(image, watermark)

    watermarked_image.save("watermarked_image.png", "PNG")

def add_watermark_to_pdf(pdf_path, watermark_details):
    output_pdf = PdfWriter()

    with open(pdf_path, "rb") as input_pdf:
        reader = PdfReader(input_pdf)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)
            c.setFont(watermark_details["font_path"], watermark_details["font_size"])

            c.setFillColor(Color(*watermark_details["color"], alpha=watermark_details["opacity"]))

            text_width = c.stringWidth(watermark_details["watermark_text"], watermark_details["font_path"], watermark_details["font_size"])
            text_height = watermark_details["font_size"]

            x = (letter[0] - text_width) / 2
            y = (letter[1] - text_height) / 2

            c.drawString(x, y, watermark_details["watermark_text"])

            c.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)
            page.merge_page(new_pdf.pages[0])

            output_pdf.add_page(page)

        with open("watermarked_pdf.pdf", "wb") as output_file:
            output_pdf.write(output_file)

def add_watermark_to_pptx(pptx_path, watermark_details):
    prs = Presentation(pptx_path)

    for slide in prs.slides:
        left = top = 0
        width = height = prs.slide_width
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = watermark_details["watermark_text"]

        for paragraph in text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.size = watermark_details["font_size"]
                run.font.name = watermark_details["font_path"]

        textbox.fill.solid()
        textbox.fill.fore_color.rgb = Color(*watermark_details["color"], alpha=watermark_details["opacity"])

    prs.save("watermarked_pptx.pptx")

def main():
    watermark_details = ask_for_watermark_details()
    if watermark_details is None:
        return

    file_path = filedialog.askopenfilename(title="选择文件", filetypes=[("Word 文件", "*.docx"), ("PowerPoint 文件", "*.pptx"), ("PDF 文件", "*.pdf")])
    if not file_path:
        messagebox.showwarning("选择错误", "未选择文件！")
        return

    if file_path.endswith(".docx