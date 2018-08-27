#!/usr/bin/env python3

"""Setup."""

import setuptools

setuptools.setup(
    name="hello",
    version="1.0",
    author="Logan Kaser",
    author_email="logankaser@fyrn.io",
    packages=["hello"],
    install_requires=[
        "termcolor",
    ]
)
