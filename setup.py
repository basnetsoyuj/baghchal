import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baghchal",
    version="1.0.1",
    author="Soyuj Jung Basnet",
    author_email="bsoyuj@gmail.com",
    description="baghchal is a pure Python Bagh Chal library that supports game import, move generation, move validation and board image rendering. It also comes with a simple engine based on minimax algorithm and alpha-beta pruning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/basnetsoyuj/baghchal",
    install_requires=['numpy', 'Pillow'],
    include_package_data=True,
    packages=setuptools.find_packages(),
    keywords=['Bagh Chal', 'game environment', 'board game'],
    download_url='https://github.com/basnetsoyuj/baghchal/archive/v_1.0.1.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
