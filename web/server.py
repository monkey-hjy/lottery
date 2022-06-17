# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/6/17 17:00
# Name : server.py
import configparser
import os

import pymysql
from flask import Flask, render_template
import time

config = configparser.RawConfigParser()
path = '/'.join(__file__.split('/')[:-2])
config.read(f'{path}/config.ini')
print(f'{path}/config.ini')
app = Flask(__name__, template_folder='./')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/list')
def show_list():
    mysql_conn = pymysql.Connect(
        host=config.get('mysql_info', 'host'),
        port=int(config.get('mysql_info', 'port')),
        user=config.get('mysql_info', 'user'),
        passwd=config.get('mysql_info', 'passwd'),
        db=config.get('mysql_info', 'db')
    )
    mysql_cursor = mysql_conn.cursor()
    sql = "select * from lottery order by open_time asc;"
    mysql_cursor.execute(sql)
    open_data = list()
    not_open_data = list()
    for info in mysql_cursor.fetchall():
        now_info = {
            # 'id': info[0],
            'l_id': info[1],
            'uid': info[2],
            'lottery_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info[3])),
            'my_cv_id': info[4],
            'reply_date': str(info[5]),
            'zj_uid': '',
            'is_me': '否',
        }
        if int(info[3]) > int(time.time()):
            not_open_data.append(now_info)
        else:
            now_info['lottery_time'] = f'{now_info["lottery_time"]}(已开奖)'
            open_data.append(now_info)
    return render_template('list.html', open_data=open_data, not_open_data=not_open_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3999, debug=True)
