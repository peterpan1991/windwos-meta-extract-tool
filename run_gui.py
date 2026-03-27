"""启动 GUI 应用程序"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.gui import main

if __name__ == "__main__":
    main()
