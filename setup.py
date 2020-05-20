import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cep_address",
    version="0.1",
    author="Sallve",
    author_email="tecnologia@sallve.com",
    description="A package for getting address data from CEP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sallve/cep_address",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
