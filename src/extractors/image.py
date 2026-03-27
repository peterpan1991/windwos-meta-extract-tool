"""图片元数据提取器"""
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image
from PIL.ExifTags import TAGS

from src.extractors.base import BaseExtractor
from src.models.metadata import Metadata
from src.utils.helpers import normalize_gps


class ImageExtractor(BaseExtractor):
    """图片元数据提取器"""

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif"}

    def extract(self, file_path: str) -> Optional[Metadata]:
        """提取图片元数据

        Args:
            file_path: 图片文件路径

        Returns:
            元数据对象
        """
        if not Path(file_path).exists():
            return None

        try:
            image = Image.open(file_path)
            return self._parse_image(file_path, image)
        except Exception as e:
            print(f"[ERROR] 提取图片元数据失败: {e}")
            return None

    def _parse_image(self, file_path: str, image: Image.Image) -> Metadata:
        """解析图片并提取元数据

        Args:
            file_path: 文件路径
            image: PIL Image对象

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
            file_type="image",
            file_name=file_info["file_name"],
            file_size=file_info["file_size"],
            modified_time=modified_time,
            accessed_time=accessed_time,
            width=image.width,
            height=image.height,
            format=image.format,
            mode=image.mode,
        )

        # 提取EXIF数据
        self._extract_exif(image, metadata)

        return metadata

    def _extract_exif(self, image: Image.Image, metadata: Metadata) -> None:
        """提取EXIF数据

        Args:
            image: PIL Image对象
            metadata: 元数据对象
        """
        exif_data = image.getexif()
        if not exif_data:
            return

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, str(tag_id))

            if tag_name == "DateTimeOriginal":
                metadata.created_time = self._parse_exif_datetime(value)
            elif tag_name == "Make":
                metadata.camera_make = str(value).strip()
            elif tag_name == "Model":
                metadata.camera_model = str(value).strip()
            elif tag_name == "Software":
                metadata.software = str(value).strip()
            elif tag_name == "Artist":
                metadata.artist = str(value).strip()
            elif tag_name == "Copyright":
                metadata.copyright = str(value).strip()
            elif tag_name == "LensModel":
                metadata.lens_model = str(value).strip()
            elif tag_name == "ExposureTime":
                metadata.exposure_time = str(value)
            elif tag_name == "FNumber":
                metadata.f_number = str(value)
            elif tag_name == "ISOSpeedRatings":
                metadata.iso = int(value) if value else None
            elif tag_name == "FocalLength":
                metadata.focal_length = str(value)
            elif tag_name == "Flash":
                metadata.flash = str(value)
            elif tag_name == "WhiteBalance":
                metadata.white_balance = str(value)
            elif tag_name == "GPSInfo":
                self._extract_gps(value, metadata)

            # 保存额外EXIF数据
            if tag_name not in metadata.extra:
                metadata.extra[tag_name] = str(value)

    def _extract_gps(self, gps_ifd: dict, metadata: Metadata) -> None:
        """提取GPS信息

        Args:
            gps_ifd: GPS IFD数据
            metadata: 元数据对象
        """
        if not gps_ifd:
            return

        gps_tags = {
            1: "GPSLatitudeRef",
            2: "GPSLatitude",
            3: "GPSLongitudeRef",
            4: "GPSLongitude",
            5: "GPSAltitudeRef",
            6: "GPSAltitude",
        }

        lat_ref = gps_ifd.get(1)
        lat = gps_ifd.get(2)
        lon_ref = gps_ifd.get(3)
        lon = gps_ifd.get(4)
        alt_ref = gps_ifd.get(5)
        alt = gps_ifd.get(6)

        if lat and lon:
            metadata.gps_latitude = normalize_gps(lat, lat_ref)
            metadata.gps_longitude = normalize_gps(lon, lon_ref)

        if alt is not None:
            metadata.gps_altitude = float(alt) if alt_ref == 1 else -float(alt)

    @staticmethod
    def _parse_exif_datetime(date_str: str) -> Optional[datetime]:
        """解析EXIF时间字符串

        Args:
            date_str: EXIF时间字符串 (格式: YYYY:MM:DD HH:MM:SS)

        Returns:
            datetime对象
        """
        try:
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
        except (ValueError, TypeError):
            return None