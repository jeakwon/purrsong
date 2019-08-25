import purrsong as ps

if __name__ == "__main__":
    cats = ps.load_cats()
    img = cats[0]['image']
    lmk = cats[0]['landmark']