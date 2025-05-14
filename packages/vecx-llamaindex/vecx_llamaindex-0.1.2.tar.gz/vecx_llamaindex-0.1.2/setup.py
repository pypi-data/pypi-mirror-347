# myproject/setup.py

from setuptools import setup, find_packages

setup(
    name="vecx-llamaindex",
    version="0.1.2",
    packages=find_packages(include=['vecx_llamaindex', 'vecx_llamaindex.*']),
    install_requires=[
        # List your dependencies here
        "llama-index>=0.12.34",
        "vecx>=0.32.1",
    ],
    author="LaunchX Labs",
    author_email="vineet@launchxlabs.ai",
    description="Encrypted Vector Database for Secure and Fast ANN Searches",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://vectorxdb.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
