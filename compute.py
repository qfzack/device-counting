import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import pandas as pd

def comput_single_area(area, start, end, maxv):
    all_area = 0
    all_num = 0
    area_sum = 0
    num = 0
    for a in area:
        if(a>=start and a<=end):
            area_sum += a
            num += 1
        if(a>=start and a<=maxv):
            all_area += a
            all_num += 1
    single_area = area_sum/num
    print(f'单个区域数量：{num}, 单个区域的面积：{single_area}')
    print(f'连通区域数量：{all_num}, 连通区域总面积：{all_area}')
    return single_area, all_area

def comput_number(area, area_dic):
    all_sum = 0  #包括连通区域的区域总数
    section = []  #将面积连续部分分为一个区间
    start = 0  #区间开始
    end = area_dic[0][1]  #区间结束
    count = 0  #区间内的连通区域数量
    maxv = 0  #所考虑的面积区间

    # 得到区间划分
    for i in range(len(area_dic)):
        if(i>0 and area_dic[i][0]!=area_dic[i-1][1]):
            section += [[start,end,count]]
            start = area_dic[i][0]
            count = 0
        count += area_dic[i][2]
        end = area_dic[i][1]
        all_sum += area_dic[i][2]
    section += [[start,end,count]]
    if(len(section)>1 and section[-1][0]>section[-2][1]*10):
        section = section[:-1]
    maxv = section[-1][1]

    for sec in section:
        if sec[2]>all_sum/5:
            start = sec[0]
            end = sec[1]
            single_area,all_area = comput_single_area(area,start,end,maxv)
            n = all_area/single_area
            print(f'器件的总数量：{int(n)}')
            break
    return section,n,start,maxv,single_area

def plot_result(section, n, start, maxv, ori_tmp, stats, labels, single_area, sign=False):
    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 0, 0), (0, 100, 0), (0, 0, 100)]
    deviation = [0.3, 0.2, 0.1, 0, -0.1, -0.2]

    new_section = []
    for sec in section:
        if sec[0] >= start and sec[1] <= maxv:
            new_section.append(sec)
    #     interval = new_section[0][0]
    interval = single_area
    # print('section:', new_section)
    # print('interval:', interval)
    new_section2 = []
    l = new_section[0][0]  # 区间开始
    r = new_section[0][1]  # 区间结束
    c = new_section[0][2]
    for i in range(1, len(new_section)):
        if new_section[i][1] - new_section[i - 1][1] >= interval or new_section[i][0] - new_section[i - 1][
            0] >= interval:
            new_section2 += [[l, r, c]]
            l = new_section[i][0]
            c = 0
        c += new_section[i][2]
        r = new_section[i][1]
    if [l, r, c] not in new_section2:
        new_section2 += [[l, r, c]]

    if (new_section2[0][1] - new_section2[0][0] > single_area * 2):
        new_single_area = single_area
    else:
        new_single_area = max(single_area, (new_section2[0][0] + new_section2[0][1]) / 2)

    index = 0
    for i, s in enumerate(stats):
        for j in range(len(new_section2)):
            if s[-1] >= start and s[-1] <= maxv and s[-1] >= new_section2[j][0] and s[-1] < new_section2[j][1]:
                ori_tmp[labels == i] = color[min(5, j)]
                index = max(index, j)

    ori_tmp = cv2.putText(ori_tmp, 'Number:', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
    for k in range(min(index + 1, 6)):
        if k == 0:
            digit = 1
        else:
            digit = int(round(new_section2[k][0] / new_single_area + deviation[k]))
        ori_tmp = cv2.putText(ori_tmp, '>=' + str(digit), (40, 140 + k * 80), cv2.FONT_HERSHEY_SIMPLEX, 1.8, color[k],
                              2, cv2.LINE_AA)
    ori_tmp = cv2.putText(ori_tmp, 'count:' + str(int(n)), (int(ori_tmp.shape[0] / 2) - 180, int(ori_tmp.shape[1] / 2)),
                          cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)

    if (sign):
        plt.figure(figsize=(12, 10))
        plt.imshow(ori_tmp)
        plt.colorbar()
    return ori_tmp