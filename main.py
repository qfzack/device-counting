import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import pandas as pd
import xlwt

from transformation import *
from component import *
from compute import *

if __name__ == "__main__":
    dir_path = './data'  #tiff文件
    png_path = './data_png'  #png文件
    save_path = './counting_result/'  #保存结果的路径

    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    file_list = []
    for name in os.listdir(dir_path):
        if name[-4:] == 'tiff':
            file_list.append(name)

    for file_name in file_list:
        print("*********************************")
        ori = show_tiff(dir_path, file_name, True)
        ori_tmp = read_img(png_path, file_name, True)
        thresh = tiff_to_binary_adapt(ori, True)
        show_components(thresh)
        labels, stats, area = comput_components(thresh)
        area_dic = comput_distribution(area, True)
        section, n, start, maxv, single_area = comput_number(area,area_dic)
        result = plot_result(section, n, start, maxv, ori_tmp, stats, labels, single_area, True)
        cv2.imwrite(save_path + file_name[:-5] + '_result.png', result)
        print("save success!")