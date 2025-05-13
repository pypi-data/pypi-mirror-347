from setuptools import setup, find_packages

setup(
    name="testuthird",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "clight",
        
    ],
    entry_points={
        "console_scripts": [
            "testuthird=testuthird.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "testuthird": [
            "main.py",
            "__init__.py",
            "__system__/imports.py",
            "__system__/index.py",
            "__system__/modules/jobs.py",
            "__system__/sources/clight.json",
            "__system__/sources/logo.ico"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="Test Project 3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        
        "Operating System :: OS Independent",
    ],
)
