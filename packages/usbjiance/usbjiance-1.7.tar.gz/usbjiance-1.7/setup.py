from setuptools import setup, find_packages
import os

# 读取README.md文件
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="usbjiance",
    version="1.07",
    author="zhaofucheng",
    author_email="your.email@example.com",
    description="高性能Windows USB设备监控工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/usbjiance",
    packages=find_packages(),
    py_modules=["usbjiance"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "wmi",
        "pywin32",  # 提供pythoncom支持
    ],
    keywords="usb, monitor, device, windows, hardware",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/usbjiance/issues",
        "Source": "https://github.com/yourusername/usbjiance",
    },
) 