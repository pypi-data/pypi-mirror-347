from setuptools import setup, find_packages

setup(
    name="usbjiance",
    version="1.9",
    packages=find_packages(),
    install_requires=[
        "wmi>=1.5.1",
        "pywin32>=305",
    ],
    author="zhaof",
    author_email="zhaof@example.com",  # 请替换为你的邮箱
    description="A high-performance Windows USB device monitoring tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/usbjiance",  # 请替换为你的仓库地址
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 