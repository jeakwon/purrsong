# purrsong


## Installation
```console
pip install purrsong
```

## Start
```python
import purrsong as ps
ps.__version__
>>> 0.1.3
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
* pandas

## Auto-download-extract-load of datasets, modelsets
Below function automatically download data or models and save locally
If data is already exists, returns data directory or model filepath
```python
import purrsong as ps
import matplotlib.pyplot as plt

cats = ps.load_cats()
cat = cats[5]
img = cat['image']
lmk = cat['landmark']

plt.imshow(img)
plt.scatter(lmk[:,0], lmk[:,1])
plt.show()
```
