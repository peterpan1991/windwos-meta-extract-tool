"""DJYMeta GUI 窗口应用程序"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from pathlib import Path
from typing import Optional

from src.main import MetadataExtractor, format_output


class MetadataExtractorGUI:
    """元数据提取器图形界面"""

    def __init__(self, root: tk.Tk):
        """初始化GUI

        Args:
            root: Tkinter根窗口
        """
        self.root = root
        self.root.title("DJYMeta - 元数据提取工具")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)

        # 设置窗口图标（如果有）
        try:
            self.root.iconbitmap("icon.ico")
        except Exception:
            pass

        # 创建提取器
        self.extractor = MetadataExtractor()
        self.current_file_path: Optional[str] = None

        # 设置样式
        self._setup_styles()

        # 创建界面
        self._create_widgets()

        # 居中显示窗口
        self._center_window()

    def _setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 按钮样式
        style.configure('Primary.TButton',
                       font=('Microsoft YaHei UI', 10),
                       padding=10)

        # 标签样式
        style.configure('Title.TLabel',
                       font=('Microsoft YaHei UI', 12, 'bold'))

        style.configure('Info.TLabel',
                       font=('Microsoft YaHei UI', 9))

        style.configure('Hint.TLabel',
                       font=('Microsoft YaHei UI', 8),
                       foreground='#666666')

        # 文本框样式
        style.configure('Output.TText',
                       font=('Consolas', 10))

    def _create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(title_frame,
                                 text="DJYMeta - 元数据提取工具",
                                 style='Title.TLabel')
        title_label.pack(side=tk.TOP, pady=(0, 5))

        # 支持的文件格式提示
        formats_text = "支持格式: 图片(JPEG/PNG/TIFF) | 文档(PDF) | 音频(MP3/FLAC/OGG/WAV/AAC/M4A/WMA) | 视频(MP4/MKV/AVI/MOV/WMV/WebM)"
        hint_label = ttk.Label(title_frame,
                               text=formats_text,
                               style='Hint.TLabel')
        hint_label.pack(side=tk.TOP)

        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="选择文件", padding="15")
        file_frame.pack(fill=tk.X, pady=(0, 20))

        # 文件路径显示
        self.file_path_var = tk.StringVar()
        path_entry = ttk.Entry(file_frame,
                               textvariable=self.file_path_var,
                               font=('Microsoft YaHei UI', 9))
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        path_entry.configure(state='readonly')

        # 浏览按钮
        browse_btn = ttk.Button(file_frame,
                               text="浏览...",
                               command=self._browse_file,
                               style='Primary.TButton')
        browse_btn.pack(side=tk.LEFT)

        # 文件信息区域
        info_frame = ttk.LabelFrame(main_frame, text="文件信息", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))

        # 创建信息显示
        self.info_vars = {
            'file_name': tk.StringVar(value="文件名: -"),
            'file_type': tk.StringVar(value="类型: -"),
            'file_size': tk.StringVar(value="大小: -"),
            'modified_time': tk.StringVar(value="修改时间: -"),
        }

        for i, (key, var) in enumerate(self.info_vars.items()):
            label = ttk.Label(info_frame, textvariable=var, style='Info.TLabel')
            label.grid(row=i // 2, column=i % 2, sticky=tk.W, padx=20, pady=5)

        # 操作按钮区域
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 20))

        self.extract_btn = ttk.Button(action_frame,
                                      text="开始提取",
                                      command=self._extract_metadata,
                                      style='Primary.TButton',
                                      state=tk.DISABLED)
        self.extract_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = ttk.Button(action_frame,
                                    text="清空",
                                    command=self._clear_output)
        self.clear_btn.pack(side=tk.LEFT)

        # 输出格式选择
        format_frame = ttk.Frame(action_frame)
        format_frame.pack(side=tk.RIGHT)

        ttk.Label(format_frame, text="输出格式:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 5))

        self.output_format = tk.StringVar(value="pretty")
        pretty_radio = ttk.Radiobutton(format_frame,
                                       text="美化",
                                       variable=self.output_format,
                                       value="pretty")
        pretty_radio.pack(side=tk.LEFT, padx=5)

        json_radio = ttk.Radiobutton(format_frame,
                                     text="JSON",
                                     variable=self.output_format,
                                     value="json")
        json_radio.pack(side=tk.LEFT, padx=5)

        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="元数据详情", padding="15")
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(output_frame,
                                                     wrap=tk.WORD,
                                                     font=('Consolas', 10),
                                                     height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame,
                               textvariable=self.status_var,
                               relief=tk.SUNKEN,
                               anchor=tk.W,
                               padding=(5, 2))
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def _center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _browse_file(self):
        """浏览并选择文件"""
        file_types = [
            ("所有支持的文件", "*.jpg;*.jpeg;*.png;*.tiff;*.tif;*.pdf;*.mp3;*.flac;*.ogg;*.wav;*.aac;*.m4a;*.wma;*.mp4;*.mkv;*.avi;*.mov;*.wmv;*.webm"),
            ("图片文件", "*.jpg;*.jpeg;*.png;*.tiff;*.tif"),
            ("PDF文件", "*.pdf"),
            ("音频文件", "*.mp3;*.flac;*.ogg;*.wav;*.aac;*.m4a;*.wma"),
            ("视频文件", "*.mp4;*.mkv;*.avi;*.mov;*.wmv;*.webm"),
            ("所有文件", "*.*"),
        ]

        file_path = filedialog.askopenfilename(
            title="选择要提取元数据的文件",
            filetypes=file_types
        )

        if file_path:
            self.current_file_path = file_path
            self.file_path_var.set(file_path)
            self._update_file_info(file_path)
            self.extract_btn.configure(state=tk.NORMAL)
            self.status_var.set(f"已选择: {Path(file_path).name}")

    def _update_file_info(self, file_path: str):
        """更新文件信息显示

        Args:
            file_path: 文件路径
        """
        path = Path(file_path)
        file_size = path.stat().st_size

        # 格式化文件大小
        for unit in ['B', 'KB', 'MB', 'GB']:
            if file_size < 1024.0:
                size_str = f"{file_size:.2f} {unit}"
                break
            file_size /= 1024.0
        else:
            size_str = f"{file_size:.2f} TB"

        # 获取修改时间
        modified_time = Path(file_path).stat().st_mtime

        # 更新显示
        self.info_vars['file_name'].set(f"文件名: {path.name}")
        self.info_vars['file_type'].set(f"类型: {path.suffix.upper()}")
        self.info_vars['file_size'].set(f"大小: {size_str}")
        self.info_vars['modified_time'].set(f"修改时间: {modified_time:.0f}")

    def _extract_metadata(self):
        """提取元数据"""
        if not self.current_file_path:
            messagebox.showwarning("警告", "请先选择文件!")
            return

        self.extract_btn.configure(state=tk.DISABLED)
        self.status_var.set("正在提取元数据...")
        self.root.update()

        try:
            # 提取元数据
            metadata = self.extractor.extract(self.current_file_path)

            if metadata:
                # 格式化输出
                output = format_output(metadata, self.output_format.get())

                # 显示结果
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, output)

                self.status_var.set(f"提取成功! 文件: {metadata.file_name}")
                messagebox.showinfo("成功", "元数据提取成功!")
            else:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, "提取失败: 不支持的文件类型或文件损坏")
                self.status_var.set("提取失败")
                messagebox.showerror("错误", "提取元数据失败!")

        except Exception as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, f"错误: {str(e)}")
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"提取过程中发生错误:\n{str(e)}")

        finally:
            self.extract_btn.configure(state=tk.NORMAL)

    def _clear_output(self):
        """清空输出"""
        self.output_text.delete(1.0, tk.END)
        self.file_path_var.set("")
        self.current_file_path = None
        self.extract_btn.configure(state=tk.DISABLED)

        # 重置文件信息
        for var in self.info_vars.values():
            if var.get().startswith("文件名:"):
                var.set("文件名: -")
            elif var.get().startswith("类型:"):
                var.set("类型: -")
            elif var.get().startswith("大小:"):
                var.set("大小: -")
            elif var.get().startswith("修改时间:"):
                var.set("修改时间: -")

        self.status_var.set("已清空")


def main():
    """主函数"""
    root = tk.Tk()
    app = MetadataExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
