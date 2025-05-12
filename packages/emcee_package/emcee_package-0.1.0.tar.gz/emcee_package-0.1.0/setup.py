from setuptools import setup, find_packages

setup(
    name='emcee_package',
    version='0.1.0',
    author='Emcee',
    description='A Test package',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[],
)