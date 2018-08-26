#!/usr/bin/env python3

"""Setup."""

import setuptools

setuptools.setup(
    name="example_app",
    version="1.0",
    author="Logan Kaser",
    author_email="logankaser@fyrn.io",
    packages=["example_app"],
    install_requires=[
        "termcolor",
    ]
)
