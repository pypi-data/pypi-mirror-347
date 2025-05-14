"""
Setup configuration for data-visualiser-package
"""
from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="data-visualiser-package",
    version="0.1.0",
    author="Jonathan Doenz",
    author_email="jonathan.doenz@gmail.com",
    description="A utility package for data visualization and statistical analysis with Matplotlib and Seaborn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathan-doenz/data-visualiser-package",
    project_urls={
        "Bug Tracker": "https://github.com/jonathan-doenz/data-visualiser-package/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "seaborn>=0.11.0",
        "matplotlib>=3.3.0",
        "numpy>=1.19.0",
    ],
    include_package_data=True,
)
