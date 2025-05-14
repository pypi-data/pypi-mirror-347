# myproject/setup.py

from setuptools import setup, find_packages

setup(
    name="vecx-langchain",
    version="0.1.3",
    packages=find_packages(include=['vecx_langchain', 'vecx_langchain.*']),
    install_requires=[
        # List your dependencies here
        "langchain>=0.3.25",
        "langchain-core>=0.3.59",
        "vecx>=0.32.1",
        "numpy",
    ],
    author="LaunchX Labs",
    author_email="vineet@launchxlabs.ai",
    description="Encrypted Vector Database for Secure and Fast ANN Searches with LangChain",
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
