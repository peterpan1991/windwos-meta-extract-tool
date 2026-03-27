# DJYMeta

元数据提取与审查工具，支持从图片(JPEG/PNG/TIFF)、PDF、音视频文件中提取元数据信息。

## 功能特性

- **图片元数据**: 提取 EXIF 数据，包括拍摄时间、GPS定位、设备型号、软件版本等
- **PDF元数据**: 提取文档标题、作者、页数、创建时间等
- **音视频元数据**: 提取时长、比特率、采样率、编码信息等
- **统一输出格式**: 支持美化输出和 JSON 格式

## 支持的文件格式

- 图片: JPEG, PNG, TIFF
- 文档: PDF
- 音频: MP3, FLAC, OGG, WAV, AAC, M4A, WMA
- 视频: MP4, MKV, AVI, MOV, WMV, WebM

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### GUI 界面 (推荐)

```bash
# 启动图形界面
python run_gui.py
```

GUI 界面提供以下功能:
- 文件浏览器选择文件
- 实时显示文件信息（文件名、类型、大小、修改时间）
- 一键提取元数据
- 支持美化和 JSON 两种输出格式
- 完整的元数据详情展示

### 命令行

```bash
# 基本用法
python -m src.main <文件路径>

# 指定文件类型
python -m src.main <文件路径> --type image

# JSON 格式输出
python -m src.main <文件路径> --style json
```

## 输出示例

```
============================================================
  文件: photo.jpg
  类型: IMAGE
  大小: 2.45 MB
============================================================
  创建时间: 2024-01-15 14:30:00
  分辨率: 4032 x 3024
  相机: Apple iPhone 15 Pro Max
  软件: iOS 17.2
  GPS: 39.904200, 116.407400
  曝光时间: 1/120
  光圈: f/1.78
  ISO: 80
  焦距: 6.86mm
============================================================
```

## 项目结构

```
DJYMeta/
├── src/
│   ├── __init__.py
│   ├── main.py              # 主程序入口
│   ├── extractors/          # 元数据提取器
│   │   ├── base.py          # 基础提取器抽象类
│   │   ├── image.py         # 图片元数据提取器
│   │   ├── pdf.py           # PDF元数据提取器
│   │   └── media.py         # 音视频元数据提取器
│   ├── models/              # 数据模型
│   │   └── metadata.py      # 元数据结构定义
│   └── utils/               # 工具函数
│       └── helpers.py       # 辅助函数
├── requirements.txt         # 依赖
├── SPEC.md                  # 规格说明
└── README.md               # 说明文档
```

## 依赖

- Pillow >= 10.0.0 (图片处理)
- pypdf >= 3.0.0 (PDF处理)
- mutagen >= 1.47.0 (音视频处理)
- python-dateutil >= 2.8.2 (日期处理)