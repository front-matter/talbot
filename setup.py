import codecs
import re
from setuptools import setup
from setuptools import find_packages

version = ""
with open("talbot/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

with codecs.open("README.rst", "r", "utf-8") as f:
    readme = f.read()

with codecs.open("Changelog.rst", "r", "utf-8") as f:
    changes = f.read()

long_description = "\n\n" + readme + "\n\n" + changes

setup(
    name="talbot",
    version=version,
    description="Library for conversions of scholarly metadata",
    long_description=long_description,
    author="Martin Fenner",
    author_email="martin@front-matter.io",
    url="https://github.com/front-matter/talbot",
    license="MIT",
    packages=find_packages(exclude=["test*"]),
    install_requires=["requests>=2.7.0", "tqdm"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
