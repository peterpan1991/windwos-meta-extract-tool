"""元数据结构定义"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Metadata:
    """统一元数据结构"""

    file_path: str
    file_type: str
    file_name: str
    file_size: Optional[int] = None

    # 基本信息
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    accessed_time: Optional[datetime] = None

    # 图片相关
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    mode: Optional[str] = None

    # EXIF 数据
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    lens_model: Optional[str] = None
    exposure_time: Optional[str] = None
    f_number: Optional[str] = None
    iso: Optional[int] = None
    focal_length: Optional[str] = None
    flash: Optional[str] = None
    white_balance: Optional[str] = None

    # GPS 数据
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    gps_altitude: Optional[float] = None

    # 软件信息
    software: Optional[str] = None
    artist: Optional[str] = None
    copyright: Optional[str] = None

    # PDF 相关
    pdf_title: Optional[str] = None
    pdf_author: Optional[str] = None
    pdf_subject: Optional[str] = None
    pdf_keywords: Optional[str] = None
    pdf_creator: Optional[str] = None
    pdf_producer: Optional[str] = None
    pdf_page_count: Optional[int] = None

    # 音视频相关
    duration: Optional[float] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    codec: Optional[str] = None

    # 其他元数据
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """转换为字典格式"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = value if value else {}
            else:
                result[key] = value
        return result

    def get_summary(self) -> dict:
        """获取摘要信息"""
        return {
            "file_name": self.file_name,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "created_time": self.created_time.isoformat() if self.created_time else None,
            "camera": f"{self.camera_make} {self.camera_model}".strip() or None,
            "gps": f"{self.gps_latitude}, {self.gps_longitude}" if self.gps_latitude and self.gps_longitude else None,
            "software": self.software,
        }

    def has_exif(self) -> bool:
        """是否有EXIF数据"""
        return bool(self.camera_make or self.camera_model or self.created_time)

    def has_gps(self) -> bool:
        """是否有GPS数据"""
        return bool(self.gps_latitude and self.gps_longitude)