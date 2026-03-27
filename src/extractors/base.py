"""基础提取器抽象类"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from src.models.metadata import Metadata


class BaseExtractor(ABC):
    """元数据提取器基类"""

    SUPPORTED_EXTENSIONS: set = set()

    def __init__(self):
        self.supported_extensions = self.SUPPORTED_EXTENSIONS

    @abstractmethod
    def extract(self, file_path: str) -> Optional[Metadata]:
        """提取元数据

        Args:
            file_path: 文件路径

        Returns:
            元数据对象，提取失败返回 None
        """
        pass

    @classmethod
    def can_extract(cls, file_path: str) -> bool:
        """检查是否支持该文件类型

        Args:
            file_path: 文件路径

        Returns:
            是否支持
        """
        ext = Path(file_path).suffix.lower()
        return ext in cls.SUPPORTED_EXTENSIONS

    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """获取文件基本信息

        Args:
            file_path: 文件路径

        Returns:
            文件信息字典
        """
        path = Path(file_path)
        stat = path.stat()
        return {
            "file_path": str(path.absolute()),
            "file_name": path.name,
            "file_size": stat.st_size,
            "modified_time": stat.st_mtime,
            "accessed_time": stat.st_atime,
        }