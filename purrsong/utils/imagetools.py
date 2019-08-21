import os
import cv2
import numpy as np
from purrsong import models

class CatFaceDetector(models.load('bbs')):
    def __init__(self):
        pass
    
    def detect(self, src, dst):
        image_input     = cv2.imread(os.path.join(src))
        model_input     = self.preprocess(image_input)
        model_output    = self.predict(model_input)
        image_output    = self.postprocess(model_output)
        cv2.imwrite(dst, image_output)
        return image_output

    def preprocess(self, image_input):
        _, *input_shape = self.input_shape
        model_input     = self._resize_and_padding(image_input, input_shape)
        return model_input

    def _resize_and_padding(self, src, dst, color=[0, 0, 0]):

        # (height, width) format
        h_src, w_src = src.shape[:2]
        h_dst, w_dst = dst.shape[:2]
        ratio   = max([h_dst, w_dst])/max([h_src, w_src])
        h_new, w_new = int(h_src*ratio), int(w_src*ratio)

        # (width, height) format
        resized_img = cv2.resize(src, (w_new, h_new))

        dh, dw = (h_new-h_dst), (w_new-w_dst) # delta_h, delta_w
        top, left = int(dh/2), int(dw/2) # top, left
        bottom, right = int(dh-top), int(dw-left) # bottom, right

        model_input = cv2.copyMakeBorder(resized_img, 
            top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        offset  = np.array([top, left])
        self.params = {
            'ratio'     : ratio,
            'offset'    : offset,
        }
        return model_input

    def postprocess(self, model_output):
        image_output = self._reverse_translocation(loc=model_output)
        return image_output

    def _reverse_translocation(self, loc):
        ratio   = self.params['ratio']
        offset  = self.params['offset']

        x_min, y_min, x_max, y_max = loc[0]
        pred_bb = np.array([[x_min, y_min],[x_max, y_max]])
        orig_bb = ((pred_bb - offset)/ratio).astype(np.int)

        # 이어서
