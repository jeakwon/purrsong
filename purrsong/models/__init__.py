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
    models = list_models(show=False)
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

def list_models(show=True, id='13rBwrVEoU_aoF-KytmOJILD7Y8Tl8Vs1'):
    """list all available models by monitoring google drive.
    :param id: models_list.csv file id in google drive
    :type id: str
    :returns: list of available models as pd.DataFrame
    """
    models_list_csv = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'models_list.csv')

    if not os.path.isfile(models_list_csv):
        google_drive_download(id, models_list_csv)
        new_models_list = pd.read_csv(models_list_csv, index_col=0)
        if show: print(new_models_list.index)
        return new_models_list
    
    else:
        old_models_list = pd.read_csv(models_list_csv, index_col=0)
        try:
            google_drive_download(id, models_list_csv)
            new_models_list = pd.read_csv(models_list_csv, index_col=0)
            if not old_models_list.equals(new_models_list):
                print("model list updated")
            if show: print(new_models_list.index)
            return new_models_list

        except: # maybe no internet connection
            if show: print(old_models_list.index)
            return old_models_list