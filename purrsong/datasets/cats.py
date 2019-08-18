import os
import zipfile
# from purrsong.datasets.utils import download_from_google_drive, extract_zip
from utils import download_from_google_drive, extract_zip, extract_tar

def load_data():
    url = "https://drive.google.com/a/korea.ac.kr/uc?export=download"
    id = '1CYLFjew3Zf9agoSIbxPuIn1YDtgjc9dn'
    savedir = os.path.join(os.path.expanduser('~'), '.purrsong','datasets')
    filename = 'cats.tar.gz'
    filepath = os.path.join(savedir, filename)
    datadir = os.path.dirname(filepath)
    
    download_from_google_drive(url, id, savedir, filename)
    
def extract(filepath):
    extract_tar(filepath)

if __name__ == "__main__":
    load_data()
    # extract_data(filepath)

