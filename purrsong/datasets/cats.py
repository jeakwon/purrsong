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

    def __call__(self, idx, factor=1.7):
        return {
            'image'         : self.image(idx),
            'landmark'      : self.landmark(idx),
            'face'          : self.face(idx, factor),
            'face_bb'       : self.face_bb(idx, factor),
            'face_img'      : self.face_img(idx, factor),
            'face_lmk'      : self.face_lmk(idx, factor),
            'eye'           : self.eye(idx, factor),
            'left_eye_bb'   : self.left_eye_bb(idx, factor), 
            'left_eye_img'  : self.left_eye_img(idx, factor), 
            'right_eye_bb'  : self.right_eye_bb(idx, factor),
            'right_eye_img' : self.right_eye_img(idx, factor), 
            'nose'          : self.nose(idx, factor),
            'nose_bb'       : self.nose_bb(idx, factor),
            'nose_img'      : self.nose_img(idx, factor),
            'ear'           : self.ear(idx, factor),
            'left_ear_bb'   : self.left_ear_bb(idx, factor), 
            'left_ear_img'  : self.left_ear_img(idx, factor), 
            'right_ear_bb'  : self.right_ear_bb(idx, factor), 
            'right_ear_img' : self.right_ear_img(idx, factor), 
        }
        
    def __getitem__(self, idx):
        return {
            'image'     : self.image(idx), 
            'landmark'  : self.landmark(idx),
        }

    def __len__(self):
        assert self.nimgs == self.nlmks, """Dataset corrupted.  Number of images 
        and landmarks does not match. Download fresh dataset."""
        return self.nimgs

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

    def face_bb(self, idx, factor=1.7):
        """ Cat image face bounding box 
        
        :param idx: index of sample
        :type idx: int
        :param factor: magnification ratio if factor=2 
            returns twice larger area of min-max landmark.
        :type factor: float

        :returns: numpy.array of cat face bounding box
            factor option determinse size
        """
        lmk = self.landmark(idx)

        bb = np.array([
            lmk.min(axis=0),
            lmk.max(axis=0)
        ])
        
        lazy_bb = self._get_lazy_bb(bb, factor=factor)
        return lazy_bb

    def face_img(self, idx, factor=1.7):
        """ Cat face image
        
        :param idx: index of sample
        :type idx: int
        :param factor: magnification ratio if factor=2 
            returns twice larger area of min-max landmark.
        :type factor: float

        :returns: numpy.array of cat face image
            factor option determinse size
        """
        bb  = self.face_bb(idx, factor)
        img = self.image(idx)
        return self._cut_img_with_bb(img, bb)
    
    def face_lmk(self, idx, factor=1.7):
        """ Cat face landmark adjusted to face image
        
        :param idx: index of sample
        :type idx: int
        :param factor: magnification ratio if factor=2 
            returns twice larger area of min-max landmark.
        :type factor: float

        :returns: numpy.array of cat face landmark
            factor option determinse size
        """
        return self.landmark(idx)-self.face_bb(idx, factor)[0]

    def face(self, idx, factor=1.7):
        """ Cat face image, bounding box and landmark
        
        :param idx: index of sample
        :type idx: int
        :param factor: magnification ratio if factor=2 
            returns twice larger area of min-max landmark.
        :type factor: float

        :returns: dict of cat face image, and bounding box.
            factor option determinse size.
            ['img'], ['bb'], ['lmk']
        """
        return {
            'img'   : self.face_img(idx, factor), 
            'bb'    : self.face_bb(idx, factor), 
            'lmk'   : self.face_lmk(idx, factor)
        }

    def eye(self, idx, factor=1.7):
        """ Cat eye image, bounding box and landmark
        
        :param idx: index of sample
        :type idx: int
        :param factor: magnification ratio if factor=2 
            returns twice larger area of min-max landmark.
        :type factor: float

        :returns: dict of cat face image, and bounding box.
            factor option determinse size.
            ['left_img'], ['right_img'], ['left_bb'], ['right_bb']
        """
        return {
            'left_img'  : self.left_eye_img(idx, factor), 
            'right_img' : self.right_eye_img(idx, factor), 
            'left_bb'   : self.left_eye_bb(idx, factor), 
            'right_bb'  : self.right_eye_bb(idx, factor)
        }

    def left_eye_bb(self, idx, factor=1.7):
        landmark = self.landmark(idx)
        distance = np.linalg.norm(landmark[0]-landmark[1])

        bb = np.array(
            [landmark[0] - distance/5, 
             landmark[0] + distance/5])

        lazy_bb = self._get_lazy_bb(bb, factor=factor)
        return lazy_bb     

    def left_eye_img(self, idx, factor=1.7):
        bb  = self.left_eye_bb(idx, factor)
        img = self.image(idx)
        return self._cut_img_with_bb(img, bb)

    def right_eye_bb(self, idx, factor=1.7):
        landmark = self.landmark(idx)
        distance = np.linalg.norm(landmark[0]-landmark[1])

        bb = np.array(
            [landmark[1] - distance/5, 
             landmark[1] + distance/5])

        lazy_bb = self._get_lazy_bb(bb, factor=factor)
        return lazy_bb     

    def right_eye_img(self, idx, factor=1.7):
        bb  = self.right_eye_bb(idx, factor)
        img = self.image(idx)
        return self._cut_img_with_bb(img, bb)

    def nose(self, idx, factor=1.7):
        return {
            'bb'  : self.nose_bb(idx, factor), 
            'img' : self.nose_img(idx, factor), 
        }

    def nose_bb(self, idx, factor=1.7):
        landmark = self.landmark(idx)
        distance = np.linalg.norm(landmark[0]-landmark[1])

        bb = np.array(
            [landmark[2] - distance/4, 
             landmark[2] + distance/4])

        lazy_bb = self._get_lazy_bb(bb, factor=factor)
        return lazy_bb

    def nose_img(self, idx, factor=1.7):
        bb  = self.nose_bb(idx, factor)
        img = self.image(idx)
        return self._cut_img_with_bb(img, bb)

    def ear(self, idx, factor=1.7):
        return {
            'left_bb'   : self.left_ear_bb(idx, factor), 
            'left_img'  : self.left_ear_img(idx, factor), 
            'right_bb'  : self.right_ear_bb(idx, factor), 
            'right_img' : self.right_ear_img(idx, factor), 
        }

    def left_ear_bb(self, idx, factor=1.7):
        lmk = self.landmark(idx)
        lmk = lmk[3:6]
        bb = np.array([
            lmk.min(axis=0),
            lmk.max(axis=0)
        ])
        
        lazy_bb = self._get_lazy_bb(bb, factor=factor)
        return lazy_bb

    def left_ear_img(self, idx, factor=1.7):
        bb  = self.left_ear_bb(idx, factor)
        img = self.image(idx)
        return self._cut_img_with_bb(img, bb)

    def right_ear_bb(self, idx, factor=1.7):
        lmk = self.landmark(idx)
        lmk = lmk[6:9]
        bb = np.array([
            lmk.min(axis=0),
            lmk.max(axis=0)
        ])
        
        lazy_bb = self._get_lazy_bb(bb, factor=factor)
        return lazy_bb

    def right_ear_img(self, idx, factor=1.7):
        bb  = self.right_ear_bb(idx, factor)
        img = self.image(idx)
        return self._cut_img_with_bb(img, bb)

    @staticmethod
    def _cut_img_with_bb(img, bb):
        """Cut image with given bb"""
        x_min, y_min    = bb[0]
        x_max, y_max    = bb[1]
        return img[y_min:y_max, x_min:x_max]

    @staticmethod
    def _get_lazy_bb(bb, factor):
        """Scale up/down bounding box with given factor"""
        x_min, y_min    = bb[0]
        x_max, y_max    = bb[1]

        x   = x_max - x_min
        y   = y_max - y_min
        dx  = x*(factor-1)/2
        dy  = y*(factor-1)/2

        lazy_bb = np.array(
            [[x_min-dx, y_min-dy], 
             [x_max+dx, y_max+dy]])
        lazy_bb = lazy_bb.clip(0, lazy_bb.max()).round().astype(int)
        return lazy_bb
    
    @staticmethod
    def _rotate_coords(coords, radian, center=(0, 0)):
        """Rotate xy coords array with given angle and center"""
        coords = coords.copy()
        x_coords, y_coords = coords[:,0], coords[:,1]
        x_center, y_center = center
        x_adjust, y_adjust = x_coords-x_center, y_coords-y_center

        sin, cos = np.sin(radian), np.cos(radian)
        x_rotate = +cos*x_adjust +sin*y_adjust + x_center
        y_rotate = -sin*x_adjust +cos*y_adjust + y_center

        coords[:, 0] = x_rotate
        coords[:, 1] = y_rotate
        return coords

    @staticmethod
    def _horizontal_angle(coord_from, coord_to, radian):
        """Calculate anlge of two coords connected 
        line from horizontal plane"""
        x, y = coord_to - coord_from
        return np.arctan2(y, x)
    
    @staticmethod
    def _rotate_image(image, radian):
        """Rotate image with given anlge"""
        h, w = image.shape[:2]
        image_center = (w/2, h/2)
        degree = np.rad2deg(radian)
        rot_mat = cv2.getRotationMatrix2D(image_center, degree, 1.0)
        result = cv2.warpAffine(image, rot_mat, (w, h), flags=cv2.INTER_LINEAR)
        return result