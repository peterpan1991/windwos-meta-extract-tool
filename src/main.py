"""DJYMeta 主程序入口"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from src.extractors.image import ImageExtractor
from src.extractors.pdf import PDFExtractor
from src.extractors.media import MediaExtractor
from src.models.metadata import Metadata
from src.utils.helpers import format_file_size, format_duration, format_bitrate


class MetadataExtractor:
    """元数据提取器管理器"""

    EXTRACTORS = [ImageExtractor(), PDFExtractor(), MediaExtractor()]

    def __init__(self):
        self.extractors = self.EXTRACTORS

    def extract(self, file_path: str, file_type: str = None) -> Optional[Metadata]:
        """提取文件元数据

        Args:
            file_path: 文件路径
            file_type: 文件类型 (image/pdf/media), 如果为None则自动检测

        Returns:
            元数据对象，失败返回None
        """
        path = Path(file_path)
        if not path.exists():
            print(f"[ERROR] 文件不存在: {file_path}")
            return None

        # 根据文件类型选择提取器
        if file_type:
            return self._extract_by_type(file_path, file_type)

        # 自动检测文件类型
        for extractor in self.extractors:
            if extractor.can_extract(file_path):
                return extractor.extract(file_path)

        print(f"[ERROR] 不支持的文件类型: {path.suffix}")
        return None

    def _extract_by_type(self, file_path: str, file_type: str) -> Optional[Metadata]:
        """根据指定类型提取

        Args:
            file_path: 文件路径
            file_type: 文件类型

        Returns:
            元数据对象
        """
        type_map = {
            "image": ImageExtractor(),
            "pdf": PDFExtractor(),
            "media": MediaExtractor(),
        }

        extractor = type_map.get(file_type.lower())
        if extractor:
            return extractor.extract(file_path)

        print(f"[ERROR] 未知的文件类型: {file_type}")
        return None


def format_output(metadata: Metadata, style: str = "pretty") -> str:
    """格式化输出

    Args:
        metadata: 元数据对象
        style: 输出样式 (pretty/json)

    Returns:
        格式化的字符串
    """
    if style == "json":
        return json.dumps(metadata.to_dict(), ensure_ascii=False, indent=2)

    # 美化输出
    lines = []
    lines.append("=" * 60)
    lines.append(f"  文件: {metadata.file_name}")
    lines.append(f"  类型: {metadata.file_type.upper()}")
    lines.append(f"  大小: {format_file_size(metadata.file_size)}" if metadata.file_size else "  大小: 未知")
    lines.append("=" * 60)

    # 基础信息
    if metadata.created_time:
        lines.append(f"  创建时间: {metadata.created_time}")
    if metadata.modified_time:
        lines.append(f"  修改时间: {metadata.modified_time}")

    # 尺寸信息 (图片)
    if metadata.width and metadata.height:
        lines.append(f"  分辨率: {metadata.width} x {metadata.height}")

    # EXIF 信息
    if metadata.camera_make or metadata.camera_model:
        camera = f"{metadata.camera_make} {metadata.camera_model}".strip()
        lines.append(f"  相机: {camera}")

    if metadata.software:
        lines.append(f"  软件: {metadata.software}")

    # GPS 信息
    if metadata.has_gps():
        lines.append(f"  GPS: {metadata.gps_latitude}, {metadata.gps_longitude}")
        if metadata.gps_altitude:
            lines.append(f"  海拔: {metadata.gps_altitude}m")

    # PDF 信息
    if metadata.file_type == "pdf":
        if metadata.pdf_title:
            lines.append(f"  标题: {metadata.pdf_title}")
        if metadata.pdf_author:
            lines.append(f"  作者: {metadata.pdf_author}")
        if metadata.pdf_page_count:
            lines.append(f"  页数: {metadata.pdf_page_count}")
        if metadata.pdf_producer:
            lines.append(f"  生产者: {metadata.pdf_producer}")

    # 音视频信息
    if metadata.file_type == "media":
        if metadata.duration:
            lines.append(f"  时长: {format_duration(metadata.duration)}")
        if metadata.bitrate:
            lines.append(f"  比特率: {format_bitrate(metadata.bitrate)}")
        if metadata.sample_rate:
            lines.append(f"  采样率: {metadata.sample_rate} Hz")
        if metadata.channels:
            channels_str = {1: "单声道", 2: "立体声"}.get(metadata.channels, str(metadata.channels))
            lines.append(f"  声道: {channels_str}")
        if metadata.codec:
            lines.append(f"  编码: {metadata.codec}")

    # 其他 EXIF 信息
    if metadata.exposure_time:
        lines.append(f"  曝光时间: {metadata.exposure_time}")
    if metadata.f_number:
        lines.append(f"  光圈: f/{metadata.f_number}")
    if metadata.iso:
        lines.append(f"  ISO: {metadata.iso}")
    if metadata.focal_length:
        lines.append(f"  焦距: {metadata.focal_length}")

    # 额外信息
    if metadata.extra and len(metadata.extra) <= 5:
        lines.append("\n  其他信息:")
        for key, value in metadata.extra.items():
            if value and len(str(value)) < 50:
                lines.append(f"    {key}: {value}")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="DJYMeta - 元数据提取与审查工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python -m src.main file.jpg
  python -m src.main document.pdf --style json
  python -m src.main video.mp4 --type media
        """
    )

    parser.add_argument("file", help="要提取元数据的文件路径")
    parser.add_argument("--type", "-t", choices=["image", "pdf", "media"],
                        help="指定文件类型 (默认自动检测)")
    parser.add_argument("--style", "-s", choices=["pretty", "json"], default="pretty",
                        help="输出样式 (默认: pretty)")
    parser.add_argument("--version", "-v", action="version", version="DJYMeta 1.0.0")

    args = parser.parse_args()

    # 创建提取器并提取元数据
    extractor = MetadataExtractor()
    metadata = extractor.extract(args.file, args.type)

    if metadata:
        print(format_output(metadata, args.style))
        return 0
    else:
        print("[ERROR] 提取元数据失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())