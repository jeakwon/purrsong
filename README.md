# purrsong

# Create Anaconda Environment(Optional)
```console
conda create -n purrsong python=3.6
conda activate purrsong
```

# Requirments
```console
pip install tensorflow # tensorflow-gpu
pip install opencv-python
pip install tqdm
pip install requests
```

# Installation
```console
pip install purrsong
```

# Start
```python
import purrsong as ps
ps.__version__
>>> 0.1.0
```

# Auto-download-extract-load of datasets, modelsets
Below function automatically download data or models and save locally
If data is already exists, returns data directory or model filepath
```python
import purrsong as ps
ps.load_cats()
>>> C:\Users\Jay\.purrsong\datasets\cats.tar
ps.load_bbs()
>>> C:\Users\Jay\.purrsong\modelsets\bbs.h5
lmks = ps.load_lmks()
>>> C:\Users\Jay\.purrsong\modelsets\lmks.h5
```
