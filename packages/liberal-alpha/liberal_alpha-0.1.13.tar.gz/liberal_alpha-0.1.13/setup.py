# setup.py
import sys
from setuptools import setup, find_packages

# Conditional dependencies
common_requires = [
    "grpcio>=1.30.0",
    "protobuf>=3.13.0",
    "requests>=2.20.0",
    "coincurve>=13.0.0",
    "pycryptodome>=3.9.0",
    "eth-account>=0.5.0",
    "eth-keys>=0.3.0",
    "websockets>=8.0.0",
    "nest_asyncio>=1.5.0",
]

extras_requires = []

# For Python 3.12+, override grpcio/protobuf
if sys.version_info >= (3, 12):
    extras_requires += [
        "grpcio>=1.70.0",
        "grpcio-tools>=1.70.0",
        "protobuf>=4.25.0"
    ]
else:
    extras_requires += [
        "grpcio-tools>=1.30.0",  # Optional, only needed for regen
    ]

setup(
    name="liberal_alpha",  # PyPI package name
    version="0.1.13",    # Package version
    author="capybaralabs",
    author_email="donny@capybaralabs.xyz",
    description="Liberal Alpha Python SDK for interacting with gRPC-based backend",
    long_description=open("README.md", encoding="utf-8").read(),  # Read README.md as PyPI description
    long_description_content_type="text/markdown",
    url="https://github.com/capybaralabs-xyz/Liberal_Alpha",  # Repository URL
    packages=find_packages(exclude=["tests", "tests.*"]),        # Automatically find packages, exclude test directories
    include_package_data=True,                                   # Include non-py files like proto/*.proto
    install_requires=common_requires + extras_requires,
    entry_points={
        "console_scripts": [
            "liberal_alpha=liberal_alpha.client:main",  # CLI command 'liberal_alpha' calls liberal_alpha/client.py:main()
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",  # Add Python 3.8 support
        "Programming Language :: Python :: 3.9",  # Add Python 3.9 support
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Lower Python requirement to 3.
)
