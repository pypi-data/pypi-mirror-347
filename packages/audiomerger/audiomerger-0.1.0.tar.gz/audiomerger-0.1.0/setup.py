from setuptools import setup, find_packages

setup(
    name="audiomerger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Guilherme Conti Teixeira",
    author_email="guibasconti@gmail.com",
    description="A simple package to merge audio files using base64 encoding",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guiconti/audiomerger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)