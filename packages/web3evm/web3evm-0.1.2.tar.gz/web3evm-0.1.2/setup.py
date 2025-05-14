from setuptools import setup, find_packages

setup(
    name="web3evm",
    version="0.1.2",
    author="bryains",
    author_email="",
    description="evm utilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
