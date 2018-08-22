"""Package file for vehicle_client."""

from setuptools import find_packages, setup

setup(
    name="vehicle_client",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-sqlalchemy"
    ],
)
