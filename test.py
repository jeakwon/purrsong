import purrsong as ps
import os
import pandas as pd
from purrsong.utils.downloader import google_drive_download
if __name__ == "__main__":
    ps.list_datasets()
    ps.load_dataset('cats')
    ps.load_dataset('catdog')
    ps.load_model('bbs')
    ps.load_model('lmks')