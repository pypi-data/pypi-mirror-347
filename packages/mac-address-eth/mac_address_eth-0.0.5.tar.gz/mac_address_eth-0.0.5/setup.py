from setuptools import setup, find_packages
import os

# Get the path to the `package_version.txt` file
version_file = os.path.join(
    os.path.dirname(__file__), "get_mac", "package_version.txt"
)

# Read the version from the VERSION file
with open(version_file) as f:
    version = f.read().strip()

setup(
    name="mac_address_eth",
    version=version,
    description="not for all people",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="your_name",
    author_email="your.email@example.com",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "get-mac=get_mac.cli:get_mac",
        ],
    },
    package_data={
        "get-mac": ["package_version.txt"],
    },
    install_requires=[
        "psutil"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
