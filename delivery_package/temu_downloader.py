# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import urllib.request
import urllib.error
import ssl
import time
from pathlib import Path

class TemuDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temu 图片下载工具")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        self.output_dir = tk.StringVar()
        self.input_file = tk.StringVar()
        self.is_downloading = False
        self.stop_flag = threading.Event()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Temu 图片下载工具", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=(0, 15))
        
        dir_frame = ttk.LabelFrame(main_frame, text="输出目录", padding="10")
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        dir_input_frame = ttk.Frame(dir_frame)
        dir_input_frame.pack(fill=tk.X)
        
        self.dir_entry = ttk.Entry(dir_input_frame, textvariable=self.output_dir)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(dir_input_frame, text="浏览...", command=self.browse_output_dir)
        browse_btn.pack(side=tk.RIGHT)
        
        file_frame = ttk.LabelFrame(main_frame, text="输入文件 (支持拖放)", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_input_frame = ttk.Frame(file_frame)
        file_input_frame.pack(fill=tk.X)
        
        self.file_entry = ttk.Entry(file_input_frame, textvariable=self.input_file)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        select_btn = ttk.Button(file_input_frame, text="选择文件...", command=self.select_input_file)
        select_btn.pack(side=tk.RIGHT)
        
        self.drop_label = ttk.Label(file_frame, text="将txt文件拖放到此处", 
                                     background="#e0e0e0", foreground="#666666",
                                     font=("微软雅黑", 9))
        self.drop_label.pack(fill=tk.X, pady=(10, 0))
        self.drop_label.bind("<Button-1>", lambda e: self.select_input_file())
        
        self.setup_drag_drop(file_frame)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_btn = ttk.Button(control_frame, text="开始下载", command=self.start_download)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="停止", command=self.stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
        
        self.progress_label = ttk.Label(control_frame, text="就绪")
        self.progress_label.pack(side=tk.RIGHT)
        
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD, 
                                 font=("Consolas", 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="请选择输出目录和输入文件", 
                                       foreground="#666666")
        self.status_label.pack(side=tk.LEFT)
        
    def setup_drag_drop(self, parent):
        def on_drag_enter(event):
            self.drop_label.config(background="#c0c0c0")
            
        def on_drag_leave(event):
            self.drop_label.config(background="#e0e0e0")
            
        def on_drop(event):
            self.drop_label.config(background="#e0e0e0")
            try:
                data = event.data
                if data.endswith('.txt') and os.path.isfile(data):
                    self.input_file.set(data)
                    self.log(f"已选择文件: {data}")
                else:
                    self.log("警告: 请拖放txt文件")
            except Exception as e:
                self.log(f"拖放错误: {str(e)}")
        
        self.drop_label.bind("<DragEnter>", on_drag_enter)
        self.drop_label.bind("<DragLeave>", on_drag_leave)
        
        parent.bind("<Drop>", on_drop)
        parent.bind("<DragOver>", lambda e: "break")
        
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)
            self.log(f"已选择输出目录: {directory}")
            
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="选择数据文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.input_file.set(file_path)
            self.log(f"已选择文件: {file_path}")
            
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_download(self):
        output_dir = self.output_dir.get().strip()
        input_file = self.input_file.get().strip()
        
        if not output_dir:
            messagebox.showwarning("警告", "请选择输出目录")
            return
            
        if not input_file:
            messagebox.showwarning("警告", "请选择输入文件")
            return
            
        if not os.path.exists(input_file):
            messagebox.showerror("错误", "输入文件不存在")
            return
            
        self.is_downloading = True
        self.stop_flag.clear()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=self.download_worker, args=(output_dir, input_file))
        thread.daemon = True
        thread.start()
        
    def stop_download(self):
        self.stop_flag.set()
        self.log("正在停止...")
        
    def download_worker(self, output_dir, input_file):
        try:
            self.log(f"开始处理文件: {input_file}")
            self.log(f"输出目录: {output_dir}")
            self.log("-" * 50)
            
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            total = len(lines)
            success = 0
            failed = 0
            
            for index, line in enumerate(lines, 1):
                if self.stop_flag.is_set():
                    self.log("下载已停止")
                    break
                    
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split('-----')
                if len(parts) < 3:
                    self.log(f"[{index}/{total}] 跳过格式错误的行")
                    failed += 1
                    continue
                    
                product_id = parts[0].strip()
                url = parts[1].strip()
                description = parts[2].strip()
                
                product_dir = os.path.join(output_dir, product_id)
                
                try:
                    os.makedirs(product_dir, exist_ok=True)
                    self.log(f"[{index}/{total}] 创建目录: {product_id}")
                    
                    image_ext = self.get_image_extension(url)
                    image_path = os.path.join(product_dir, f"image{image_ext}")
                    
                    if self.download_image(url, image_path):
                        self.log(f"  └── 下载图片成功")
                    else:
                        self.log(f"  └── 下载图片失败")
                        failed += 1
                        continue
                    
                    desc_path = os.path.join(product_dir, "description.txt")
                    with open(desc_path, 'w', encoding='utf-8') as df:
                        df.write(description)
                    self.log(f"  └── 保存描述成功")
                    
                    success += 1
                    
                except Exception as e:
                    self.log(f"  └── 错误: {str(e)}")
                    failed += 1
                    
                self.update_progress(index, total, success, failed)
                
            self.log("-" * 50)
            self.log(f"下载完成! 成功: {success}, 失败: {failed}, 总计: {total}")
            messagebox.showinfo("完成", f"下载完成!\n成功: {success}\n失败: {failed}")
            
        except Exception as e:
            self.log(f"错误: {str(e)}")
            messagebox.showerror("错误", str(e))
        finally:
            self.is_downloading = False
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))
            
    def get_image_extension(self, url):
        if '.png' in url.lower():
            return '.png'
        elif '.gif' in url.lower():
            return '.gif'
        elif '.webp' in url.lower():
            return '.webp'
        else:
            return '.jpg'
            
    def download_image(self, url, save_path):
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                data = response.read()
                with open(save_path, 'wb') as f:
                    f.write(data)
                    
            return True
            
        except Exception as e:
            self.log(f"  └── 下载失败: {str(e)}")
            return False
            
    def update_progress(self, current, total, success, failed):
        progress_text = f"进度: {current}/{total} | 成功: {success} | 失败: {failed}"
        self.root.after(0, lambda: self.progress_label.config(text=progress_text))

def main():
    root = tk.Tk()
    app = TemuDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
