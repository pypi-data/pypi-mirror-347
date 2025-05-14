from setuptools import setup, find_packages

setup(
    name='khmernames',
    version='0.1',
    packages=find_packages(),
    install_requires=['pandas', 'openpyxl'],
    author='Sammy KH',
    description='Khmer Name Generator with full/first/last names and export options',
    python_requires='>=3.6',
)
