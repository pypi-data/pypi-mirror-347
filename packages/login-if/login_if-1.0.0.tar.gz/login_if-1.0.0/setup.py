from setuptools import setup, find_packages

setup(
    name='login-if',
    version='1.0.0',
    description='API key verification library for secure login checks',
    author='OUBStudios',
    packages=find_packages(),
    install_requires=['requests'],
    python_requires='>=3.6',
)