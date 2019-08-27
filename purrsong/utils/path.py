import os

# PROPS
USER        = os.path.expanduser('~')
DESKTOP     = os.path.join(USER, 'DESKTOP')
PURRSONG    = os.path.join(USER, '.purrsong')
DATASETS    = os.path.join(USER, '.purrsong', 'datasets')
MODELS      = os.path.join(USER, '.purrsong', 'models')

# METHODS
def desktop(filename):
    return os.path.join(DESKTOP, filename)

def join(a, *p):
    return os.path.join(a, *p)

def listext(directory, ext=[], abspath=False):
    ls = []
    for f in os.listdir(directory):
        for e in ext:
            if f.lower().endswith(e.lower()):
                if abspath:
                    f = os.path.join(directory, f)
                ls.append(f)
    return ls