from setuptools import setup, find_packages

setup(
    name="sws_test_pkg",  # ✅ Your package name
    version="0.26.0",
    author="Your Name",
    description="A simple test package",
    packages=find_packages(),
    python_requires=">=3.6",
)
