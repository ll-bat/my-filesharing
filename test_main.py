import math
from PIL import Image
from working_version.core.helpers import ScreenshotHelper
import pickle 
import zlib
import cv2 
import psutil
import time
import numpy as np

screenshot_helper = ScreenshotHelper()

np_array = screenshot_helper.get_screenshot() 

# def get_size(array):
#     image_bytes = pickle.dumps(array) 
#     delimeter_bytes = pickle.dumps('@')
#     compressed_image_bytes = zlib.compress(image_bytes)
#     return (len(compressed_image_bytes + delimeter_bytes))


# print('original image size: %s' % get_size(np_array)) 
# for i in range(500):
#     for j in range(1, len(np_array[0]), 15):
#         np_array[i][j] = [0, 0, 0, 100]

img = Image.fromarray(np_array)
# img.show() 

converted_img = img.convert(mode='P', colors=250)
converted_img.show()

print(np.array(converted_img))
# print('changed image size: %s' % get_size(np_array)) 
