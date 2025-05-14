from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nmeaparsec",
    version="0.1.0",
    author="Yavuz Murat",
    author_email="yyavuzmurat@gmail.com",
    description="A Python package for parsing NMEA data from GPS devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YavuzMuratt/nmeaparsec",
    packages=find_packages(exclude=["tests", "tests.*", "testfiles", "visualization_output"]),
    package_data={
        "nmeaparsec": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
    ],
    extras_require={
        "visualization": ["matplotlib>=3.3.0"],
    },
    project_urls={
        "Bug Reports": "https://github.com/YavuzMuratt/nmeaparsec/issues",
        "Source": "https://github.com/YavuzMuratt/nmeaparsec",
    },
) 