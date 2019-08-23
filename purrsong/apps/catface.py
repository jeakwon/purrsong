import os
import cv2
import csv
import numpy as np
from purrsong.models.core import load
from tensorflow.keras.models import Model

class CatFaceDetector:
    def __init__(self, bbs_model=None, lmks_model=None):
        self.bbs    = self.load_model(bbs_model)
        self.lmks   = self.load_model(lmks_model)
        self.params = {}
    def load_model(self, model):
        if model is None:
            return None
        elif isinstance(model, Model):
            return model
        elif isinstance(model, str):
            return load(model)
        else: 
            raise(
                """Invalid argument. argument should be either 
                tensorflow.python.keras.engine.training.Model or str""")

    def detect(self, src, dst=None, factor=1.6):
        assert self.bbs, 'bbs model not loaded'
        image_input     = cv2.imread(os.path.join(src))
        model_input     = self.preprocess(image_input)
        model_output    = self.bbs.predict(model_input)
        image_output    = self.bbs_postprocess(model_output, image_input, factor)
        if dst:
            cv2.imwrite(dst, image_output)
        return image_output

    def extract(self, src, dst=None, factor=1):
        assert self.lmks, 'lmks model not loaded'
        image_input     = self.detect(src)
        model_input     = self.preprocess(image_input)
        model_output    = self.lmks.predict(model_input)
        lmks_output    = self.lmks_postprocess(model_output, image_input, factor)
        if dst:
            with open(dst, 'w') as f:
                for lmks in lmks_output:
                    f.write(str(lmks))
        return lmks_output

    def preprocess(self, image_input):
        image_input = image_input/255
        model_input = self._fit_model(image_input)
        return model_input

    def bbs_postprocess(self, model_output, image_input, factor):
        xy_pairs        = model_output[0].reshape((-1, 2))
        XY_pairs        = self._reverse_translocation(xy_pairs)
        lazy_bb         = self._get_lazy_bb(bb=XY_pairs, factor=factor)
        x_min, y_min    = lazy_bb[0]
        x_max, y_max    = lazy_bb[1]
        self.params['image_offset'] = lazy_bb[0]
        image_output    = image_input[y_min:y_max, x_min:x_max]
        return image_output

    def lmks_postprocess(self, model_output, image_input, factor):
        xy_pairs    = model_output[0].reshape((-1, 2))
        XY_pairs    = self._reverse_translocation(xy_pairs)
        lmks        = XY_pairs + self.params['image_offset']
        lmks        = lmks.reshape((-1, 1))
        return lmks

    def _fit_model(self, img):        
        _, *input_shape = self.bbs.input_shape
        img             = self._resize_and_padding(img, input_shape[:2])
        model_input     = img.reshape(1, *input_shape)
        return model_input
    
    def _resize_and_padding(self, src, size, color=[0, 0, 0]):   
        # resize image. h: height, w: width, src: source, dst: destination
        h_src, w_src = src.shape[:2]
        h_dst, w_dst = size[:2]
        ratio        = max(h_dst, w_dst)/max(h_src, w_src)
        self.params['ratio'] = ratio
        h_new, w_new = int(h_src*ratio), int(w_src*ratio)
        resized_img = cv2.resize(src, (w_new, h_new)) # (width, height) format

        # padding image. t: top, b: bottom, l: left, r: right, d: delta
        dh, dw = (h_dst-h_new), (w_dst-w_new)
        t, l = int(dh/2), int(dw/2), 
        b, r = int(dh-t), int(dw-l), 
        offset  = np.array([l, t])
        self.params['offset'] = offset
        padded_img = cv2.copyMakeBorder(resized_img, t, b, l, r, cv2.BORDER_CONSTANT, value=color)
        return padded_img

    def _reverse_translocation(self, xy_pairs):
        ratio   = self.params['ratio']
        offset  = self.params['offset']

        # (x, y) -> (X, Y)
        XY_pairs = ((xy_pairs - offset)/ratio).astype(np.int) 
        return XY_pairs

    
    def _get_lazy_bb(self, bb, factor=1):
        x_min, y_min = bb[0]
        x_max, y_max = bb[1]

        x = x_max - x_min
        y = y_max - y_min
        dx  = int(x*(factor-1)/2)
        dy  = int(y*(factor-1)/2)

        lazy_bb = np.array(
            [[x_min-dx, y_min-dy], 
            [x_max+dx, y_max+dy]])
        lazy_bb = lazy_bb.clip(0, lazy_bb.max())
        return lazy_bb
