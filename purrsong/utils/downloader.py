import os
import requests
from tqdm import tqdm

def google_drive_download(id, destination):
    """Download file from google drive with file id at destination
    
    :param id: google drive file id
    :type id: str
    :param destination: full file path to save
    :type destination: str
    :returns: True, destination (if download completed)
    """

    URL = 'https://docs.google.com/uc?export=download'

    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)

    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    CHUNK_SIZE = 32*1024
    total_size = int(response.headers.get('content-length', 0))
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    print('Start google_drive_download')
    with tqdm(desc=destination, total=total_size, unit='B', unit_scale=True) as pbar:
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:
                    pbar.update(CHUNK_SIZE)
                    f.write(chunk)
    return True
