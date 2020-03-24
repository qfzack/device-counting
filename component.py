import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import pandas as pd
import xlwt

# 显示所有的连通区域
def show_components(thresh):
    # Marker labelling
    ret, markers = cv2.connectedComponents(thresh)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1000

    # Now, mark the region of unknown with zero
    # markers[gray!=255]=0
    markers[thresh!=255]=0

    plt.figure(figsize=(12,12))
    plt.imshow(markers)
    plt.colorbar()

# 计算所有的连通区域及相关的信息
def comput_components(thresh):
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    # stats = [x0, y0, width, height, area]
    l = sorted(np.array(stats)[:,-1])
    print('区域的面积最大值前10：',l[-10:])

    area = []  #圆环内的区域面积
    for s in stats:
        area.append(s[-1])
    return labels,stats,area

def comput_average_area(area,l,r):
    count = 0
    area_sum = 0
    for a in area:
        if a>=l and a<r:
            count += 1
            area_sum += a
    return area_sum/count

# 计算连通区域的面积分布
def comput_distribution(area, show=False):
    number = []
    axis_area = []
    dis = 10
    area = np.array(area)
    for i in range(0, max(area), dis):
        axis_area.append(i + dis)
        number.append(((area >= i) & (area < i + dis)).sum())

    area_dic = []
    for i in range(len(number)):
        if (number[i] != 0):
            area_dic.append([axis_area[i] - dis, axis_area[i], number[i]])

    if (show):
        for i in range(len(number)):
            if (number[i] != 0):
                print(f'面积区间为：{axis_area[i] - dis}-{axis_area[i]}, 面积区间内的器件数量为：{number[i]}')
        plt.figure(figsize=(20, 8))
        plt.subplot(1, 2, 1)
        plt.plot(axis_area[:200], number[:200], 'g.-', linewidth=1.5)
        plt.title('the relationship of area and number')
        plt.xlabel('area')
        plt.ylabel('number')

        plt.subplot(1, 2, 2)
        plt.bar(axis_area[:200], number[:200], width=8, log=True)
        plt.title('the relationship of area and number')
        plt.xlabel('area')
        plt.ylabel('number')
    return area_dic