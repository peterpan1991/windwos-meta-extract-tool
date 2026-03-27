"""辅助函数"""
from typing import Optional, Tuple


def normalize_gps(coordinate: Tuple, ref: str) -> Optional[float]:
    """规范化GPS坐标为十进制度数

    Args:
        coordinate: GPS坐标元组 (度, 分, 秒)
        ref: 方向引用 (N/S/E/W)

    Returns:
        十进制度数
    """
    if not coordinate or not ref:
        return None

    try:
        degrees = float(coordinate[0])
        minutes = float(coordinate[1])
        seconds = float(coordinate[2])

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        # 南半球或西半球为负值
        if ref in ("S", "W"):
            decimal = -decimal

        return round(decimal, 6)
    except (TypeError, IndexError, ValueError):
        return None


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小

    Args:
        size_bytes: 字节数

    Returns:
        格式化的大小字符串
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def format_duration(seconds: float) -> str:
    """格式化音视频时长

    Args:
        seconds: 秒数

    Returns:
        格式化的时间字符串 (HH:MM:SS)
    """
    if seconds < 0:
        return "00:00:00"

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_bitrate(bitrate: int) -> str:
    """格式化比特率

    Args:
        bitrate: 比特率 (bps)

    Returns:
        格式化的比特率字符串
    """
    if bitrate < 1000:
        return f"{bitrate} bps"
    elif bitrate < 1000000:
        return f"{bitrate / 1000:.0f} kbps"
    else:
        return f"{bitrate / 1000000:.1f} Mbps"