import os
import pandas as pd
from purrsong.utils import google_drive_download
from tensorflow.keras.models import load_model

def load(name, fresh=False):
    """Returns directory that contains cat images and face landmarks.
    if not exist locally, download and extract automatically from google drive
    
    :param name: model name,
    :type name: str
    :param fresh: if True, proceed download and extract 
    :type fresh: bool
    :returns: bbs filepath
    """
    models = list_models()
    if name not in models.index:
        models = list_models(fresh=True)
        if name not in models.index:
            raise(f'Model {name} not exists')

    model = models.loc[name]

    model_path = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'models', model['filename'])
    
    if not os.path.isfile(model_path):
        print(f'Model not exist at {model_path}')
        fresh=True

    if fresh:
        print(f'Downloading model at {model_path}')
        google_drive_download(model['id'], model_path)

    return load_model(model_path)

def list_models(fresh=False, id='13rBwrVEoU_aoF-KytmOJILD7Y8Tl8Vs1'):
    """list all available models by monitoring google drive.
    :param id: models_list.csv file id in google drive
    :type id: str
    :returns: list of available models as pd.DataFrame
    """
        
    models_list_csv = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'models_list.csv')

    if not os.path.isfile(models_list_csv): 
        fresh=True

    if fresh:
        google_drive_download(id, models_list_csv)
    
    return pd.read_csv(models_list_csv, index_col=0)
