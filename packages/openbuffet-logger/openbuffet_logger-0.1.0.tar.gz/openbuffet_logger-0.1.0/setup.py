# setup.py
from setuptools import setup, find_packages

setup(
    name="openbuffet_logger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Ferdi Kurnaz",
    author_email="ferdikurnazdm@gmail.com",
    description="Flexible, pluggable and testable logger manager for Python.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ferdikurnazdm/openbuffet_logger",  # GitHub repo linkin
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
