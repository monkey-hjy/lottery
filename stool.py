# -*- coding: utf-8 -*-
# User : HJY
# Date : 2022/6/14 18:26
# Name : stool.py

"""放置功能代码"""
import random
import re
import time

import pymysql
import redis
import requests
from loguru import logger
import configparser

logger.add('lottery_o.loc', mode='a')
config = configparser.RawConfigParser()
config.read('config.ini')

COOKIE = config.get('cookie', 'cookie')
CSRF = re.findall('bili_jct=(.*?);', COOKIE)[0]
HEADERS = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': COOKIE,
    'origin': 'https://space.bilibili.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
}
BRIEF_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}
KEYWORDS = config.get('keywords', 'keywords').split(',')
REDIS_CONFIG = config['redis']
REDIS_CONN = redis.StrictRedis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], password=REDIS_CONFIG['password'], db=REDIS_CONFIG['db'])


def get_response(url, method='get', data=None, params=None, headers=None):
    """
    获取响应
    :param url: 请求地址
    :param method: 请求方式
    :param data: 请求数据
    :param params: 请求参数
    :param headers: 请求头
    """
    err_count = 0
    while err_count < 5:
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, data=data, params=params, timeout=30)
            else:
                logger.error(f'请求参数错误 method: {method}')
                return None
            if response.status_code == 200:
                return response
            else:
                raise Exception(response.status_code)
        except Exception as e:
            err_count += 1
            logger.error(f'requests err {err_count}, e: {e.args[0]}')


def get_all_lottery():
    """
    获取所有抽奖ID
    """
    url = 'https://api.bilibili.com/x/web-interface/search/type?__refresh__=true&_extra=&context=&page=1&page_size=50&order=totalrank&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=%E4%BA%92%E5%8A%A8%E6%8A%BD%E5%A5%96&category_id=0&search_type=article&preload=true&com2co=true'
    response = get_response(url, method='get', headers=BRIEF_HEADERS)
    if response is None:
        return False
    response = response.json()['data']['result']
    # response = requests.get(url, headers=HEADERS).json()['data']['result']
    ids = [info['id'] for info in response]
    lottery_ids = list()
    for cv_id in ids[:2]:
        url = 'https://www.bilibili.com/read/cv{}'.format(cv_id)
        try:
            response = get_response(url, method='get', headers=BRIEF_HEADERS)
            if response is None:
                continue
            # response = requests.get(url, headers=BRIEF_HEADERS, timeout=15)
            now_ids = re.findall('href="https://t\.bilibili\.com/(.*?)\?', response.text)
            for l_id in now_ids:
                if REDIS_CONN.sismember('lottery_ids', l_id):
                    continue
                lottery_ids.append(l_id)
            logger.info(f'{url}, {len(lottery_ids)}')
        except Exception as e:
            logger.error(f'{url}, {e.args[0]}')
    logger.info(f'res: {len(set(lottery_ids))}')
    return list(set(lottery_ids))


def is_official(l_id):
    """
    判断是否使用官方抽奖工具
    :param l_id: 抽奖动态ID
    :return: True/False
    """
    url = f'https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice?dynamic_id={l_id}'
    response = get_response(url, method='get', headers=BRIEF_HEADERS)
    if response is None:
        return False
    response = response.json()
    # response = requests.get(url, headers=BRIEF_HEADERS, timeout=15).json()
    if response['code'] != 0:
        return False
    if response['data']['lottery_time'] <= int(time.time()):
        return False
    return response['data']['lottery_time']


def get_user_uid(l_id):
    """
    根据抽奖动态获取到用户ID
    :param l_id: 抽奖动态ID
    :return: 用户ID
    """
    open_time = is_official(l_id)
    if open_time is False:
        return False, False, False
    url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id={l_id}'
    response = get_response(url, method='get', headers=BRIEF_HEADERS)
    if response is None:
        return False, False, False
    response = response.json()
    # response = requests.get(url, headers=BRIEF_HEADERS).json()
    comment_id = response['data']['item']['basic']['comment_id_str']
    uid = response['data']['item']['modules']['module_author']['mid']
    return comment_id, uid, open_time


