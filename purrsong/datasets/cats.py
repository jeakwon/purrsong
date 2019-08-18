import os
from downloader import download_file_from_google_drive

def load_data():
    file_id = '1n9AzQxoXQx8fGdew_7tuuFRTopmRzGas'
    download_file_from_google_drive(file_id,'cats.zip')

if __name__ == "__main__":
    load_data()