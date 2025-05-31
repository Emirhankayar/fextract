#!/usr/bin/env python3

from setuptools import setup, find_packages
# import pathlib

# this_directory = pathlib.Path(__file__).parent
#long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="fextract",
    version="1.0.0",
    description="Fast multithreaded file extraction and compression tool",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    author="Emirhan Kayar",
    author_email="emirhan.kayar80@gmail.com",
    url="https://github.com/emirhankayar/fextract",
    
    # Package configuration
    packages=find_packages(),
    py_modules=["main"],  
    
    python_requires=">=3.11",
    install_requires=[
        # extra dependencies
    ],
    
    # Console scripts 
    entry_points={
        "console_scripts": [
            "fextract=main:main",
            "fext=main:main",
        ],
    },
    
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Utilities",
    ],
    
    keywords="zip, compression, extraction, multithreading, fast, archive",
    
    project_urls={
        "Bug Reports": "https://github.com/emirhankayar/fextract/issues",
        "Source": "https://github.com/emirhankayar/fextract",
    },
)