# setup.py
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="contain_101_or_not",
    version="1.1.0",
    description="Check if a binary string contains 101 using DFA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mohamed Khaled",
    author_email="mokhaled732003@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
