#!/usr/bin/env python3
"""
Setup script for the secure-model-service package.
"""

import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements.txt for dependencies
requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
try:
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    # Fallback to minimal requirements if the file is not found
    requirements = [
        "requests>=2.25.0",
        "boto3>=1.28.0",
        "pydantic>=2.0.0"
    ]

setup(
    name="paitient-secure-model",
    version="0.0.1",
    author="PaiTIENT",
    author_email="info@paitient.ai",
    description="PaiTIENT - HIPAA/SOC2 compliant secure model hosting service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saulbuilds/paitient-ai",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "secure-model=secure_model_service.cli.secure_model_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "paitient-ai": [
            "config/*.yaml",
            "kubernetes/**/*.yaml",
            "monitoring/**/*.yml",
        ],
    },
    zip_safe=False,
)
