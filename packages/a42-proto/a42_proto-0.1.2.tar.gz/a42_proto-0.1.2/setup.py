from setuptools import setup, find_packages

setup(
    name="a42_proto",
    version="0.1.2",
    packages=find_packages(include=["a42_proto", "a42_proto.*"]),
    package_dir={"": "."},
    install_requires=["protobuf==3.20.3"],
    include_package_data=True,
    description="Protobuf Python bindings for A42 sensor data",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Alexander Baumann",
    url="https://github.com/HSE-VSV/DataReaderA42",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
