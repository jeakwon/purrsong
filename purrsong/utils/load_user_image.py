
import cv2

def load_user_image(image):
    """load_user_image

       @Load User Image
        - load input image from user
        - convert BGR to RGB

       :pram image: image source from users
       :return: RGB image
       :type return: np.array
     """
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    # convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
    
