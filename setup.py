import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="etl_data_reader-CaptainDario",
    version="2.0",
    author="CaptainDario",
    author_email="daapplab@gmail.com",
    description="A python package for conveniently handling the ETL data set",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CaptainDario/ETL_data_reader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)