import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import base64
import pyperclip

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("密码管理器")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 数据文件路径
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "passwords.json")
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # 主密码变量
        self.master_password = ""
        self.key = None
        
        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 密码生成标签页
        self.generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.generate_tab, text="生成密码")
        
        # 密码存储标签页
        self.store_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.store_tab, text="存储密码")
        
        # 密码查询标签页
        self.query_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.query_tab, text="查询密码")
        
        # 初始化标签页
        self.init_generate_tab()
        self.init_store_tab()
        self.init_query_tab()
        
        # 初始化主密码
        self.prompt_master_password()
    
    def prompt_master_password(self):
        """提示用户输入主密码"""
        master_window = tk.Toplevel(self.root)
        master_window.title("设置主密码")
        master_window.geometry("300x150")
        master_window.resizable(False, False)
        master_window.transient(self.root)
        master_window.grab_set()
        
        ttk.Label(master_window, text="请输入主密码（用于加密存储）：").pack(pady=10, padx=10)
        
        password_var = tk.StringVar()
        password_entry = ttk.Entry(master_window, textvariable=password_var, show="*")
        password_entry.pack(pady=5, padx=10, fill=tk.X)
        password_entry.focus()
        
        def set_master_password():
            self.master_password = password_var.get()
            if not self.master_password:
                messagebox.showerror("错误", "主密码不能为空！")
                return
            # 生成加密密钥
            self.key = PBKDF2(self.master_password, b"salt", dkLen=32)
            master_window.destroy()
        
        ttk.Button(master_window, text="确定", command=set_master_password).pack(pady=10)
        
        # 按Enter键确认
        master_window.bind('<Return>', lambda event: set_master_password())
    
    def init_generate_tab(self):
        """初始化密码生成标签页"""
        frame = ttk.LabelFrame(self.generate_tab, text="密码生成设置")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 密码长度设置
        length_frame = ttk.Frame(frame)
        length_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(length_frame, text="密码长度：").pack(side=tk.LEFT, padx=5)
        self.length_var = tk.IntVar(value=16)
        length_spinbox = ttk.Spinbox(length_frame, from_=8, to=50, textvariable=self.length_var, width=5)
        length_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 密码复杂度设置
        complexity_frame = ttk.Frame(frame)
        complexity_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(complexity_frame, text="包含大写字母", variable=self.uppercase_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(complexity_frame, text="包含小写字母", variable=self.lowercase_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(complexity_frame, text="包含数字", variable=self.digits_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(complexity_frame, text="包含特殊字符", variable=self.special_var).pack(side=tk.LEFT, padx=5)
        
        # 生成密码按钮
        generate_button = ttk.Button(frame, text="生成密码", command=self.generate_password)
        generate_button.pack(pady=10)
        
        # 生成的密码显示
        password_frame = ttk.Frame(frame)
        password_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(password_frame, text="生成的密码：").pack(anchor=tk.W, pady=5)
        self.generated_password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.generated_password_var, state="readonly")
        password_entry.pack(fill=tk.X, pady=5)
        
        # 复制按钮
        copy_button = ttk.Button(password_frame, text="复制到剪贴板", command=self.copy_password)
        copy_button.pack(side=tk.RIGHT, pady=5)
    
    def generate_password(self):
        """生成强密码"""
        length = self.length_var.get()
        
        # 构建字符集
        char_set = ""
        if self.uppercase_var.get():
            char_set += string.ascii_uppercase
        if self.lowercase_var.get():
            char_set += string.ascii_lowercase
        if self.digits_var.get():
            char_set += string.digits
        if self.special_var.get():
            char_set += string.punctuation
        
        if not char_set:
            messagebox.showerror("错误", "至少选择一种字符类型！")
            return
        
        # 生成密码
        password = ''.join(random.choice(char_set) for _ in range(length))
        self.generated_password_var.set(password)
    
    def copy_password(self):
        """复制生成的密码到剪贴板"""
        password = self.generated_password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("成功", "密码已复制到剪贴板！")
        else:
            messagebox.showerror("错误", "没有可复制的密码！")
    
    def init_store_tab(self):
        """初始化密码存储标签页"""
        frame = ttk.LabelFrame(self.store_tab, text="存储密码")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 账户描述
        desc_frame = ttk.Frame(frame)
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(desc_frame, text="账户描述：").pack(side=tk.LEFT, padx=5)
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(desc_frame, textvariable=self.desc_var)
        desc_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # 用户名
        user_frame = ttk.Frame(frame)
        user_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(user_frame, text="用户名：").pack(side=tk.LEFT, padx=5)
        self.user_var = tk.StringVar()
        user_entry = ttk.Entry(user_frame, textvariable=self.user_var)
        user_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # 密码
        pass_frame = ttk.Frame(frame)
        pass_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(pass_frame, text="密码：").pack(side=tk.LEFT, padx=5)
        self.pass_var = tk.StringVar()
        pass_entry = ttk.Entry(pass_frame, textvariable=self.pass_var, show="*")
        pass_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # 使用生成的密码按钮
        use_generated_button = ttk.Button(frame, text="使用生成的密码", command=self.use_generated_password)
        use_generated_button.pack(pady=5)
        
        # 存储按钮
        store_button = ttk.Button(frame, text="存储密码", command=self.store_password)
        store_button.pack(pady=10)
    
    def use_generated_password(self):
        """使用生成的密码"""
        generated_password = self.generated_password_var.get()
        if generated_password:
            self.pass_var.set(generated_password)
        else:
            messagebox.showerror("错误", "请先生成密码！")
    
    def store_password(self):
        """存储密码"""
        desc = self.desc_var.get()
        user = self.user_var.get()
        password = self.pass_var.get()
        
        if not desc or not password:
            messagebox.showerror("错误", "账户描述和密码不能为空！")
            return
        
        # 加密密码
        encrypted_password = self.encrypt_password(password)
        
        # 读取现有数据
        data = self.load_data()
        
        # 添加新密码
        data[desc] = {
            "username": user,
            "password": encrypted_password
        }
        
        # 保存数据
        self.save_data(data)
        
        # 清空输入
        self.desc_var.set("")
        self.user_var.set("")
        self.pass_var.set("")
        
        messagebox.showinfo("成功", "密码存储成功！")
    
    def init_query_tab(self):
        """初始化密码查询标签页"""
        frame = ttk.LabelFrame(self.query_tab, text="查询密码")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 搜索框
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="搜索：").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # 搜索按钮
        search_button = ttk.Button(frame, text="搜索", command=self.search_password)
        search_button.pack(pady=5)
        
        # 结果列表
        result_frame = ttk.Frame(frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(result_frame, text="搜索结果：").pack(anchor=tk.W, pady=5)
        
        # 树状视图
        columns = ("desc", "username", "password")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        self.tree.heading("desc", text="账户描述")
        self.tree.heading("username", text="用户名")
        self.tree.heading("password", text="密码")
        
        self.tree.column("desc", width=200)
        self.tree.column("username", width=150)
        self.tree.column("password", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 复制密码按钮
        copy_pass_button = ttk.Button(frame, text="复制选中密码", command=self.copy_selected_password)
        copy_pass_button.pack(side=tk.RIGHT, pady=5)
        
        # 显示所有密码
        self.show_all_passwords()
    
    def search_password(self):
        """搜索密码"""
        search_term = self.search_var.get().lower()
        data = self.load_data()
        
        # 清空树状视图
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 搜索并显示结果
        for desc, info in data.items():
            if search_term in desc.lower() or search_term in info["username"].lower():
                decrypted_password = self.decrypt_password(info["password"])
                self.tree.insert("", tk.END, values=(desc, info["username"], decrypted_password))
    
    def show_all_passwords(self):
        """显示所有密码"""
        data = self.load_data()
        
        # 清空树状视图
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 显示所有密码
        for desc, info in data.items():
            decrypted_password = self.decrypt_password(info["password"])
            self.tree.insert("", tk.END, values=(desc, info["username"], decrypted_password))
    
    def copy_selected_password(self):
        """复制选中的密码"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("错误", "请先选择一个密码！")
            return
        
        item = selected_items[0]
        password = self.tree.item(item, "values")[2]
        
        pyperclip.copy(password)
        messagebox.showinfo("成功", "密码已复制到剪贴板！")
    
    def encrypt_password(self, password):
        """加密密码"""
        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted = cipher.encrypt(pad(password.encode(), AES.block_size))
        return base64.b64encode(iv + encrypted).decode()
    
    def decrypt_password(self, encrypted_password):
        """解密密码"""
        data = base64.b64decode(encrypted_password)
        iv = data[:16]
        encrypted = data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode()
    
    def load_data(self):
        """加载数据"""
        if not os.path.exists(self.data_file):
            return {}
        
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    
    def save_data(self, data):
        """保存数据"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
