# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/6/14 18:25
# Name : main.py
from stool import Stool
import configparser
import pymysql
import time
from loguru import logger


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
lottery_ids = None
for info in user_res:
    info = {
        'uid': info[1],
        'cookie': info[2],
        'name': info[3]
    }
    st = Stool(user_info=info)
    if lottery_ids is None:
        lottery_ids = st.get_all_lottery()
    for l_id in lottery_ids:
        l_id = str(l_id)
        comment_id, uid, lottery_time = st.get_user_uid(l_id)
        if not comment_id:
            logger.error(f'get_user_uid failed l_id: {l_id}')
            st.REDIS_CONN.sadd('lottery_ids', l_id)
            time.sleep(10)
            continue
        logger.info(f'get_user_uid success l_id: {l_id}, comment_id: {comment_id}, uid: {uid}, lottery_time: {lottery_time}')
        res = st.comment(comment_id, l_id)
        if not res:
            continue
        st.click_like(l_id)
        my_cv_id = st.reply(l_id)
        if not my_cv_id:
            continue
        st.follow_user(uid)
        st.save_sql(l_id, uid, lottery_time, my_cv_id)
        time.sleep(30)
    st.search_lottery_info()
    st.delete_expired_info()
    logger.info(f'{info} 处理结束')
