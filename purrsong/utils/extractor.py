import os
import zipfile
import tarfile
from tqdm import tqdm
    
def extract_zip(src):
    """Extract zip file
    
    :param src: .zip file
    :type src: str
    :param savedir: directory to save
    :type savedir: str
    :returns: True if extract completed
    """
    savedir = os.path.splitext(src)[0]

    with zipfile.ZipFile(src) as zf:
        for f in tqdm(zf.infolist(), desc=savedir):
            zf.extract(f, savedir)
    return True

def extract_tar(src):
    """Extract various tar files
    
    :param src: .tar|.tar.gz|.tar.bz2|.tar.xz file
    :type src: str
    :param savedir: directory to save
    :type savedir: str
    :returns: True if extract completed
    """
    savedir = os.path.splitext(src)[0]

    with tarfile.open(src) as tf:
        for f in tqdm(tf.getmembers(), desc=savedir):
            tf.extract(f, savedir)
    return True
