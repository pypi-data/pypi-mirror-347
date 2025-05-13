from setuptools import setup, find_packages

setup(
    name="datasend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
    ],
    author="DataShare Team",
    author_email="p.korovesis@bigdatalab.ai",
    description="The quickest way to share data with your team",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://bigdatalab.ai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)