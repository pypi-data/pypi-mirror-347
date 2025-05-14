from setuptools import setup, find_packages

setup(
    name="mcard",
    version="0.1.8",  # Increment the version number
    description="MCard - Content type detection and analysis library",
    author="Ben Koo",
    author_email="koo0905@gmail.com",
    url="https://github.com/xlp0/MCard_TDD",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "lxml;python_version>='3.7'",  # Optional dependency for XMLDetector
    ],
)