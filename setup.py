
from setuptools import setup, find_packages
import purrsong
from os import path 

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name                            = 'purrsong',
    version                         = purrsong.__version__,
    description                     = 'purrsong',
    author                          = 'jeakwon',
    author_email                    = 'onlytojay@gmail.com',
    url                             = 'https://github.com/jeakwon/ccpy',
    packages                        = find_packages(exclude = []),
    keywords                        = ['purrsong'],
    python_requires                 = '>=3.6',
    license                         = 'LICENSE.txt',
    install_requires                =  [],
    long_description                = long_description,
    long_description_content_type   = 'text/markdown'
)