# OrKa: Orchestrator Kit Agents
# Copyright © 2025 Marco Somma
#
# This file is part of OrKa – https://github.com/marcosomma/orka
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes without explicit permission.
#
# Full license: https://creativecommons.org/licenses/by-nc/4.0/legalcode
# For commercial use, contact: marcosomma.work@gm
# 
# Required attribution: OrKa by Marco Somma – https://github.com/marcosomma/orka

from setuptools import setup, find_packages

setup(
    name="orka-reasoning",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "redis",
        "litellm",
        "pyyaml"
    ],
    author="Marco Somma",
    description="OrKa: Modular orchestration for agent-based cognition",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marcosomma/orka",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
