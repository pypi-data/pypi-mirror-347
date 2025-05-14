#!/usr/bin/env python3
"""
Setup script for Threat Canvas - an advanced autonomous threat modeling system.
"""

import os

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

# Optional dependencies
extras_require = {
    "visualization": [
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "mermaid-cli>=0.1.0",  # For rendering Mermaid diagrams to images
    ],
    "dev": [
        "pytest>=7.0.0",
        "pytest-cov>=3.0.0",
        "black>=22.0.0",
        "isort>=5.10.0",
        "mypy>=0.9.0",
        "flake8>=4.0.0",
    ],
    "docs": [
        "sphinx>=4.0.0",
        "sphinx-rtd-theme>=1.0.0",
        "sphinx-autodoc-typehints>=1.12.0",
    ],
}

# Add 'all' option that includes all extras
extras_require["all"] = [pkg for group in extras_require.values() for pkg in group]

setup(
    name="autothreats",
    version="0.1.2",
    author="Threat Canvas Team",
    author_email="info@threatcanvas.io",
    description="Advanced Autonomous Threat Modeling System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/threatcanvas/threat-canvas",
    project_urls={
        "Documentation": "https://threatcanvas.io/docs",
        "Bug Tracker": "https://github.com/threatcanvas/threat-canvas/issues",
        "Source Code": "https://github.com/threatcanvas/threat-canvas",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements + ["jinja2>=3.0.0"],
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "threat-modeling=autothreats.scripts.threat_modeling_cli:main",
            "threat-canvas=autothreats.scripts.threat_modeling_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "autothreats": [
            "templates/*.html",
            "templates/*.json",
            "data/*.json",
        ],
    },
)
