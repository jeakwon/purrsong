import os
import requests
import zipfile
import tarfile

def download_from_google_drive(url, id, savedir, filename):
    session = requests.Session()
    response = session.get(url, params = { 'id' : id }, stream = True)
    token = _get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(url, params = params, stream = True)
    filepath = _save_response_content(response, savedir, filename)    
    return filepath

def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def _save_response_content(response, savedir, filename):
    os.makedirs(savedir, exist_ok=True)
    tmpfilename = filename+'.tmp'
    tmpfilepath = os.path.join(savedir, tmpfilename)
    filepath = os.path.join(savedir, filename)

    try:
        CHUNK_SIZE = 1024*1024 # 1 Mega Byte
        with open(tmpfilepath, "wb") as f:
            for MB, chunk in enumerate(response.iter_content(CHUNK_SIZE), start=1):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    print(f'{MB:} MB Downloaded,', end='\r')

        os.rename(tmpfilename, filename, savedir, savedir)
        print(f'{filepath} download complete. total size [{MB:} MB],')
        return True
    except:
        print(f'{filepath} download failed.')
        os.remove(tmpfilename, savedir)
        return False

    
def extract_zip(filepath):
    dirpath = os.path.dirname(filepath)
    
    zf = zipfile.ZipFile(filepath)
    uncompress_size = sum((file.file_size for file in zf.infolist()))
    extracted_size = 0
    for file in zf.infolist():
        extracted_size += file.file_size
        print(f'{extracted_size/uncompress_size:3.2%}', end='\r')
        zf.extract(file)
    zf.close()
    return dirpath

def extract_tar(filepath):
    dirpath = os.path.dirname(filepath)

    with tarfile.open(filepath, "r:gz") as tar:
        print('preparing tar.gz extraction...', end='\r')
        members = tar.getmembers()
        for i, f in enumerate(members):
            print(f'[{i/len(members):7.2%}] extracting {f.name:<100}', end='\r')
            tar.extract(f, dirpath)
        print(f'[{i/len(members):7.2%}] extract completed. filepath: {dirpath}')

    return dirpath
