import setuptools
from distutils.core import setup

# read the contents of README.md
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "../README.md"), encoding="utf-8") as f:
    long_description = f.read()

from os import environ

setup(
    name="ILMO",
    version="0.0.2",
    description="A library management tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Julian-Samuel Gebühr",
    author_email="julian-samuel@gebuehr.net",
    url="https://github.com/moan0s/ILMO2",
    download_url="https://github.com/moan0s/ILMO2.git",
    license="GPL-3",
    packages=["ilmo", "library"],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Environment :: Web",
        "Intended Audience :: Libraries",
        "License :: OSI Approved :: GPL-3 License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
    ],
)