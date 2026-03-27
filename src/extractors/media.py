"""音视频元数据提取器"""
from datetime import datetime
from pathlib import Path
from typing import Optional

import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from mutagen.mp4 import MP4
from mutagen.m4a import M4A

from src.extractors.base import BaseExtractor
from src.models.metadata import Metadata


class MediaExtractor(BaseExtractor):
    """音视频元数据提取器"""

    SUPPORTED_EXTENSIONS = {
        ".mp3", ".flac", ".ogg", ".wav", ".aac", ".m4a", ".wma",
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"
    }

    def extract(self, file_path: str) -> Optional[Metadata]:
        """提取音视频元数据

        Args:
            file_path: 音视频文件路径

        Returns:
            元数据对象
        """
        if not Path(file_path).exists():
            return None

        try:
            media = mutagen.File(file_path)
            # mutagen.File 可能返回空对象，需要检查类型
            if media is None or not hasattr(media, 'info'):
                return None
            return self._parse_media(file_path, media)
        except Exception as e:
            print(f"[ERROR] 提取音视频元数据失败: {e}")
            return None

    def _parse_media(self, file_path: str, media: mutagen.FileType) -> Metadata:
        """解析音视频并提取元数据

        Args:
            file_path: 文件路径
            media: mutagen文件对象

        Returns:
            元数据对象
        """
        # 文件基本信息
        file_info = self.get_file_info(file_path)
        modified_time = datetime.fromtimestamp(file_info["modified_time"])
        accessed_time = datetime.fromtimestamp(file_info["accessed_time"])

        # 创建元数据对象
        metadata = Metadata(
            file_path=file_info["file_path"],
            file_type="media",
            file_name=file_info["file_name"],
            file_size=file_info["file_size"],
            modified_time=modified_time,
            accessed_time=accessed_time,
        )

        # 提取元数据
        self._extract_media_info(media, metadata)

        return metadata

    def _extract_media_info(self, media: mutagen.FileType, metadata: Metadata) -> None:
        """提取音视频元数据

        Args:
            media: mutagen文件对象
            metadata: 元数据对象
        """
        # 时长 ( mutagen 可能返回 0，需要检查有效性 )
        if hasattr(media.info, "length") and media.info.length > 0:
            metadata.duration = float(media.info.length)

        # 比特率
        if hasattr(media.info, "bitrate") and media.info.bitrate > 0:
            metadata.bitrate = int(media.info.bitrate)

        # 采样率
        if hasattr(media.info, "sample_rate") and media.info.sample_rate > 0:
            metadata.sample_rate = int(media.info.sample_rate)

        # 声道数
        if hasattr(media.info, "channels") and media.info.channels > 0:
            metadata.channels = int(media.info.channels)

        # 编解码器
        if hasattr(media.info, "codec"):
            metadata.codec = str(media.info.codec)

        # 尝试使用 pprint 获取更多信息
        if hasattr(media.info, "pprint"):
            try:
                info_str = media.info.pprint()
                if info_str:
                    metadata.extra["pprint"] = info_str
            except Exception:
                pass

        # 标签信息
        tags = getattr(media, "tags", None)
        if tags:
            self._extract_tags(tags, metadata)

        # 根据文件类型补充格式信息
        metadata.format = self._get_format_name(type(media).__name__)

    def _extract_tags(self, tags, metadata: Metadata) -> None:
        """提取标签信息

        Args:
            tags: mutagen标签对象
            metadata: 元数据对象
        """
        # 尝试获取常见标签
        tag_mapping = {
            "artist": "artist",
            "album": "pdf_author",  # 借用字段存储专辑
            "title": "pdf_title",
            "date": None,
            "genre": None,
            "comment": None,
        }

        for tag_key, field_name in tag_mapping.items():
            if hasattr(tags, tag_key):
                value = getattr(tags, tag_key)
                if value:
                    value_str = str(value[0]) if hasattr(value, "__getitem__") else str(value)

                    if field_name == "artist":
                        metadata.artist = value_str
                    elif field_name == "pdf_author":
                        # 保存为extra
                        metadata.extra["album"] = value_str
                    elif field_name == "pdf_title":
                        metadata.pdf_title = value_str
                    elif field_name == "created_time" and field_name is None:
                        # 解析日期
                        metadata.created_time = self._parse_tag_date(value_str)
                    else:
                        metadata.extra[tag_key] = value_str

        # 软件信息
        if hasattr(tags, "encodedby") or hasattr(tags, "encoder"):
            encoder = getattr(tags, "encodedby", None) or getattr(tags, "encoder", None)
            if encoder:
                metadata.software = str(encoder[0]) if hasattr(encoder, "__getitem__") else str(encoder)

        # 版权信息
        if hasattr(tags, "copyright"):
            copyright = getattr(tags, "copyright")
            if copyright:
                metadata.copyright = str(copyright[0]) if hasattr(copyright, "__getitem__") else str(copyright)

    @staticmethod
    def _parse_tag_date(date_str: str) -> Optional[datetime]:
        """解析标签日期字符串

        Args:
            date_str: 日期字符串

        Returns:
            datetime对象
        """
        if not date_str:
            return None

        # 尝试多种日期格式
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return None

    @staticmethod
    def _get_format_name(class_name: str) -> str:
        """获取格式名称

        Args:
            class_name: mutagen类名

        Returns:
            格式名称
        """
        format_map = {
            "MP3": "MP3",
            "FLAC": "FLAC",
            "OggVorbis": "Ogg Vorbis",
            "WAVE": "WAV",
            "MP4": "MP4",
            "M4A": "M4A",
        }
        return format_map.get(class_name, class_name)