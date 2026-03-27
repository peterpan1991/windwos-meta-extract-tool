# DJYMeta 元数据提取与审查工具

## 项目概述
元数据提取与审查工具，支持从图片(JPEG/PNG/TIFF)、PDF、音视频文件中提取元数据信息。

## 功能特性
- 支持 JPEG/PNG/TIFF 图片的 EXIF 元数据提取
- 支持 PDF 文档元数据提取
- 支持音视频文件元数据提取
- 统一的元数据输出格式
- 简洁的命令行交互界面

## 技术栈
- Python 3.8+
- Pillow (图片处理)
- pypdf2 或 pypdf (PDF处理)
- mutagen (音视频处理)

## 项目结构
```
DJYMeta/
├── src/
│   ├── __init__.py
│   ├── main.py              # 主程序入口
│   ├── extractors/          # 元数据提取器
│   │   ├── __init__.py
│   │   ├── base.py          # 基础提取器抽象类
│   │   ├── image.py         # 图片元数据提取器
│   │   ├── pdf.py           # PDF元数据提取器
│   │   └── media.py         # 音视频元数据提取器
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   └── metadata.py      # 元数据结构定义
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── helpers.py       # 辅助函数
├── requirements.txt         # 依赖
└── README.md               # 说明文档
```

## 使用方法
```bash
python -m src.main <文件路径>
```