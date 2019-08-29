# purrsong


## Installation
```console
pip install purrsong
```

## Start
```python
import purrsong as ps
ps.__version__
>>> 0.1.6
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
* matplotlib
* scipy

## Auto-download-extract-load of datasets, modelsets
Below function automatically download data or models and save locally
If data is already exists, returns data directory or model filepath

```python
import purrsong as ps

model_list = ps.list_models() # or ps.list_models(fresh=True)
print(model_list)
ps.load_model('bbs') # or ps.load_model('bbs', fresh=True)

dataset_list = ps.list_datasets() # or ps.list_datasets(fresh=True)
print(dataset_list)
ps.load_dataset('cat') # or ps.load_dataset('cat', fresh=True)
```

## Manipulating cats dataset
You can play with auto downloaded `cats` dataset by below example.
Try changing `factor` arg, which will return different size of bounding boxes.

#### load cats dataset
```python
import purrsong as ps
import matplotlib.pyplot as plt
cats = ps.load_cats()
```

#### showing cat image
```python
img = cats[0]['image']
plt.imshow(img)
plt.show()
```

#### showing cat image with landmark
```python
img = cats[0]['image']
lmk = cats[0]['landmark']
x, y = lmk.T
plt.imshow(img)
plt.scatter(x, y)
plt.show()
```

#### showing cat face image
```python
img = cats.face_img(44)  # or img = cats.face_img(idx=44, factor=1.7)
plt.imshow(img)
plt.show()
```

#### showing cat left eye image
```python
img = cats.left_eye_img(44)  # or img = cats.face_img(idx=44, factor=1.7)
plt.imshow(img)
plt.show()
```

#### available data features
```python
import purrsong as ps
cats = ps.load_cats()

cat = cats(0)         # or cats(idx=0, factor=1.7)

cat['image']          # cats.image(0)
cat['landmark']       # cats.landmark(0)
cat['face']           # cats.face(0, factor=1.7)
cat['face_bb']        # cats.face_bb(0, factor=1.7)
cat['face_img']       # cats.face_img(0, factor=1.7)
cat['face_lmk']       # cats.face_lmk(0, factor=1.7)
cat['eye']            # cats.eye(0, factor=1.7)
cat['left_eye_bb']    # cats.left_eye_bb(0, factor=1.7)
cat['left_eye_img']   # cats.left_eye_img(0, factor=1.7)
cat['right_eye_bb']   # cats.right_eye_bb(0, factor=1.7)
cat['right_eye_img']  # cats.right_eye_img(0, factor=1.7)
cat['nose']           # cats.nose(0, factor=1.7)
cat['nose_bb']        # cats.nose_bb(0, factor=1.7)
cat['nose_img']       # cats.nose_img(0, factor=1.7)
cat['ear']            # cats.ear(0, factor=1.7)
cat['left_ear_bb']    # cats.left_ear_bb(0, factor=1.7)
cat['left_ear_img']   # cats.left_ear_img(0, factor=1.7)
cat['right_ear_bb']   # cats.right_ear_bb(0, factor=1.7)
cat['right_ear_img']  # cats.right_ear_img(0, factor=1.7)
```
left dict form is much more intuitive and good 
when you have to handle many of features at the same time.  
right method way is good when you access specific feature.

# Style Transfer
```python
content_path = ".../cat.jpg"
style_path   = ".../awesome_style.jpg"
dst          = ".../cat"
st           = ps.StyleTransfer(content_path, style_path, dst, 
                                iterations=20, content_weight=0.25, style_weight=1.5, 
                                total_variation_weight=1e-4, img_height=400)
st.transfer_image()
```

#### Load User Image
```python
from purrsong.utils import load_user_image

image_path = ".../cat.jpg"
load_user_image(image_path)
```

