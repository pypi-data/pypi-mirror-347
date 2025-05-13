#!/usr/bin/env python3
"""
Setup script for testindex-knowledge-contract package.
"""

from setuptools import setup, find_packages

setup(
    name="testindex-knowledge-contract",
    version="0.1.0",
    description="Knowledge v1 Contract for TestIndex",
    author="TestIndex Team",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "testindex_knowledge_contract": ["test_data/*.json"],
    },
    install_requires=[
        "neo4j>=5.0.0,<6.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 