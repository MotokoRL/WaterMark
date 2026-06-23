import streamlit as st
import fitz
from PIL import Image, ImageDraw, ImageFont
import io
import tempfile
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "SourceHanSansCN-Normal.ttf")

def create_safe_wm_image(text, font_size, color, opacity):
    test_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(test_img)

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except Exception as e:
        st.error(f"字体加载失败：{e}")
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    padding = 10
    img = Image.new("RGBA", (tw + padding, th + padding), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    fill_color = (*color, int(255 * opacity))
    d.text((padding // 2, padding // 2), text, font=font, fill=fill_color)

    rotated_img = img.rotate(45, expand=True, resample=Image.BICUBIC)

    img_byte_arr = io.BytesIO()
    rotated_img.save(img_byte_arr, format="PNG")

    return img_byte_arr.getvalue(), rotated_img.width, rotated_img.height


def add_tiled_watermark(input_pdf, output_pdf, text, horiz_grid, vert_grid, opacity, color_rgb, font_size, offset_percent):
    doc = fitz.open(input_pdf)

    wm_bytes, wm_w, wm_h = create_safe_wm_image(
        text, font_size, color_rgb, opacity
    )

    for page in doc:
        w, h = page.rect.width, page.rect.height

        step_x = max(10, horiz_grid)
        step_y = max(10, vert_grid)

        row_count = 0
        current_offset_x = step_x * (offset_percent / 100) if offset_percent > 0 else 0

        start_x = -wm_w + ((w + wm_w) % step_x) /2
        start_y = -wm_h + ((h + wm_h) % step_y) /2

        y = start_y
        row_count = 0

        while y < h + wm_h:
            row_count += 1
            row_offset_x = current_offset_x if row_count % 2 == 0 else 0

            x = start_x
            while x < w + wm_w:
                final_x = x + row_offset_x
                rect = fitz.Rect(final_x, y, final_x + wm_w, y + wm_h)
                page.insert_image(rect, stream=wm_bytes)
                x += step_x

            y += step_y

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()

st.title("PDF 水印工具")

uploaded_file = st.file_uploader("上传 PDF 文件", type=["pdf"])

watermark_text = st.text_input("水印内容", "本材料仅供【】阅览")

font_size = st.slider("字体大小", 10, 100, 24)
opacity = st.slider("不透明度 (%)", 5, 100, 20) / 100
horiz_grid = st.slider("水平间距：越小越密", 30, 500, 166)
vert_grid = st.slider("垂直间距：越小越密", 30, 500, 197)
offset_percent = st.slider("错位平铺 (%)", 0, 100, 0)

color = st.color_picker("水印颜色", "#B3B3B3")
color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

if uploaded_file and st.button("生成 PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(uploaded_file.read())
        input_path = input_tmp.name

    output_path = input_path.replace(".pdf", "-watermark.pdf")

    try:
        add_tiled_watermark(
            input_path,
            output_path,
            watermark_text,
            horiz_grid,
            vert_grid,
            opacity,
            color_rgb,
            font_size,
            offset_percent,
        )

        with open(output_path, "rb") as f:
            original_name = uploaded_file.name
            name_without_ext = os.path.splitext(original_name)[0]
            download_name = f"{name_without_ext}-watermark.pdf"

            st.success("处理完成")
            st.download_button(
                "下载加水印后的 PDF",
                data=f,
                file_name=download_name,
                mime="application/pdf",
            )

    except Exception as e:
        st.error(f"处理失败：{e}")

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
