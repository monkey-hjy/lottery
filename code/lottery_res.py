# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/8/5 16:35
# Name : lottery_res.py

from stool import Stool
import configparser
import pymysql


now_file_path = __file__.split('/')
config = configparser.RawConfigParser()
config.read(f"{'/'.join(now_file_path[:-2])}/config.ini")
mysql_conn = pymysql.Connect(
    host=config.get('mysql_info', 'host'),
    port=int(config.get('mysql_info', 'port')),
    user=config.get('mysql_info', 'user'),
    passwd=config.get('mysql_info', 'passwd'),
    db=config.get('mysql_info', 'db')
)
mysql_cursor = mysql_conn.cursor()
sql = "select * from user;"
mysql_cursor.execute(sql)
user_res = mysql_cursor.fetchall()
for info in user_res:
    info = {
        'uid': info[1],
        'cookie': info[2],
        'name': info[3]
    }
    Stool(user_info=info).search_lottery_info()

