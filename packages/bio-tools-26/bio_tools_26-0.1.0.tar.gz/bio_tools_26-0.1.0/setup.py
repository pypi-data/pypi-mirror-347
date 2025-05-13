from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Package setup
setup(
    name="bio-tools-26",  # Replace with your desired package name
    version="0.1.0",
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    description="A collection of bioinformatics tools and notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bio",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "bio": ["*.ipynb", "*.exe", "*.ent", "All Files/*"]
    },
)