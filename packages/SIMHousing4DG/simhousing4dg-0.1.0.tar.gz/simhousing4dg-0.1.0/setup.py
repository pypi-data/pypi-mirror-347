# D:\SIMHousing4DG\setup.py

from setuptools import setup, find_packages

setup(
    name="SIMHousing4DG",
    version="0.1.0",
    description=(
        "用于揭示在住房–服务双重梯度调整背景下，不同收入群体的居住行为反应、"
        "匹配效用变化及其引发的财政与人口结构反馈机制的模拟器。"
        "模型通过设置结构性 HQG 与 SGI，结合居民对住房与服务的异质性偏好，"
        "动态模拟多类政策路径对居住效用、人口空间重构和财政支出结构的系统性影响，"
        "实现“住房–服务–人口–财政”四元系统的耦合演进。"
    ),
    author="ZHANG Zuo, WANG Zhe",
    python_requires=">=3.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
    ],
    entry_points={
        "console_scripts": [
            # 安装后，用户敲 simhousing4dg 就会调用 launch.main()
            "simhousing4dg = SIMHousing4DG.launch:main",
        ],
    },
)
