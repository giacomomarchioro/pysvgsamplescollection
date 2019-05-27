import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="svgsamplescolletion",
    version="0.0.1",
    author="Giacomo Marchioro",
    author_email="giacomo.marchioro@outlook.com",
    description="This package allows creating samples collections drawing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giacomomarchioro/pysvgsamplescollection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
