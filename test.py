import purrsong as ps
import matplotlib.pyplot as plt

if __name__ == "__main__":
    cats = ps.load_cats()
    img = cats.right_ear_img(44)
    plt.imshow(img)
    plt.show()
    
    