# setup.py
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mojtaba-first-test',
    version='0.1.1',
    author='Mojtaba',
    author_email='your-email@example.com',
    description='My first test Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mojtaba-first-test',
    package_dir={'': 'src'},
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
) 
