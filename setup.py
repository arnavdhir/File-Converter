"""
Setup configuration for the file converter application
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file-converter",
    version="1.0.0",
    author="Qwen Developer",
    author_email="qwen@example.com",
    description="A comprehensive CLI tool for converting between various file formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qwen/file-converter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=8.0.0",
        "PyPDF2>=3.0.0",
        "python-docx>=0.8.11",
        "pandas>=1.3.0",
        "PyYAML>=5.4.0",
        "markdown>=3.3.0",
        "reportlab>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "file-converter=src.main:main",
        ],
    },
)