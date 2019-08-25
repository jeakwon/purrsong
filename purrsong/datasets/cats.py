import os
import cv2
import numpy as np
from purrsong.datasets.core import load

def load_cats(fresh=False):
    """load cats dataset
        :param fresh: if True, download fresh dataset 
        :type fresh: Bool
        :returns: Cats instance

        :examples:
            import purrsong as ps
            cats = ps.load_cats
            cats[0] # idx 0 data dict. keys = 'image', 'landmark'
            cats.image(0) # idx 0 image
            cats.landmark(0) # idx 0 landmark
    """
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
        """ Cat image array

        :param idx: index of sample
        :type idx: int
        :returns: numpy.array
        """
        filename = os.path.join(self.imgs_dir, f'{idx:05}.jpg')
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img 

    def landmark(self, idx):
        """ Cat landmark array 

        :param idx: index of sample
        :type idx: int
        :returns: numpy.array, colums = x, y rows = position
        """
        filename = os.path.join(self.lmks_dir, f'{idx:05}.npy')
        lmk = np.load(filename)
        return lmk

    def face(self, idx, factor=1.7):
        """ Cat image array 
        
        :param idx: index of sample
        :type idx: int
        :param factor: magnification ratio if factor=2 
            returns twice larger area of min-max landmark.
        :type factor: float

        :returns: numpy.array of cat face. 
            factor option determinse size
        """
        img = self.image(idx)
        lmk = self.landmark(idx)

        bb = np.array([
            lmk.min(axis=0),
            lmk.max(axis=0)
        ])
        
        lazy_bb = self._get_lazy_bb(bb, factor=factor)

        x_min, y_min = lazy_bb[0]
        x_max, y_max = lazy_bb[1]

        return img[y_min:y_max, x_min:x_max]

    def _get_lazy_bb(self, bb, factor=1):
        x_min, y_min = bb[0]
        x_max, y_max = bb[1]

        x = x_max - x_min
        y = y_max - y_min
        dx  = x*(factor-1)/2
        dy  = y*(factor-1)/2

        lazy_bb = np.array(
            [[x_min-dx, y_min-dy], 
            [x_max+dx, y_max+dy]])
        lazy_bb = lazy_bb.clip(0, lazy_bb.max()).round().astype(int)
        return lazy_bb