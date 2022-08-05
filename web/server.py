# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/6/17 17:00
# Name : server.py
import configparser
import os

import pymysql
from flask import Flask, render_template
import time

app = Flask(__name__, template_folder='./')
now_file_path = __file__.split('/')
config = configparser.RawConfigParser()
config.read(f"{'/'.join(now_file_path[:-2])}/config.ini")


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
    sql = "select * from lottery where is_delete=0 order by open_time asc;"
    mysql_cursor.execute(sql)
    open_data = list()
    not_open_data = list()
    index = 0
    for info in mysql_cursor.fetchall():
        index += 1
        now_info = {
            'id': index,
            'l_id': info[1],
            'uid': info[2],
            'my_cv_id': info[3],
            'lottery_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info[4])),
            'reply_date': str(info[5]),
            # 'zj_uid': info[6],
            'is_me': '中奖了!!!!!!!!' if info[7] else '否',
        }
        if int(info[4]) > int(time.time()):
            now_info['is_me'] = '未知' if now_info['is_me'] == '否' else now_info['is_me']
            not_open_data.append(now_info)
        else:
            now_info['lottery_time'] = f'{now_info["lottery_time"]}(已开奖)'
            open_data.append(now_info)
    return render_template('list.html', open_data=open_data, not_open_data=not_open_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3999, debug=True)
