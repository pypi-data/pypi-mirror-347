from setuptools import setup, find_packages

setup(
    name="excel-conversion",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["xlrd>=1.1.0"]
)
