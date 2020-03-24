import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import pandas as pd
import xlwt

# 读取并显示tiff文件的内容，返回中间区域
def show_tiff(dir_path, file_name, show=False):
    img = cv2.imread(os.path.join(dir_path, file_name), flags=-1)
    print("文件名称：", file_name)
    ori = img[500:2500, 500:2500]
    max_v = max([max(l) for l in ori])
    ori = ori/max_v*255
    ori = np.array(ori, dtype='uint8')
    if(show):
        plt.imshow(ori)
        plt.colorbar()
    return ori

def read_img(png_path, file_name, sign = False):
    img2 = cv2.imread(os.path.join(png_path, file_name[:-5]+'_trans.png'))
    ori_tmp = img2[500:2500, 500:2500]
    # print(max([max(l) for l in ori_tmp[0]]))
    if(sign):
        plt.imshow(ori_tmp)
        plt.colorbar()
    return ori_tmp

# 将tiff文件转换为二值图像
def tiff_to_binary(ori, show=False):
    max_value = max([max(l) for l in ori])
    value = max_value/2-5
    ret, thresh = cv2.threshold(ori, value, max_value, cv2.THRESH_BINARY_INV)
    thresh[thresh == max_value] = 255
    thresh = np.array(thresh, dtype='uint8')

    if(show):
        plt.figure(figsize=(12,12))
        plt.imshow(thresh)
        plt.colorbar()
    return thresh

def tiff_to_binary_adapt(ori, show=False):
    max_value = max([max(l) for l in ori])
    value = 9
    thresh = cv2.adaptiveThreshold(ori, max_value, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, value, 40)
    thresh[thresh == max_value] = 255
    thresh = np.array(thresh, dtype='uint8')

    if(show):
        plt.figure(figsize=(12, 12))
        plt.imshow(thresh)
        plt.colorbar()
    return thresh