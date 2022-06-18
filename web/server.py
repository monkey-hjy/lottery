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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/list')
def show_list():
    mysql_conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='demo'
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
            'lottery_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info[3])),
            'my_cv_id': info[4],
            'reply_date': str(info[5]),
            # 'zj_uid': info[6],
            'is_me': '中奖了!!!!!!!!' if info[7] else '否',
        }
        if int(info[3]) > int(time.time()):
            not_open_data.append(now_info)
        else:
            now_info['lottery_time'] = f'{now_info["lottery_time"]}(已开奖)'
            open_data.append(now_info)
    return render_template('list.html', open_data=open_data, not_open_data=not_open_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3999, debug=True)
