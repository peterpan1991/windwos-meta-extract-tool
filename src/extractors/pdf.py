"""PDF元数据提取器"""
from datetime import datetime
from pathlib import Path
from typing import Optional

from pypdf import PdfReader

from src.extractors.base import BaseExtractor
from src.models.metadata import Metadata


class PDFExtractor(BaseExtractor):
    """PDF元数据提取器"""

    SUPPORTED_EXTENSIONS = {".pdf"}

    def extract(self, file_path: str) -> Optional[Metadata]:
        """提取PDF元数据

        Args:
            file_path: PDF文件路径

        Returns:
            元数据对象
        """
        if not Path(file_path).exists():
            return None

        try:
            reader = PdfReader(file_path)
            return self._parse_pdf(file_path, reader)
        except Exception as e:
            print(f"[ERROR] 提取PDF元数据失败: {e}")
            return None

    def _parse_pdf(self, file_path: str, reader: PdfReader) -> Metadata:
        """解析PDF并提取元数据

        Args:
            file_path: 文件路径
            reader: PdfReader对象

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
            file_type="pdf",
            file_name=file_info["file_name"],
            file_size=file_info["file_size"],
            modified_time=modified_time,
            accessed_time=accessed_time,
            format="PDF",
        )

        # 提取PDF元数据
        self._extract_pdf_metadata(reader, metadata)

        return metadata

    def _extract_pdf_metadata(self, reader: PdfReader, metadata: Metadata) -> None:
        """提取PDF特定元数据

        Args:
            reader: PdfReader对象
            metadata: 元数据对象
        """
        # 基本信息
        metadata.pdf_page_count = len(reader.pages)

        # 文档信息
        doc_info = reader.metadata
        if doc_info:
            # 标题
            if "/Title" in doc_info:
                metadata.pdf_title = doc_info["/Title"]

            # 作者
            if "/Author" in doc_info:
                metadata.pdf_author = doc_info["/Author"]

            # 主题
            if "/Subject" in doc_info:
                metadata.pdf_subject = doc_info["/Subject"]

            # 关键词
            if "/Keywords" in doc_info:
                metadata.pdf_keywords = doc_info["/Keywords"]

            # 创建者
            if "/Creator" in doc_info:
                metadata.pdf_creator = doc_info["/Creator"]

            # 生产者
            if "/Producer" in doc_info:
                metadata.pdf_producer = doc_info["/Producer"]

            # 创建时间
            if "/CreationDate" in doc_info:
                metadata.created_time = self._parse_pdf_date(doc_info["/CreationDate"])

            # 修改时间
            if "/ModDate" in doc_info:
                metadata.modified_time = self._parse_pdf_date(doc_info["/ModDate"])

            # 软件信息
            if "/Creator" in doc_info:
                metadata.software = doc_info["/Creator"]

            if "/Producer" in doc_info:
                if metadata.software:
                    metadata.software += f" ({doc_info['/Producer']})"
                else:
                    metadata.software = doc_info["/Producer"]

    @staticmethod
    def _parse_pdf_date(date_str: str) -> Optional[datetime]:
        """解析PDF日期字符串

        Args:
            date_str: PDF日期字符串 (格式: D:YYYYMMDDHHmmSSOHHmm'm)

        Returns:
            datetime对象
        """
        if not date_str:
            return None

        try:
            # 格式: D:YYYYMMDDHHmmSS
            if date_str.startswith("D:"):
                date_str = date_str[2:]

            if len(date_str) >= 14:
                year = int(date_str[0:4])
                month = int(date_str[4:6]) if len(date_str) >= 6 else 1
                day = int(date_str[6:8]) if len(date_str) >= 8 else 1
                hour = int(date_str[8:10]) if len(date_str) >= 10 else 0
                minute = int(date_str[10:12]) if len(date_str) >= 12 else 0
                second = int(date_str[12:14]) if len(date_str) >= 14 else 0

                return datetime(year, month, day, hour, minute, second)
        except (ValueError, IndexError):
            pass

        return None