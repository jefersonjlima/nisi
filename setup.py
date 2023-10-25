from setuptools import setup

with open('requirements.txt', 'rt') as f:
    requirements_list = [req[:-1] for req in f.readlines()]

setup(
    name='nisi',
    version='1.0.0',
    packages=['nisi', 'nisi.core'],
    url='https://gitlab.com/jeferson.lima/nisi',
    license='',
    author='Jeferson Lima',
    author_email='jefersonjl82@gmail.com',
    description='NisI: Non-Ideal System Identification',
    install_requires = requirements_list)
