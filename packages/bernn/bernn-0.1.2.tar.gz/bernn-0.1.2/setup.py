#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 2021
@author: Simon Pelletier
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Read long description from README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bernn",
    description="BERNN: A deep learning framework for MS/MS data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Simon P. Pfeiffer",
    author_email="simon.pelletier@gmail.com",
    url="https://github.com/spell00/BERNN_MSMS",
    packages=find_packages(
        exclude=[
            "DeepExplainer*",
            "figures*",
            "htmlcov*",
            "images*",
            "mlruns*",
            "tests*",
            "notebooks*",
            "data*",
            "build*",
            "dist*",
            "bin*",
            "logs*",
            "tmp*",
            "temp*",
            "*.tests",
            "*.test",
        ]
    ),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=[
        "mass spectrometry",
        "deep learning",
        "neural networks",
        "bioinformatics",
        "proteomics",
    ],
    project_urls={
        "Bug Reports": "https://github.com/spell00/BERNN_MSMS/issues",
        "Source": "https://github.com/spell00/BERNN_MSMS",
        "Documentation": "https://github.com/spell00/BERNN_MSMS#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
