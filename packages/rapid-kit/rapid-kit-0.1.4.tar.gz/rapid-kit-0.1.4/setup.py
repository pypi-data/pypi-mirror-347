from setuptools import setup, find_packages
import os

# 读取README.md文件作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    readme_content = fh.read()

# 尝试读取CHANGELOG.md并添加到长描述末尾
try:
    with open("CHANGELOG.md", "r", encoding="utf-8") as ch:
        changelog_content = ch.read()
        long_description = f"{readme_content}\n{changelog_content}"
except FileNotFoundError:
    long_description = readme_content

setup(
    name="rapid-kit",
    version="0.1.4",
    packages=find_packages(),
    description="Real-time Audio-visual Platform for IoT Devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TANGE.AI",
    author_email="fengjun.dev@gmail.com",
    url="https://tange.ai/",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
) 