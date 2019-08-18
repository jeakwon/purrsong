import os
from purrsong.utils import google_drive_download, extract_tar

def load(fresh=False):
    """Returns directory that contains cat images and face landmarks.
    if not exist locally, download and extract automatically from google drive
    
    :param fresh: if True, proceed download and extract 
    :type fresh: bool
    :returns: data directory
    """
    destination = os.path.join(os.path.expanduser('~'), '.purrsong', 'datasets', 'cats.tar.gz')
    datadir = os.path.splitext(destination)[0]
    
    if fresh:
        id = '1CYLFjew3Zf9agoSIbxPuIn1YDtgjc9dn'
        download_done = google_drive_download(id, destination)
        if download_done:
            extract_done = extract_tar(destination)
            if extract_done:
                os.remove(destination)
        return datadir

    if not os.path.exists(datadir):
        if os.path.isfile(destination):
            try: # try extracting with existing file
                extract_done = extract_tar(destination)
                if extract_done:
                    os.remove(destination)
            except: # if corrupted, fresh download
                load(fresh=True) # recursive
        else:
            load(fresh=True) # recursive

    return datadir