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
