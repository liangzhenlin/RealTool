#  -*- coding: utf-8 -*-
# @Time:2022/10/23   0:39
# @Author: Lanser
# @File:yy.py
# Software:PyCharm

# 获取YY直播的真实流媒体地址。https://www.yy.com/1349606469
# 默认获取最高画质

import requests
import re
import json
import sys
# sys.path.insert(0, '..')
from .requests_code import requests_get_code
from multiprocessing.pool import ThreadPool

class YY:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        headers = {
            'referer': f'https://wap.yy.com/mobileweb/{self.rid}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.69 Safari/537.36 '
        }
        room_url = f'https://interface.yy.com/hls/new/get/{self.rid}/{self.rid}/1200?source=wapyy&callback='
        try:
            with requests.Session() as s:
                res = s.get(room_url, headers=headers, timeout=2)
        except:
            return {}
        real_lists = []
        real_list = []
        thread_list = []
        real_dict = {}
        if res.status_code == 200:
            data = json.loads(res.text[1:-1])
            if data.get('hls', 0):
                xa = data['audio']
                xv = data['video']
                xv = re.sub(r'_0_\d+_0', '_0_0_0', xv)
                url = f'https://interface.yy.com/hls/get/stream/15013/{xv}/15013/{xa}?source=h5player&type=m3u8'
                res = s.get(url).json()
                real_url = res['hls']
                real_lists.append({'hls': real_url})
        if real_lists:
            pool = ThreadPool(processes=int(len(real_lists)))
            for real_ in real_lists:
                thread_list.append(pool.apply_async(requests_get_code, args=(real_,)))
            for thread in thread_list:
                return_dict = thread.get()
                if return_dict:
                    real_list.append(return_dict)
            if real_list:
                real_list.append({'rid': self.rid})
                real_dict['yy'] = real_list
                return real_dict
        return {}


# if __name__ == '__main__':
#     r = '54880976'
#     yy = YY(r)
#
#     # r = input('输入YY直播房间号：\n')
#     print( yy.get_real_url())
