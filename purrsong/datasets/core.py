import os
import json
import pandas as pd
import zipfile
import tarfile
from purrsong.utils import google_drive_download, extract

def load(name, fresh=False):
    """Returns directory that contains cat images and face landmarks.
    if not exist locally, download and extract automatically from google drive
    
    :param name: dataset name,
    :type name: str
    :param fresh: if True, proceed download and extract 
    :type fresh: bool
    :returns: data directory
    """
    # google dirve file id list
    datasets = list_datasets()
    if name not in datasets.index:
        datasets = list_datasets(name)
        if name not in datasets.index:
            raise(f'Dataset {name} not exists')

    dataset = datasets.loc[name]

    dataset_path = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'datasets', dataset['filename'])
    datadir = os.path.splitext(dataset_path)[0]
    

    if not os.path.exists(datadir):
        if os.path.isfile(dataset_path):
            try: # try extracting with existing file
                print(f'Extract dataset at {datadir}')
                extract(dataset_path)
            except: # if corrupted, fresh download
                print(f'Failed to extract {dataset_path}')
                fresh=True
        else: # if datadir not exists, fresh download
            fresh=True

    if fresh:
        print(f'Download dataset at {dataset_path}')
        download_done = google_drive_download(dataset['id'], dataset_path)
        if download_done:
            print(f'Extract dataset at {datadir}')
            extract(dataset_path)

    return datadir

def list_datasets(fresh=False, id='1kGtEoB--o_1cN0Zk9pogFsXqaISJUsQc'):
    """list all available _datasets by monitoring google drive.
    :param id: _datasets_list.csv file id in google drive
    :type id: str
    :returns: list of available _datasets as pd.DataFrame
    """
        
    datasets_list_csv = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'datasets_list.csv')

    if not os.path.isfile(datasets_list_csv): 
        fresh=True

    if fresh:
        google_drive_download(id, datasets_list_csv)

    return pd.read_csv(datasets_list_csv, index_col=0)