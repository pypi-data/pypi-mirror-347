from setuptools import setup
import os

# Read long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_desc = f.read()

packages = ['hobby_by_category']

setup(
    name='hobby-by-category',
    version='1.0.0', 
    author='Michael Anan Onimisi',
    author_email='247@therealMAO.com',
    description='Categorized list of hobbies',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/therealMAO247/hobby-by-category-py',
    packages=packages,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
    include_package_data=True,
    options={
        'bdist_wheel': {
            'universal': True
        }
    }
)