from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="a42_proto",
    version="0.1.4",
    author="Alexander Baumann",
    author_email="alexander.baumann@hs-esslingen.de",
    description="Protobuf Python bindings for A42 sensor data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HSE-VSV/DataReaderA42",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "protobuf==3.20.3",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
