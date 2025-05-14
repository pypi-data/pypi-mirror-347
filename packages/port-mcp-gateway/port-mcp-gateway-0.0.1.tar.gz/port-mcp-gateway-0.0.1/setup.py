"""
Setup script for port-mcp-gateway.
"""

from setuptools import setup, find_packages
import os
import re
import codecs

# Read the requirements from requirements.txt in the root directory
with open("../requirements.txt") as f:
    requirements = [line.strip() for line in f if not line.startswith("#")]

# Get version from version.txt
with open("version.txt", "r") as f:
    version = f.read().strip()

# Read the long description from docs/PyPI-README.md
with open("docs/PyPI-README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="port-mcp-gateway",
    version=version,
    description="A gateway for interacting with Port.io through a standardized MCP API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Amzulescu",
    author_email="dan.a@port.io",
    url="https://github.com/port-experimental/port-mcp-gateway",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "port-mcp-gateway=mcp.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="port.io, mcp, api, gateway",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/port-mcp-gateway/issues",
        "Source": "https://github.com/yourusername/port-mcp-gateway",
    },
)
