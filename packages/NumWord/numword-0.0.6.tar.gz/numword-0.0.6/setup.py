from setuptools import setup, find_packages

setup(
    name='NumWord',
    version='0.0.6',
    packages=find_packages(),
    install_requires=[],
    author='Harshit Dalal',
    author_email='harshitdalal96@gmail.com',
    description='Convert words to numbers, numbers to words, and humanized formats and currency conversion with live rates.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/HarshitDalal/NumWord',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'number', 'word', 'conversion', 'numbers2words',
        'number to word', 'word to number', 'num2words', 'words2number', 'numword'
    ],
    python_requires='>=3.6',
)
