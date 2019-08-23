import purrsong as ps

from purrsong.apps.catface import CatFaceDetector

if __name__ == "__main__":
    cfd=CatFaceDetector(bbs_model='bbs', lmks_model='lmks')
    imagedir = ps.join(ps.load_dataset('cats'), 'cats', 'CAT_00')
    jpgs = ps.listext(imagedir, ['jpg'])
    for jpg in jpgs:
        cfd.extract(ps.join(imagedir, jpg), ps.join(ps.DESKTOP, 'lmks', jpg+'.cat'))
    # ps.list_models()