import os
from purrsong.utils import google_drive_download

def load(fresh=False):
    """Returns directory that contains cat images and face landmarks.
    if not exist locally, download and extract automatically from google drive
    
    :param fresh: if True, proceed download and extract 
    :type fresh: bool
    :returns: lmks filepath
    """
    destination = os.path.join(os.path.expanduser('~'), '.purrsong', 'modelsets', 'lmks.h5')
    
    if fresh:
        id = '1jzureRduuWcECqeqpDLY79mIEIYimcs5'
        download_done = google_drive_download(id, destination)
        if download_done:
            return destination

    if not os.path.isfile(destination):
        load(fresh=True)
    return destination