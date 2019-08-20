import purrsong as ps
import os
import pandas as pd
from purrsong.utils.downloader import google_drive_download
if __name__ == "__main__":
    ps.load_data('cats')
    ps.load_model('bbs')