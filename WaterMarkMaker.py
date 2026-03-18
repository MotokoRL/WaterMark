import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import os

def get_chinese_font():
    windir = os.environ.get('WINDIR', 'C:/Windows')
    fonts = [os.path.join(windir, "Fonts", "msyh.ttc"), os.path.join(windir, "Fonts", "simsun.ttc")]
    for f in fonts:
        if os.path.exists(f): return f
    return None

current_color = (0.7, 0.7, 0.7)

def pick_color():
    global current_color
    color = colorchooser.askcolor(title="选择水印颜色")
    if color[1]:
        current_color = tuple(c/255 for c in color[0])
        color_button.config(bg=color[1])

def add_tiled_watermark(input_pdf, output_pdf, text, grid_size, opacity, color_rgb, font_size):
    try:
        doc = fitz.open(input_pdf)
        font_path = get_chinese_font()
        if not font_path: return False

        text_width = len(text) * font_size 
        safe_grid_x = max(grid_size, text_width * 1.2)
        safe_grid_y = max(grid_size, font_size * 4)

        for page in doc:
            w, h = page.rect.width, page.rect.height
            p1 = fitz.Point(0, 0)
            m = fitz.Matrix(45)
            
            for x in range(-int(w), int(w * 1.5), int(safe_grid_x)):
                for y in range(-int(h), int(h * 1.5), int(safe_grid_y)):
                    page.insert_text(
                        (x, y), text, fontsize=font_size, fontfile=font_path,
                        fontname="zh", color=color_rgb, fill_opacity=opacity, morph=(p1, m)
                    )
        doc.save(output_pdf)
        doc.close()
        return True
    except:
        return False

# --- 逻辑处理部分 ---
selected_files = []

def select_files():
    global selected_files
    files = filedialog.askopenfilenames(filetypes=[("PDF文件", "*.pdf")])
    if files:
        selected_files = list(files)
        file_label.config(text=f"已选择 {len(selected_files)} 个文件")

def select_output_dir():
    path = filedialog.askdirectory()
    if path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)

def start_batch_process():
    watermark_text = text_entry.get()
    output_dir = output_entry.get()
    
    if not selected_files:
        messagebox.showwarning("提示", "请先选择 PDF 文件")
        return
    if not output_dir:
        messagebox.showwarning("提示", "请选择保存目录")
        return

    opacity_val = opacity_slider.get() / 100
    grid_val = int(grid_slider.get())
    size_val = int(size_slider.get())

    success_count = 0
    for file_path in selected_files:
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        new_name = f"{name}-watermark{ext}"
        target_path = os.path.join(output_dir, new_name)
        
        if add_tiled_watermark(file_path, target_path, watermark_text, grid_val, opacity_val, current_color, size_val):
            success_count += 1

    messagebox.showinfo("完成", f"批量处理结束！\n成功：{success_count} 个\n保存位置：{output_dir}")

# --- UI 界面 ---
root = tk.Tk()
root.title("PDF 批量水印大师 v1.0")
root.geometry("500x650")

main_frame = tk.Frame(root, padx=30, pady=20)
main_frame.pack(expand=True, fill="both")

# 1. 选择多个文件
tk.Label(main_frame, text="1. 选择 PDF 文件 (支持多选):", font=("Arial", 10, "bold")).pack(anchor="w")
tk.Button(main_frame, text="点击选择多个文件", command=select_files).pack(fill="x", pady=5)
file_label = tk.Label(main_frame, text="未选择任何文件", fg="blue")
file_label.pack(anchor="w")

# 2. 选择输出目录
tk.Label(main_frame, text="2. 选择保存位置:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
output_frame = tk.Frame(main_frame)
output_frame.pack(fill="x", pady=5)
output_entry = tk.Entry(output_frame)
output_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
tk.Button(output_frame, text="浏览", command=select_output_dir).pack(side="right")

# 3. 水印设置
tk.Label(main_frame, text="3. 水印文字:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
text_entry = tk.Entry(main_frame)
text_entry.insert(0, "内部资料 严禁外传")
text_entry.pack(fill="x", pady=5)

color_button = tk.Button(main_frame, text="选择颜色", command=pick_color, bg="#B3B3B3")
color_button.pack(fill="x", pady=5)

tk.Label(main_frame, text="字体大小:").pack(anchor="w")
size_slider = tk.Scale(main_frame, from_=10, to=100, orient=tk.HORIZONTAL)
size_slider.set(20)
size_slider.pack(fill="x")

tk.Label(main_frame, text="不透明度 (%):").pack(anchor="w")
opacity_slider = tk.Scale(main_frame, from_=5, to=100, orient=tk.HORIZONTAL)
opacity_slider.set(20)
opacity_slider.pack(fill="x")

tk.Label(main_frame, text="网格间距:").pack(anchor="w")
grid_slider = tk.Scale(main_frame, from_=50, to=500, orient=tk.HORIZONTAL)
grid_slider.set(150)
grid_slider.pack(fill="x")

tk.Button(main_frame, text="🚀 开启批量处理", command=start_batch_process, bg="#0078D4", fg="white", font=("Arial", 12, "bold"), height=2).pack(fill="x", pady=30)

root.mainloop()
