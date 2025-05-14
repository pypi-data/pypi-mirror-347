from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="divisible_by_3_turing_machine",
    version="1.0.0",
    description="Check if a binary number is divisible by 3 using a Turing machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mohamed Khaled",
    author_email="mokhaled732003@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)