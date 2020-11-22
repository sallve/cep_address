from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="cep_address",
    version="0.1.2",
    author="Sallve",
    author_email="tecnologia@sallve.com",
    description="A package for getting address data from CEP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sallve/cep_address",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=["requests>=2.22.0,<3.0.0"],
    extras_require={
        "test": [
            "pytest==5.4.3",
            "vcrpy==4.1.0",
        ],
    },
)
