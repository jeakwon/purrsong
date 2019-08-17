# purrsong
purrsong related python development library


# 2019-08-17 devlog
### 1. Created new environment with anaconda
__anaconda version 4.7.10__
```
conda create -n purrsong python=3.6
conda activate purrsong
```

### 2. Installed libraries for development ###
```
pip install tensorflow
pip install opencv-python
```

### 3. Intalled libraries for PyPI upload ###
[Instructions, Korean](https://medium.com/@onlytojay/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B0%B0%ED%8F%AC-%ED%8C%A8%ED%82%A4%EC%A7%80-%EB%A7%8C%EB%93%A4%EA%B8%B0-%EC%A4%91%EA%B0%84%EA%B2%80%ED%86%A0-a2dade70c247)
```
pip install setuptools # Requirement already satisfied (--> conda env default provided)
pip install wheel # Requirement already satisfied (--> conda env default provided)
pip install twine
```

### 4. Clone this repo, add setup.py, setup.cfg
```
git clone https://github.com/jeakwon/purrsong.git
```
