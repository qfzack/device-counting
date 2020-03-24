from PIL import Image
import os
import matplotlib.pyplot as plt
import cv2
from skimage.color import gray2rgb
import numpy as np

if __name__ == "__main__":
    path = './data'
    file_list = []
    if not os.path.isdir('./data_png'):
        os.mkdir('./data_png/')
    for name in os.listdir(path):
        if name[-4:]=='tiff':
            img = cv2.imread('./data/'+name,cv2.IMREAD_UNCHANGED)
            maxv = max([max(l) for l in img])
            img = (img/maxv)*255
            cv2.imwrite('./data_png/'+name[:-5]+'_trans.png',img)
            print("save success!")