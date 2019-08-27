import purrsong as ps
import matplotlib.pyplot as plt

if __name__ == "__main__":
    st = ps.StyleTransfer('cat.jpg','7.jpg')
    st.transfer_image()
