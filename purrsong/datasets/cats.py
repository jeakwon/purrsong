import os
from purrsong.datasets.downloader import download_file_from_google_drive

def load_data():
    file_id = '1n9AzQxoXQx8fGdew_7tuuFRTopmRzGas'
    download_file_from_google_drive(file_id,'cats.zip')
