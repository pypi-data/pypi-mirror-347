#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fluidgrids-cli",
    version="0.1.0",
    author="Vignesh T.V",
    author_email="vignesh@algoshred.com",
    description="Command-line interface for the FluidGrids Workflow Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://fluidgrids.ai/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fluidgrids==0.1.0",
        "click>=8.0.0",
        "pyyaml>=6.0",
        "rich>=12.0.0",
        "keyring>=23.0.0",
        "tabulate>=0.8.0",
    ],
    entry_points={
        "console_scripts": [
            "fluidgrids=fluidgrids_cli.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 