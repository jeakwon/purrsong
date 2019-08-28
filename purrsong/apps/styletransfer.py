"""
DEV enviornment

python 3.6.5
tensorflow 1.11.0
scipy 1.1.0
matplotlib 3.1.0
numpy 1.13.3
cv2 4.1.0

"""

from tensorflow.keras.preprocessing.image import load_img, save_img, img_to_array
from tensorflow.keras.applications import vgg19
from tensorflow.keras import backend as K

from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
import cv2
from tqdm import tqdm

# content Loss에 사용되는 Layer
CONTENT_LAYER = 'block5_conv2'

# Style Loss에 사용되는  Layer
STYLE_LAYERS = ['block1_conv1', 
                'block2_conv1',
                'block3_conv1',
                'block4_conv1',
                'block5_conv1']

class StyleTransfer:
    """Style Transfer
    
    :param content_path: content image source. provide file path
        -type content_path: str
    :param style_path: style image source. provide file path
        -type style_path: str
    :param dst: style_transferred_image save path
        -type dst: str   
    :param iterations: transfer model iteration
        -type iterations: int   
    :param content_weight: content loss weight. @default=0.25
        -type content_weight: float
    :param style_weight: style loss weight. @default=1.5
        -type style_weight: float
    :param total_variation_weight: total variation weight. @default=1e-4
        -type total_variation_weight: float
    :param img_height: define image height. @default=400
        -type img_height: int
     
    
    -------------------------
    
    Transfer Method::
    
       transfer_image()

    -------------------------
    
    Example) :
    import purrsong as ps
    
    content_path = ".../cat.jpg"
    style_path   = ".../awesome_style.jpg"
    dst          = ".../cat"
    st           = ps.StyleTransfer(content_path, style_path, dst, iterations=20, content_weight=0.25, style_weight=1.5, total_variation_weight=1e-4, img_height=400)
    st.transfer_image()
    
    :
    """
    
    def __init__(self, content_path, style_path, dst=None, iterations=20, content_weight=0.25, style_weight=1.5, total_variation_weight=1e-4, img_height=400):
        self.content_img            = self.read_image(content_path)
        self.style_img              = self.read_image(style_path)
        self.dst                    = dst
        self.iterations             = iterations
        self.style_weight           = style_weight
        self.content_weight         = content_weight
        self.total_variation_weight = total_variation_weight
        
        self.loss_value             = None
        self.grads_values           = None
        
        # 생성될 이미지 사이즈
        height, width               = self.content_img.shape[:-1]
        self.img_height             = img_height
        self.img_width              = int(width * self.img_height / height)
        self.combination_image      = K.placeholder((1, self.img_height, self.img_width, 3))
        
        
        content_image               = K.constant(self.preprocess_image(self.content_img))
        style_image                 = K.constant(self.preprocess_image(self.style_img))
        
        input_tensor                = K.concatenate([content_image, 
                                                     style_image,
                                                     self.combination_image], axis=0)
        total_loss                  = self.cal_total_loss(input_tensor)
        gradient                    = K.gradients(total_loss, self.combination_image)[0]
        self.fetch_loss_and_grads   = K.function(inputs=[self.combination_image], outputs=[total_loss, gradient])
        print('Initialized Style Transfer....')

    # image 불러오기
    def read_image(self, image):
        """read_image
        :pram image: image source from users
        :return:image to preprocess_image
        :type return: np.array
        """
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
        
    # image size 맞추기
    def preprocess_image(self, image):
        """preprocess_image
        :param image: image source from read_image method
        :return: image to input. 
        :type return: np.array
         
        """
        img = cv2.resize(image, dsize=(self.img_width, self.img_height), interpolation=cv2.INTER_LINEAR)
        img = np.expand_dims(img, axis=0)
        img = vgg19.preprocess_input(img)
        return img    

    def deprocess_image(self, x):
        """deprocess_image
        """
    
        # Remove zero-center by mean pixel
        x[:, :, 0] += 103.939
        x[:, :, 1] += 116.779
        x[:, :, 2] += 123.68
        # BGR->RGB
        x           = x[:, :, ::-1]
        x           = np.clip(x, 0, 255).astype('uint8')
        return x
    
    # vgg19 불러오기
    def load_model(self, input_tensor):
        """load_model
        @Load Model VGG19
        
        :param input_tensor: dedicate input shape to use in VGG19
            -type input_tensor : tensoflow Tensor
            
        :return: model (VGG19)
        """
        model = vgg19.VGG19(input_tensor=input_tensor,weights='imagenet', include_top=False)
        return model
    
    def define_content_loss(self, content_features, combination_features):
        """define_content_loss
        @Define Content Loss
            sum((combination_features - content_features)^2)
            
        :param content_features : content features from VGG19
        :param combination_features : combination_features features from VGG19
        
        :return to : cal_content_loss method
        
        """
        return K.sum(K.square(combination_features - content_features))
    
    def cal_content_loss(self, model, loss):
        """cal_content_loss
        @Calculate Content Loss
            content weight * content loss
        
        :param model : VGG19
        :param loss : current loss
        
        :return to : cal_total_loss method
        
        :using layer of VGG19 : 
        ['block5_conv2']
        
        """
        layer_features         = model.get_layer(CONTENT_LAYER).output
       
        content_image_features = layer_features[0, :, :, :]
        combination_features   = layer_features[2, :, :, :]

        loss                   = loss + self.content_weight * self.define_content_loss(content_image_features, combination_features)
        
        return loss
    
    def gram_matrix(self, x):
        """gram_matrix
        
        @define gram matrix
        
        :return to : define_style_loss
        
        """
        features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
        gram     = K.dot(features, K.transpose(features))
        return gram
    
    def define_style_loss(self, style_features, combination_features):
        """define_style_loss
        @Define Style Loss
            1/4*(1/channels^2)*(1/size^2)*sum(gram(style) - gram(combination)) 
            
        :param content_features : content features from VGG19
        :param combination_features : combination_features features from VGG19
        
        :return to : cal_style_loss method
        
        """
        S        = self.gram_matrix(style_features)
        C        = self.gram_matrix(combination_features)
        channels = 3 
        size     = self.img_height * self.img_width

        return K.sum(K.square(S - C)) / (4. * (channels**2) * (size**2))
    
    def cal_style_loss(self, model, loss):
        
        """cal_style_loss
        @Calculate Style Loss
            style weight * content loss / length(style layers)
        
        :param model : VGG19
        :param loss : current loss
        
        :return to : cal_total_loss method
 
        :using layer of VGG19 :
        ['block1_conv1','block2_conv1','block3_conv1','block4_conv1','block5_conv1']

        """
        for layer_name in STYLE_LAYERS:
            layer_features       = model.get_layer(layer_name).output
            style_features       = layer_features[1, :, :, :]
            combination_features = layer_features[2, :, :, :]
            s1                   = self.define_style_loss(style_features, combination_features)
            loss                 = loss + (self.style_weight / len(STYLE_LAYERS)) * s1

        return loss
    
    def total_variation_loss(self, x) :
        """total_variation_loss
        @Total Variation Loss
        
        :return to : cal_total_loss method        
        """
    
        # y축으로의 변화
        a = K.square(x[:, :self.img_height - 1, :self.img_width - 1, :] - x[:, 1:, :self.img_width - 1, :])
        # x축으로의 변화 
        b = K.square(x[:, :self.img_height - 1, :self.img_width -1, :] - x[:, :self.img_height - 1, 1:, :])
        
        return K.sum(K.pow(a + b, 1.25))
    
    def cal_total_loss(self, input_tensor):
        """cal_total_loss
        
        total loss = content loss + style loss + total variation loss
        
        """
        model              = self.load_model(input_tensor)

        default_loss       = K.variable(0.)
        content_loss       = self.cal_content_loss(model, default_loss)
        content_style_loss = self.cal_style_loss(model, content_loss)
        total_loss         = content_style_loss + self.total_variation_weight * self.total_variation_loss(self.combination_image)
        
        return total_loss
        
    def func_loss(self, x):
        """func_loss
        loss placeholder for fmin_l_bfgs_b optimizer
        
        :return to : generator method
        """
        assert self.loss_value is None
        x                 = x.reshape((1, self.img_height, self.img_width, 3))
        outs              = self.fetch_loss_and_grads([x])
        loss_value        = outs[0]
        grad_values       = outs[1].flatten().astype("float64")
        self.loss_value   = loss_value
        self.grads_values = grad_values
        return self.loss_value

    def func_grads(self, x):
        """func_grads
        grad placeholder for fmin_l_bfgs_b optimizer
        
        :return to : generator method
        """
        assert self.loss_value is not None 

        grad_values      = np.copy(self.grads_values)
        self.loss_value  = None
        self.grad_values = None 

        return grad_values
    
    def generator(self, x, iterations):
        """generator
        @ Optimize loss and Generate Image      
        
        """
        for i in tqdm(range(iterations)):
            
            x, min_val, info = optimize.fmin_l_bfgs_b(func=self.func_loss,
                                                        x0=x,
                                                        fprime=self.func_grads,
                                                        maxfun=self.iterations)

            img              = x.copy().reshape((self.img_height, self.img_width, 3))
            img              = self.deprocess_image(img)
           
        plt.imshow(img)
        plt.axis('off')
        plt.show()   
        
        if self.dst:
            result_prefix = self.dst    
            fname         = result_prefix + '.jpg' 
            save_img(fname, img)
            print('image saved as {}'.format(fname))

    def transfer_image(self):
        """
        transfer_image
        
        :return: style_transferred_image. 
        :type return: np.array, image
        
        """
        x = self.preprocess_image(self.content_img)
        x = x.flatten()
        self.generator(x, self.iterations)


