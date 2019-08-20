import os
from purrsong.utils import google_drive_download
from tensorflow.keras.models import load_model

# google dirve file id list
GDID = {
    'bbs.h5':'14GKBs17iiO-y0fdsOsO1khBtegf2RB3c',
    'lmks.h5':'1jzureRduuWcECqeqpDLY79mIEIYimcs5'
}

def load(filename, fresh=False):
    """Returns directory that contains cat images and face landmarks.
    if not exist locally, download and extract automatically from google drive
    
    :param filename: {'bbs'|'lmks'},
    :type filename: str
    :param fresh: if True, proceed download and extract 
    :type fresh: bool
    :returns: bbs filepath
    """

    model_path = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'models', filename)
    
    if not os.path.isfile(model_path):
        print(f'Model not exist at {model_path}')
        fresh=True

    if fresh:
        print(f'Downloading model at {model_path}')
        google_drive_download(GDID[filename], model_path)

    return load_model(model_path)
