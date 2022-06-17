# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/6/17 18:23
# Name : select_lottery_info.py
# 查询中奖信息
import time

import pymysql
import redis
import requests
from loguru import logger
import configparser

BRIEF_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}

mysql_conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='demo'
)
mysql_cursor = mysql_conn.cursor()
sql = "select * from lottery where win_uid is null;"
mysql_cursor.execute(sql)
data = mysql_cursor.fetchall()
for info in data:
    if int(info[3]) <= int(time.time()):
        url = f'https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice?dynamic_id={info[1]}'
        win_uid = list()
        win_name = list()
        response = requests.get(url, headers=BRIEF_HEADERS, timeout=30).json()
        if response['code'] == 0:
            response = response['data']['lottery_result']
            for key in response:
                for now_win_info in response[key]:
                    win_uid.append(str(now_win_info['uid']))
                    win_name.append(now_win_info['name'])
        if win_uid:
            is_me = 0
            win_uid = ','.join(win_uid)
            if '347405521' in win_uid:
                is_me = 1
            if 'Monkey-_-' in win_name:
                is_me = 1
            sql = f"update lottery set win_uid='{win_uid}', me_win={is_me} where id={info[0]};"
            mysql_cursor.execute(sql)
            mysql_conn.commit()
