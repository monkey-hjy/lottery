# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/6/14 18:25
# Name : main.py
from stool import *

lottery_ids = get_all_lottery()
for l_id in lottery_ids:
    l_id = str(l_id)
    comment_id, uid, lottery_time = get_user_uid(l_id)
    if comment_id is False:
        logger.error(f'get_user_uid failed l_id: {l_id}')
        REDIS_CONN.sadd('lottery_ids', l_id)
        time.sleep(10)
        continue
    logger.info(f'get_user_uid success l_id: {l_id}, comment_id: {comment_id}, uid: {uid}, lottery_time: {lottery_time}')
    comment(comment_id, l_id)
    click_like(l_id)
    my_cv_id = reply(l_id)
    follow_user(uid)
    save_sql(l_id, uid, lottery_time, my_cv_id)
    time.sleep(30)
