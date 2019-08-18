import os
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/a/korea.ac.kr/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = _get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    filepath = _save_response_content(response, destination)    
    return filepath

def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def _save_response_content(response, destination):
    directory = os.path.join(os.path.expanduser('~'), '.purrsong','datasets')
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, destination)

    CHUNK_SIZE = 1024*1024

    with open(os.path.join(directory, destination), "wb") as f:
        for MB, chunk in enumerate(response.iter_content(CHUNK_SIZE), start=1):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                print(f'{MB:} MB Downloaded,', end='\r')
        print(f'Download Complete. Total size [{MB:} MB],')