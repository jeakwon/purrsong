import os
import zipfile

def extract_zipfile(filepath):
    dirpath = os.path.splitext(filepath)[0]
    
    f = zipfile.ZipFile(filepath)
    f.extractall(dirpath)
    f.close()

    return dirpath