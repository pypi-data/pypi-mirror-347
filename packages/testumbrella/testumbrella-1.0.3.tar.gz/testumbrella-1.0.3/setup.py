from setuptools import setup, find_packages

setup(
    name="testumbrella",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "clight",
        "testufirst==1.0.2",
        "testusecond==1.0.1",
        "testuthird==1.0.1",
        "testufirst"
    ],
    entry_points={
        "console_scripts": [
            "testumbrella=testumbrella.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "testumbrella": [
            "main.py",
            "__init__.py",
            ".system/imports.py",
            ".system/index.py",
            ".system/modules/jobs.py",
            ".system/sources/clight.json",
            ".system/sources/logo.ico"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="Test umbrella project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        
        "Operating System :: OS Independent",
    ],
)
