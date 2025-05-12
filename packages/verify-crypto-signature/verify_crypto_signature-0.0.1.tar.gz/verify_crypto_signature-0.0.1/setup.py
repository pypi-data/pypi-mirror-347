#!/usr/bin/env python
"""
Setup script for the verify-crypto-signature package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "annotated-types==0.7.0",
    "bitarray==3.4.0",
    "ckzg==2.1.1",
    "cytoolz==1.0.1",
    "eth-account==0.13.7",
    "eth-hash==0.7.1",
    "eth-keyfile==0.8.1",
    "eth-keys==0.7.0",
    "eth-rlp==2.2.0",
    "eth-typing==5.2.1",
    "eth-utils==5.3.0",
    "eth_abi==5.2.0",
    "hexbytes==1.3.0",
    "jsonalias==0.1.1",
    "parsimonious==0.10.0",
    "pycryptodome==3.22.0",
    "pydantic==2.11.4",
    "pydantic_core==2.33.2",
    "regex==2024.11.6",
    "rlp==4.1.0",
    "solders==0.26.0",
    "toolz==1.0.0",
    "typing-inspection==0.4.0",
    "typing_extensions==4.13.2"
]

setup(
    name="verify-crypto-signature",
    version="0.0.1",
    author="BonifacioCalindoro",
    author_email="admin@walver.io",
    description="A comprehensive Python library to verify crypto wallet signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/walver-io/verify-crypto-signature",
    packages=find_packages(include=["verify_crypto_signature", "verify_crypto_signature.*"]),
    package_data={
        "verify_crypto_signature": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords=["verify", "crypto", "signature", "wallet", "blockchain", "solana", "ethereum", "cryptography"],
    include_package_data=True,
) 