def reply(l_id):
    """
    转发动态
    :param l_id: 抽奖动态ID
    """
    url = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/reply'
    data = {
        'uid': '7281407',
        'type': '1',
        'rid': l_id,
        'content': random.choice(KEYWORDS),
        'repost_code': '30000',
        'from': 'create.comment',
        'extension': '{"emoji_type":1}',
    }
    response = get_response(url, method='post', data=data, headers=HEADERS)
    if response is None:
        return False
    response = response.json()
    # response = requests.post(url, headers=HEADERS, data=data).json()
    if response['code'] == 0:
        logger.info(f'reply success l_id: {l_id}, res: {response}')
        if 'dynamic_id_str' in response['data']:
            return response['data']['dynamic_id_str']
        else:
            return response['data']['dynamic_id']
    else:
        logger.error(f'reply failed l_id: {l_id}, res: {response}')
        return False


def comment(comment_id, l_id):
    """
    评论
    :param comment_id: 评论ID
    :param l_id: 动态ID
    :return:
    """
    url = 'https://api.bilibili.com/x/v2/reply/add'
    data = {
        'oid': comment_id,
        'type': 17 if comment_id == l_id else 11,
        'message': random.choice(KEYWORDS),
        'plat': '1',
        'ordering': 'heat',
        'jsonp': 'jsonp',
        'csrf': CSRF
    }
    response = get_response(url, method='post', data=data, headers=HEADERS)
    if response is None:
        return False
    # response = requests.post(url, headers=HEADERS, data=data)
    res = response.json()['code']
    if res != 0:
        res = response.json()
        logger.error(f'comment error l_id: {l_id}, res: {res}, data: {data}')
    else:
        logger.info(f'comment success l_id: {l_id}')


def follow_user(uid):
    """
    关注用户
    :param uid: 用户ID
    """
    url = 'https://api.bilibili.com/x/relation/modify'
    data = {
        'fid': uid,
        'act': '1',
        're_src': '11',
        'spmid': '333.999.0.0',
        'extend_content': '{"entity":"user","entity_id":' + str(uid) + ',"fp":"0\u0001900,,1440\u0001MacIntel\u00018\u00018\u000130\u00011\u0001zh-CN\u00011\u00010,,0,,0\u0001Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"}',
        'jsonp': 'jsonp',
        'csrf': CSRF,
    }
    response = get_response(url, method='post', data=data, headers=HEADERS)
    # response = requests.post(url, headers=HEADERS, data=data)
    logger.info(f'follow success uid: {uid}, res: {response.text}')


def click_like(l_id):
    """
    点赞
    :param l_id: 动态ID
    """
    url = 'https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/thumb'
    data = {
        'dynamic_id': l_id,
        'up': '1',
        'csrf': CSRF,
    }
    response = get_response(url, method='post', data=data, headers=HEADERS)
    # response = requests.post(url, headers=HEADERS, data=data)
    logger.info(f'like success l_id: {l_id}, res: {response.text}')


def save_sql(l_id, uid, open_time, my_cv_id):
    """
    保存数据到数据库
    :param l_id: 抽奖动态ID
    :param uid: 用户ID
    :param open_time: 开奖时间
    :param my_cv_id: 转发的动态ID
    """
    mysql_conn = pymysql.Connect(
        host=config.get('mysql_info', 'host'),
        port=int(config.get('mysql_info', 'port')),
        user=config.get('mysql_info', 'user'),
        passwd=config.get('mysql_info', 'passwd'),
        db=config.get('mysql_info', 'db')
    )
    mysql_cursor = mysql_conn.cursor()
    sql = f"insert into lottery_o (l_id, uid, open_time, my_cv_id) VALUES ('{l_id}', '{uid}', {open_time}, '{my_cv_id}');"
    mysql_cursor.execute(sql)
    mysql_conn.commit()
    mysql_cursor.close()
    mysql_conn.close()
    REDIS_CONN.sadd('lottery_id', l_id)
    logger.info(f'save success l_id: {l_id}, uid: {uid}, open_time: {open_time}, my_cv_id: {my_cv_id}')
    logger.info('-'*50)
