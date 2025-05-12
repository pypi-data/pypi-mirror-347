from setuptools import setup, find_packages
import os

# 读取 README 文件内容作为 long_description
with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gisense",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # 添加项目依赖
        "numpy",
        "matplotlib",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "geopandas",  # 可选依赖
        ],
    },
    python_requires=">=3.8",
    long_description=long_description,  # 添加 long_description
    long_description_content_type="text/markdown",  # 指定描述内容类型为 Markdown
)
