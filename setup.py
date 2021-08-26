import setuptools

with open("README.md", "r") as fh: long_description = fh.read()

setuptools.setup(
    name="seleniumprocessor",
    version="0.1.2",
    author="Enrico Cambiaso",
    author_email="enrico.cambiaso@gmail.com",
    description="A simple library to set up Selenium processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/auino/seleniumprocessor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
