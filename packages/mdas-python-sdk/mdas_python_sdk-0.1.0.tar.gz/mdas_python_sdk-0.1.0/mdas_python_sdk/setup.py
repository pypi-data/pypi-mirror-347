from setuptools import setup, find_packages

setup(
    name="mdas-python-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="MDAS Team",
    author_email="info@example.com",
    description="Python SDK for the MDAS API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mdas/mdas-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 