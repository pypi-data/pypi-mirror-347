#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="code-metrics-tracker",
    version="0.1.0",
    description="Code Quality Metrics Tracking Tool",
    author="AgileWorks",
    author_email="info@agileworks.co.za",
    url="https://github.com/AgileWorksZA/codeqa",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "codeqa": ["templates/*"],
    },
    entry_points={
        "console_scripts": [
            "codeqa=codeqa.cli:main",
        ],
    },
    python_requires=">=3.7",
    install_requires=[
        "ruff>=0.0.254",
        "radon>=5.1.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)