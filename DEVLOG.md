

# 2019-08-17
### 0. Create this repo with
* LICENSE : GNU v3
* .gitignore : python
* README.md : for description of this repo

### 1. Create new environment with anaconda
anaconda version `4.7.10`
```
conda create -n purrsong python=3.6
conda activate purrsong
```

### 2. Install libraries for development ###
```
pip install tensorflow
pip install opencv-python
```

### 3. Install libraries for PyPI upload ###
[Instructions(Korean)](https://medium.com/@onlytojay/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B0%B0%ED%8F%AC-%ED%8C%A8%ED%82%A4%EC%A7%80-%EB%A7%8C%EB%93%A4%EA%B8%B0-%EC%A4%91%EA%B0%84%EA%B2%80%ED%86%A0-a2dade70c247)
```
pip install setuptools # Requirement already satisfied (--> conda env default provided)
pip install wheel # Requirement already satisfied (--> conda env default provided)
pip install twine
```

### 4. Clone this repo, add setup.py, setup.cfg
#### 4.1. cloned this repo
```
git clone https://github.com/jeakwon/purrsong.git
```

#### 4.2. added `setup.py`
```python
from setuptools import setup, find_packages

setup(
    name                = 'purrsong',
    version             = '0.0.1',
    description         = 'purrsong',
    author              = 'jeakwon',
    author_email        = 'onlytojay@gmail.com',
    url                 = 'https://github.com/jeakwon/ccpy',
    packages            = find_packages(exclude = []),
    keywords            = ['purrsong'],
    python_requires     = '>=3.6',
    license             = 'LICENSE.txt',
    install_requires    =  [],
)
```

#### 4.3. added `setup.cfg`
```
[metadata]
description-file = README.md
```

#### 4.4. current folder structure
```
purrsong
├── .gitignore
├── LICENSE
├── README.md
├── setup.cfg
└── setup.py
```

#### 4.5. git commit, push

### 5. Create empty PyPI package
#### 5.1. created `.whl` file
In the prompt, with `(purrsong)` env activated in `purrsong` directory, 
```
python setup.py bdist_wheel
```

#### 5.2. uploaded `.whl` file
Uploaded wheel with `twine` module
```
twine upload dist\purrsong-0.0.1-py3-none-any.whl
```
For your information, twine requires PyPI id/pw. register PyPI first.

#### 5.3. check upload
```
pip install purrsong
```

### 6. Add purrsong module
#### 6.1. added `purrsong` folder with `__init__.py`
```
purrsong
├── purrsong            # add folder
    └── __init__.py     # add __init__.py
├── .gitignore
├── LICENSE
├── README.md
├── setup.cfg
└── setup.py
```

#### 6.2. updated package
General procedure, when update
1. change `purrsong` module
2. change `setup.py` version (ex: 0.0.1->0.0.2)
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.2-py3-none-any.whl`
5. git push

#### 6.3. upgraded existing purrsong
```
pip install --upgrade purrsong
```

after sucessful upgrade, activate python kernel
```python
import purrsong
```
No error -> success

### 7. display for PyPI package 
added below code for PyPI display
```python
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # ...
    long_description                = long_description,
    long_description_content_type   = 'text/markdown'
)
```

### 8. Version control change
#### 8.1. adding __version__ in `purrsong/__init__.py`
__`__init__.py`__
```python
__version__ = 0.03
```

#### 8.2. change `setup.py` version from manual to automatic
__`setup.py`__
```python
import purrsong # add this line
setup(
    version = purrsong.__version__, # add this line
)
```

#### 8.3. updated package
General procedure, when update
1. change `purrsong` module
2. change `purrsong.__init__.py` version (__version__ = '0.0.3')
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.3-py3-none-any.whl`
5. git push
6. `pip install --upgrade purrsong`

#### 8.4. check update
```python
import purrsong
purrsong.__version__
>>> '0.0.3'
```