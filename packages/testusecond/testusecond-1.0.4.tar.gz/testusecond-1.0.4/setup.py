from setuptools import setup, find_packages

setup(
    name="testusecond",
    version="1.0.4",
    packages=find_packages(),
    install_requires=[
        "clight",
        
    ],
    entry_points={
        "console_scripts": [
            "testusecond=testusecond.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "testusecond": [
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
    description="Test Project 2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        
        "Operating System :: OS Independent",
    ],
)
