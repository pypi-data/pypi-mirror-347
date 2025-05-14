# D:\SIMHousing4DG\SIMHousing4DG\launch.py

import os
import sys
from subprocess import call

def main():
    # 定位到 __main__.py 在包内的实际路径
    pkg_dir = os.path.dirname(__file__)
    script = os.path.join(pkg_dir, "__main__.py")
    # 用 streamlit CLI 启动脚本
    call([sys.executable, "-m", "streamlit", "run", script])
