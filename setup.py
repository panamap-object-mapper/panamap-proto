from setuptools import setup, find_packages
from os import path


project_directory = path.abspath(path.dirname(__file__))


def load_from(file_name):
    with open(path.join(project_directory, file_name), encoding="utf-8") as f:
        return f.read()


setup(
    name="panamap-proto",
    version=load_from("panamap_proto/panamap_proto.version").strip(),
    description="Protobuf module for panamap",
    long_description=load_from("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/kirillsulim/panamap-proto",
    author="Kirill Sulim",
    author_email="kirillsulim@gmail.com",
    license="MIT",
    packages=find_packages(include=["panamap_proto",]),
    package_data={"panamap_proto": ["panamap_proto.version",]},
    test_suite="tests",
    install_requires=["panamap>=1.2.0", "protobuf",],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="object mapper, protobuf",
)
