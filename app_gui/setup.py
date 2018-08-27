#!/usr/bin/env python3

"""Setup."""

import setuptools

setuptools.setup(
    name="gui",
    version="1.0",
    author="Logan Kaser",
    author_email="logankaser@fyrn.io",
    packages=["gui"],
    install_requires=[
        "termcolor",
    ]
)
