from setuptools import setup, find_packages

setup(
    name='unlimited_time',
    version='0.1.0',
    packages=find_packages(),
    description='A library to work with all possible time values and limitations.',
    long_description='This library helps to limit time ranges and provides a list of all possible months, years, seconds, minutes, etc.',
    long_description_content_type='text/plain',
    author='OUBStudios',
    author_email='oubstudios@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
