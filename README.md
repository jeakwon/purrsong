# purrsong


## Installation
```console
pip install purrsong
```

## Start
```python
import purrsong as ps
ps.__version__
>>> 0.1.0
```

## Create Anaconda Environment(Optional)
```console
conda create -n purrsong python=3.6
conda activate purrsong
```

## Requirments
* tensorflow
* opencv-python
* tqdm
* requests

## Auto-download-extract-load of datasets, modelsets
Below function automatically download data or models and save locally
If data is already exists, returns data directory or model filepath
```python
import purrsong as ps
data = ps.load_cats()
bbs = ps.load_model('bbs.h5')
lmks = ps.load_model('lmks.h5')
```
