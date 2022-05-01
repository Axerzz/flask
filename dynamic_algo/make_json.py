import json

from static_algo.config_exp import config


def make_revenue_json(revenue_cs):
    csNum = config.cs_num
    w = open("D:/pycharm/python/flask/dynamic_algo/revenue.txt", "w+")
    print('Revenue,CSnum,Time', file=w)
    revenue_tmp = [0 for i in range(csNum)]
    mint = 0
    hour = 9
    for i in range(29):
        for j in range(csNum):
            for k in range(i * 60, i * 60 + 60):
                revenue_tmp[j] += revenue_cs[k][j]
            st = str('%.3f' % revenue_tmp[j]) + ',CS-' + str(j + 1) + ','
            time = "2021-09-09 "
            if hour < 10:
                time += "0" + str(hour) + ":"
            else:
                time += str(hour) + ":"
            if mint < 10:
                time += "0" + str(mint)
            else:
                time += str(mint)
            time += ":00"
            st += time
            print(st, file=w)
        mint += 5
        hour += int(mint / 60)
        mint %= 60


def make_price_json(price_time):
    print("正在make price json")
    csNum = config.cs_num
    f = open("D:/pycharm/python/flask/dynamic_algo/price.txt", "w+")
    print('Price,CSnum,Time', file=f)
    mint = 0
    hour = 9
    for i in range(29):
        for j in range(csNum):
            st = str(price_time[i][j]) + ',CS-' + str(j + 1) + ','
            time = "2021-09-09 "
            if hour < 10:
                time += "0" + str(hour) + ":"
            else:
                time += str(hour) + ":"
            if mint < 10:
                time += "0" + str(mint)
            else:
                time += str(mint)
            time += ":00"
            st += time
            print(st, file=f)
        mint += 5
        hour += int(mint / 60)
        mint %= 60

