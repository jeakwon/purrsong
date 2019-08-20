import os
import json
import pandas as pd
from purrsong.utils import google_drive_download, extract_tar

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
    datasets = list_datasets(show=False)
    dataset = datasets.loc[name]

    dataset_path = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'datasets', dataset['filename'])
    datadir = os.path.splitext(dataset_path)[0]
    

    if not os.path.exists(datadir):
        print(f'dataset not exist at {datadir}')
        if os.path.isfile(dataset_path):
            try: # try extracting with existing file
                print(f'Extract dataset at {datadir}')
                extract_done = extract_tar(dataset_path)
                if extract_done:
                    os.remove(dataset_path)
            except: # if corrupted, fresh download
                fresh=True
        else: # if datadir not exists, fresh download
            fresh=True

    if fresh:
        print(f'Download dataset at {dataset_path}')
        download_done = google_drive_download(dataset['gdid'], dataset_path)
        if download_done:
            print(f'Extract dataset at {datadir}')
            extract_done = extract_tar(dataset_path)
            if extract_done:
                os.remove(dataset_path)
        return datadir


    return datadir

def list_datasets(show=True, id='1kGtEoB--o_1cN0Zk9pogFsXqaISJUsQc'):
    """list all available _datasets by monitoring google drive.
    :param id: _datasets_list.csv file id in google drive
    :type id: str
    :returns: list of available _datasets as pd.DataFrame
    """
    datasets_list_csv = os.path.join(
        os.path.expanduser('~'), '.purrsong', 'datasets_list.csv')

    if not os.path.isfile(datasets_list_csv):
        google_drive_download(id, datasets_list_csv)
        new_datasets_list = pd.read_csv(datasets_list_csv, index_col=0)
        if show: print(new_datasets_list.index)
        return new_datasets_list
    
    else:
        old_datasets_list = pd.read_csv(datasets_list_csv, index_col=0).copy()
        try:
            google_drive_download(id, datasets_list_csv)
            new_datasets_list = pd.read_csv(datasets_list_csv, index_col=0)
            if not old_datasets_list.equals(new_datasets_list):
                print("dataset list updated")
            if show: print(new_datasets_list.index)
            return new_datasets_list

        except: # maybe no internet connection
            if show: print(old_datasets_list.index)
            return old_datasets_list