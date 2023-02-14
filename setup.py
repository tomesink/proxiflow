from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

NAME = 'adprep'

setup(
    name='adprep',
    version='0.1.0',
    description='Data Preprocessing tool in python',
    author='Martin Tomes',
    author_email='tomesm@gmail.com',
    license='MIT',
    url='https://github.com/tomesm/adprep',
    packages=find_packages(),
    zip_safe=False,
)