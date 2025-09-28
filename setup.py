from setuptools import setup, find_packages

setup(
    name='qibo_qec',
    version='0.1',
    packages=find_packages(),
    install_requires=["qibo"],  # qui puoi aggiungere dipendenze
    author='Yehan Edirisinghe',
    description='A Quantum Error Correction (QEC) module for Qibo',
    
)