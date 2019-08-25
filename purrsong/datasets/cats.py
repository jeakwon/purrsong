import os
import cv2
import numpy as np
from purrsong.datasets.core import load

def load_cats(fresh=False):
    return Cats(fresh=fresh)

class Cats:
    """Cat Face Landmarks dataset."""
    def __init__(self, fresh=False):
        self.root_dir   = load(name='cats', fresh=fresh)
        self.imgs_dir   = os.path.join(self.root_dir, 'imgs')
        self.lmks_dir   = os.path.join(self.root_dir, 'lmks')
        self.imgs_list  = [os.path.join(self.imgs_dir, f) for f in os.listdir(self.imgs_dir)]
        self.lmks_list  = [os.path.join(self.lmks_dir, f) for f in os.listdir(self.lmks_dir)]
        self.nimgs      = len(self.imgs_list)
        self.nlmks      = len(self.lmks_list)

    def __len__(self):
        assert self.nimgs == self.nlmks, """Dataset corrupted.  Number of images 
        and landmarks does not match. Download fresh dataset."""
        return self.nimgs

    def __getitem__(self, idx):
        return {'image': self.image(idx), 'landmark': self.landmark(idx)}

    def image(self, idx):
        filename = os.path.join(self.imgs_dir, f'{idx:05}.jpg')
        return cv2.imread(filename)

    def landmark(self, idx):
        filename = os.path.join(self.lmks_dir, f'{idx:05}.npy')
        return np.load(filename)