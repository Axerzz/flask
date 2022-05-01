from flask import Flask
from flask_cors import *
import pymysql
import json

from dynamic_algo.Dynamic_simulation import *
from static_algo.config_exp import config

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='lyw.0824', port=3306, db='springboot', charset='utf8')

app = Flask(__name__)

CORS(app, resources=r'/*')

from flask import Flask, request, jsonify


@app.route('/get_revenue', methods=['POST'])
def get_revenue():
    f = open("D:/pycharm/python/flask/dynamic_algo/revenue.txt", "r")
    data = []
    line = f.readline()
    line = line.strip("\n")
    tmp = line.split(',')
    data.append(tmp)
    line = f.readline()
    line = line.strip("\n")
    while line != '':
        tmp = line.split(',')
        tmp[0] = float(tmp[0])
        data.append(tmp)
        line = f.readline()
        line = line.strip("\n")
    print(data)
    f.close()
    back = {'msg': 'success',
            'json': data}
    return jsonify(back)


@app.route('/get_price', methods=['POST'])
def get_price():
    f = open("D:/pycharm/python/flask/dynamic_algo/price.txt", "r")
    data = []
    line = f.readline()
    line = line.strip("\n")
    tmp = line.split(',')
    data.append(tmp)
    line = f.readline()
    line = line.strip("\n")
    while line != '':
        tmp = line.split(',')
        tmp[0] = float(tmp[0])
        data.append(tmp)
        line = f.readline()
        line = line.strip("\n")
    print(data)
    f.close()
    back = {'msg': 'success',
            'json': data}
    return jsonify(back)


@app.route('/calculate', methods=['POST'])
def calculate_revenue():
    data = request.get_data()
    data = json.loads(data)
    param = data.get('params')
    csNum = param.get('csNum')
    position = param.get('position')
    capacity = param.get('capacity')
    cost = param.get('cost')
    print("csNum:", csNum)
    print("position:", position)
    print("capacity:", capacity)
    print("cost:", cost)
    config.change_cs_num(csNum)
    config.change_cs_info(cs_info=position)
    config.change_cs_cap_vector(cs_cap_vector=capacity)
    config.change_cost(cost)
    change_dist_vector(position)
    revenue = evcs_dynamic(6, csNum)
    total_revenue = 0
    for i in range(csNum):
        total_revenue += revenue[i]
    cur = conn.cursor()  # 生成游标对象
    sql = "delete from csinfo"
    cur.execute(sql)  # 执行SQL语句
    cur.connection.commit()
    for i in range(csNum):
        sql = "insert into csinfo values(%d,%f,%f,%d,%f,%d)" % (i+1,position[i][1],position[i][0],capacity[i],revenue[i],cost[i])
        cur.execute(sql)
        cur.connection.commit()
    cur.close()
    back = {'msg': 'success',
            'revenue': revenue,
            'total_revenue': '%.3f' % total_revenue}
    return jsonify(back)


@app.route('/get_all_cs', methods=['POST'])
def get_all_cs():
    cur = conn.cursor()  # 生成游标对象
    sql = "select * from `csinfo`"
    cur.execute(sql)
    row = cur.fetchone()
    cap = []
    lat = []
    lng = []
    cost = []

    l = 0
    revenue = 0
    while row is not None:
        l = l + 1
        lat.append(row[1])
        lng.append(row[2])
        cap.append(row[3])
        revenue += row[4]
        cost.append(row[5])
        row = cur.fetchone()
    cur.close()
    print(cap, lat, lng, cost)
    back = {'msg': 'success',
            'lat': lat,
            'lng': lng,
            'capacity': cap,
            'length': l,
            'revenue': '%.3f' % revenue,
            'cost': cost}
    return jsonify(back)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    data = request.get_data()
    data = json.loads(data)
    print("data:", data)
    username = data.get('username')
    mobile = data.get('mobile')
    email = data.get('email')
    carnum = data.get('carnum')
    age = int(data.get('age'))
    lat = float(data.get('lat'))
    lng = float(data.get('lng'))
    print(mobile, email, lat, lng, carnum, age, username)
    cur = conn.cursor()  # 生成游标对象
    sql = "update profile set mobile='{}',email='{}',lat='{}',lng='{}',carnum='{}',age='{}'" \
          " where username='{}'".format(mobile, email, lat, lng, carnum, age, username)
    cur.execute(sql)  # 执行SQL语句
    cur.connection.commit()
    back = {'msg': 'success'}
    cur.close()  # 关闭游标
    return jsonify(back)


@app.route('/profile/select', methods=['POST', 'GET'])
def select_profile():
    if request.method == 'GET':
        username = request.args.get('username')
        print(username)
        cur = conn.cursor()  # 生成游标对象
        sql = "select * from `profile` where username = '%s'" % (username)
        cur.execute(sql)  # 执行SQL语句
        row = cur.fetchone()
        print(row)
        data = {'msg': 'success',
                'username': row[0],
                'mobile': row[1],
                'email': row[2],
                'lat': row[3],
                'lng': row[4],
                'carnum': row[5],
                'age': row[6],
                'role': row[7]}
        cur.close()  # 关闭游标
        return jsonify(data)


@app.route('/profile', methods=['POST', 'GET'])
def init_profile():
    if request.method == 'GET':
        username = request.args.get('username')
        role = int(request.args.get('role'))
        print(username, role)
        cur = conn.cursor()  # 生成游标对象
        sql = "insert into profile values('%s','%s','%s',%f,%f,'%s',%d,%d)" % (username, '', '', 0.0, 0.0, '', 0, role)
        cur.execute(sql)  # 执行SQL语句
        cur.connection.commit()
        data = {'msg': 'success'}
        cur.close()  # 关闭游标
        return jsonify(data)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        role = int(request.args.get('role'))
        print(username, password, role)
        cur = conn.cursor()  # 生成游标对象
        sql = "select * from `user` where username = '%s'" % (username)
        cur.execute(sql)  # 执行SQL语句
        row = cur.fetchone()
        if row is not None:
            data = {'msg': 'failed'}
            cur.close()  # 关闭游标
            return jsonify(data)
        else:
            sql = "insert into user values('%s','%s',%d)" % (username, password, role)
            cur.execute(sql)  # 执行SQL语句
            cur.connection.commit()
            data = {'msg': 'success'}
            cur.close()  # 关闭游标
            return jsonify(data)


@app.route('/register/find', methods=['POST', 'GET'])
def register_find():
    if request.method == 'GET':
        username = request.args.get('username')
        cur = conn.cursor()  # 生成游标对象
        sql = "select * from `user` where username = '%s'" % (username)
        cur.execute(sql)  # 执行SQL语句
        row = cur.fetchone()
        if row is not None:
            data = {'msg': 'failed'}
            cur.close()  # 关闭游标
            return jsonify(data)
        else:
            data = {'msg': 'success'}
            cur.close()  # 关闭游标
            return jsonify(data)


@app.route('/login', methods=['POST', 'GET'])
def login_in():
    if request.method == 'GET':
        name = request.args.get('username')
        pwd = request.args.get('password')
        cur = conn.cursor()  # 生成游标对象
        sql = "select * from `user` where username = '%s' and password='%s'" % (name, pwd)  # SQL语句
        cur.execute(sql)  # 执行SQL语句
        row = cur.fetchone()
        fail_data = {'msg': 'failed'}
        if row is not None:
            succ_data = {'msg': 'success',
                         'role': row[2]}
            cur.close()  # 关闭游标
            return jsonify(succ_data)
        else:
            cur.close()  # 关闭游标
            return jsonify(fail_data)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
