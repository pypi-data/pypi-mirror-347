from setuptools import setup, find_packages

setup(
    name='emcee_package',
    version='0.2.0',
    author='Emcee',
    description='A Test package',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[],
    entry_points={
        "console_scripts":["emcee-bye = emcee_package:bye"]
    }
)