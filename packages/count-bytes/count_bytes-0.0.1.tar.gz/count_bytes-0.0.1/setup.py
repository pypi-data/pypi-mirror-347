from setuptools import setup, find_packages

setup(
    name="count-bytes", # Name on PyPI
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "emoji>=2.0.0"
    ],
    author="Adonis Miclea",
    author_email="tilik_87@yahoo.com",
    description="A Python module that prints how many bytes are in a string or file",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
