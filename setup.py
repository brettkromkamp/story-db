"""
setup.py file.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    README = f.read()

with open(os.path.join(here, "HISTORY.rst"), encoding="utf-8") as f:
    HISTORY = f.read()

setup(
    name="story-db",
    version="0.0.1",  # Bump version NUMBER *after* starting (git flow) release.
    description="Pending.",
    long_description=README + "\n\n" + HISTORY,
    keywords="storytelling, narratives, stories, topic maps, semantic technology",
    url="https://github.com/brettkromkamp/story-db",
    author="Brett Alistair Kromkamp",
    author_email="brett.kromkamp@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["docs", "tests*", "scripts"]),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=["topic-db", "python-slugify"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
