#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:   csev
@File:      config_exp.py
@Author:    bai
@Email:     wenchao.bai@qq.com
@Date:      2021/10/25 10:55
@Purpose:   a more convenience config for experiment
"""

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Config:
    """配置文件，包含相关环境数据等

    """

    def __init__(self):
        super().__init__()
        self.threshold = 0.000001  # 迭代截止阈值
        self.total_cs = 13
        self.total_regions = 13

        self.total_price = [85, 90, 80, 60, 55, 65, 68, 74, 85, 48, 58, 40, 90]
        self.total_vehicle_vector = [559, 167, 350, 346, 5, 200, 80, 60, 20, 92, 70, 130]
        # self.total_vehicle_vector = np.array([75, 153, 182, 33, 358, 208, 140, 80, 60, 20, 92, 70, 130])

        # 横坐标是CS维度，纵坐标是区域维度
        self.total_dist_vector = [[14.6514, 43.4912, 85.8734, 66.0878, 50.4677, 36.9472],
                                           [71.0449, 98.1383, 47.689, 9.68888, 40.0168, 38.0073],
                                           [75.8642, 57.7501, 24.645, 37.8972, 10.7528, 42.8276],
                                           [114.517, 65.1346, 14.0155, 40.8803, 49.4096, 81.4797],
                                           [46.9808, 7.71284, 53.5447, 87.9221, 50.3968, 72.7247]]

        self.cs_info = [[31.851441415, 117.1740803],
           [31.85064675, 117.1153743],
           [31.83534871, 117.1341873],
           [31.81164271, 117.1153179],
           [31.82085063, 117.1759037]]
        self.cs_cap_vector = [10, 4, 4, 5, 6, 8, 12, 8, 6, 6, 6, 4, 12]
        self.w_p, self.w_qf, self.w_d = 0.7, 0.1, 0.2
        self.P_MIN, self.P_MAX = 40, 90

        self.region_num = 6  # 下层区域的数量6
        self.cs_num = 5  # 充电站的数量5
        self.cost = [65, 60, 25, 15, 20, 15, 24, 36, 27, 13, 22, 28, 25]  # 运营成本

        # 根据充电站数量和研究区域的数量截取相关环境数据
        self.price = self.total_price[:self.cs_num]
        self.cs_cap = self.cs_cap_vector[:self.cs_num]
        self.vehicle_vector = self.total_vehicle_vector[:self.region_num]
        self.dist_vector = self.total_dist_vector

    def change_total_dist_vector(self, dist_vector):
        self.total_dist_vector = dist_vector

    def change_region_num(self, change_num):
        self.region_num = change_num

    def change_cs_info(self, cs_info):
        self.cs_info = cs_info

    def change_cost(self, cost):
        self.cost = cost

    def change_cs_cap_vector(self, cs_cap_vector):
        self.cs_cap_vector = cs_cap_vector

    def change_cs_num(self, change_num):
        self.cs_num = change_num

    def change_region_cs_num(self, region_num, cs_num):
        self.region_num = region_num
        self.cs_num = cs_num
        self.price = self.total_price[:self.cs_num]
        self.vehicle_vector = self.total_vehicle_vector[:self.region_num]
        self.cs_cap = self.cs_cap_vector[:self.cs_num]


config = Config()


# 1	31.851441	117.174081	10	20773.963
# 2	31.850647	117.115370	4	17000.181
# 3	31.835349	117.134187	4	25875.224
# 4	31.811643	117.115318	5	13612.031
# 5	31.820851	117.175904	6	13045.198
