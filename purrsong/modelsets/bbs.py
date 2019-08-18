import os
from purrsong.utils import google_drive_download

def load(fresh=False):
    """Returns directory that contains cat images and face landmarks.
    if not exist locally, download and extract automatically from google drive
    
    :param fresh: if True, proceed download and extract 
    :type fresh: bool
    :returns: bbs filepath
    """
    destination = os.path.join(os.path.expanduser('~'), '.purrsong', 'modelsets', 'bbs.h5')
    
    if fresh:
        id = '14GKBs17iiO-y0fdsOsO1khBtegf2RB3c'
        download_done = google_drive_download(id, destination)
        if download_done:
            return destination

    if not os.path.isfile(destination):
        load(fresh=True)
    return destination
