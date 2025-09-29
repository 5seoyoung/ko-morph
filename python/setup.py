from setuptools import setup, find_packages

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="komorph",
    version="0.1.0",
    author="Korean Morpheme Analyzer Team",
    description="Hybrid Korean Morphological Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Korean",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "komorph=komorph.cli:main",
        ],
    },
)