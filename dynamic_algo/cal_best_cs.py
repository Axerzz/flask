#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/3/24
# @Author : lyw
# @Version：V 0.1
# @File : cal_best_cs.py
# @desc : calculate best cs for ev

import os
import sys
import math

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from static_algo.config_exp import config

intersection_info = []

cs_info = []

EARTH_REDIUS = 6378.137

region_info = [[31.85151432, 117.1796566],
               [31.81629693, 117.1786985],
               [31.81164271, 117.1153179],
               [31.85054195, 117.1110452],
               [31.8353396, 117.1396697],
               [31.85977969, 117.1448201]
               ]


def change_dist_vector(position):
    print("position", position)
    dist_vector = []
    csNum = config.cs_num
    for i in range(csNum):
        dist = [0 for i in range(6)]
        for j in range(6):
            dist[j] = get_rightAngle_dist(region_info[j][0], region_info[j][1], position[i][1], position[i][0])
        dist_vector.append(dist)
    print(dist_vector)
    config.change_total_dist_vector(dist_vector)


def rad(d):
    return (d * math.pi) / 180.0


def getDistance(lat1, lng1, lat2, lng2):
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(
        math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    s = s * EARTH_REDIUS
    return s


def init_intersection_info():
    cs_info = config.cs_info
    print(cs_info)
    f = open("D:/pycharm/python/flask/intersection_pos.txt")
    line = f.readline()
    while line:
        line = line.strip("\n")
        intersection_info.append(line.split("\t"))
        line = f.readline()


def get_rightAngle_dist(x1, y1, x2, y2):
    dis = getDistance(x1, y1, x2, y1) + getDistance(x2, y1, x2, y2)
    dis = dis * 10
    return dis


def get_pos_from_intersection(intersection):
    latitude = 0.0
    longitude = 0.0
    for i in range(len(intersection_info)):
        if intersection_info[i][0] == intersection:
            latitude = float(intersection_info[i][1])
            longitude = float(intersection_info[i][2])
            break
    return latitude, longitude


def get_best_cs(start_road, end_road, price, cs_in_queue):
    cs_info = config.cs_info
    ll = len(start_road)
    intersection_start = "intersection" + start_road[5:ll - 3]
    ll = len(end_road)
    intersection_end = "intersection" + end_road[5:ll - 3]
    latitude, longitude = get_pos_from_intersection(intersection_start)
    latitude_end, longitude_end = get_pos_from_intersection(intersection_end)
    best_dist = 0
    minx = 1e9
    best_cs = 0
    best_dist1 = 0
    best_dist2 = 0
    csNum = config.cs_num
    for i in range(csNum):
        dist1 = get_rightAngle_dist(latitude, longitude, cs_info[i][1], cs_info[i][0])
        dist2 = get_rightAngle_dist(latitude_end, longitude_end, cs_info[i][1], cs_info[i][0])
        tmp = 0.6 * price[i] + 0.1 * cs_in_queue[i] + 0.3 * (dist1 + dist2)
        if tmp < minx:
            best_cs = i
            best_dist = dist1 + dist2
            minx = tmp
            best_dist1 = dist1
            best_dist2 = dist2
    return best_cs, best_dist, intersection_start, best_dist1, best_dist2

