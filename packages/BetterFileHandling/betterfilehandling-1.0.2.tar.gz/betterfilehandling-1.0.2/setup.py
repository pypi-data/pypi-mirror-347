from setuptools import setup, find_packages
import pathlib

# Read the long description from README.md
this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="BetterFileHandling",
    version="1.0.2",
    author="Aksh Tiwari",
    author_email="akshprooo@gmail.com",  # replace with your real email or leave as placeholder
    description="A modular Python package for efficient, secure, and readable file operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords=(
        "file handling, file operations, python file utils, read files, "
        "write files, encode files, json writer, modular file library, "
        "python utilities, secure file handling, efficient file IO"
    ),
    license="MIT",
)
