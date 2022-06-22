# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/6/14 18:25
# Name : main.py
from stool import *

while True:
    lottery_ids = get_all_lottery()
    for l_id in lottery_ids:
        l_id = str(l_id)
        comment_id, uid, lottery_time = get_user_uid(l_id)
        if not comment_id:
            logger.error(f'get_user_uid failed l_id: {l_id}')
            REDIS_CONN.sadd('lottery_ids', l_id)
            time.sleep(10)
            continue
        logger.info(f'get_user_uid success l_id: {l_id}, comment_id: {comment_id}, uid: {uid}, lottery_time: {lottery_time}')
        res = comment(comment_id, l_id)
        if not res:
            continue
        click_like(l_id)
        my_cv_id = reply(l_id)
        if not my_cv_id:
            continue
        follow_user(uid)
        save_sql(l_id, uid, lottery_time, my_cv_id)
        time.sleep(30)
    search_lottery_info()
    delete_expired_info()
    time.sleep(600)
