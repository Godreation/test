import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import cv2
import os

class QRCodeTool:
    def __init__(self, root):
        self.root = root
        self.root.title("二维码生成器与读取器")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 生成的二维码图像
        self.qr_image = None
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标签页
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 生成二维码标签页
        self.generate_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.generate_frame, text="生成二维码")
        
        # 读取二维码标签页
        self.read_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.read_frame, text="读取二维码")
        
        # 初始化生成二维码标签页
        self.init_generate_tab()
        
        # 初始化读取二维码标签页
        self.init_read_tab()
    
    def init_generate_tab(self):
        # 输入区域
        input_frame = ttk.LabelFrame(self.generate_frame, text="输入文本", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.text_input = tk.Text(input_frame, height=5, width=50)
        self.text_input.pack(fill=tk.X, expand=True, pady=(0, 10))
        
        # 按钮区域
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        self.generate_btn = ttk.Button(button_frame, text="生成二维码", command=self.generate_qr)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(button_frame, text="保存二维码", command=self.save_qr)
        self.save_btn.pack(side=tk.LEFT)
        
        # 显示区域
        display_frame = ttk.LabelFrame(self.generate_frame, text="二维码预览", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.qr_canvas = tk.Canvas(display_frame, bg="white", width=300, height=300)
        self.qr_canvas.pack(fill=tk.BOTH, expand=True)
    
    def init_read_tab(self):
        # 按钮区域
        button_frame = ttk.Frame(self.read_frame)
        button_frame.pack(pady=10)
        
        self.read_btn = ttk.Button(button_frame, text="选择二维码图片", command=self.read_qr)
        self.read_btn.pack()
        
        # 显示区域
        display_frame = ttk.LabelFrame(self.read_frame, text="二维码图片", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.read_canvas = tk.Canvas(display_frame, bg="white", width=300, height=300)
        self.read_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 结果区域
        result_frame = ttk.LabelFrame(self.read_frame, text="读取结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=5, width=50)
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def generate_qr(self):
        # 获取输入文本
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "请输入要生成二维码的文本！")
            return
        
        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # 创建图像
        self.qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # 显示二维码
        self.display_qr(self.qr_image, self.qr_canvas)
    
    def display_qr(self, image, canvas):
        # 调整图像大小以适应画布
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # 如果画布大小为0，使用默认值
        if canvas_width == 1 or canvas_height == 1:
            canvas_width = 300
            canvas_height = 300
        
        # 转换PIL图像为Tkinter图像
        image = image.resize((canvas_width, canvas_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)
        
        # 保存图像引用，防止被垃圾回收
        canvas.tk_image = tk_image
        
        # 显示图像
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    
    def save_qr(self):
        if not self.qr_image:
            messagebox.showwarning("警告", "请先生成二维码！")
            return
        
        # 打开文件对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="保存二维码"
        )
        
        if file_path:
            try:
                self.qr_image.save(file_path)
                messagebox.showinfo("成功", f"二维码已保存到：{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
    
    def read_qr(self):
        # 打开文件对话框
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")],
            title="选择二维码图片"
        )
        
        if not file_path:
            return
        
        try:
            # 读取图像
            image = Image.open(file_path)
            
            # 显示图像
            self.display_qr(image, self.read_canvas)
            
            # 解码二维码
            decoded_objects = decode(image)
            if decoded_objects:
                result = "\n".join([obj.data.decode("utf-8") for obj in decoded_objects])
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, result)
            else:
                messagebox.showinfo("结果", "未检测到二维码！")
                self.result_text.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("错误", f"读取失败：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeTool(root)
    root.mainloop()