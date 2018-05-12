# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:minus 
@file: test.py 
@time: 2018/05/12 
"""

import requests

url = 'https://passport.hupu.com/pc/login/member.action'


headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Length': '99',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'passport.hupu.com',
    'Referer': 'https://passport.hupu.com/pc/login',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'X-Requested-With': 'XMLHttpRequest'
}
data = {
    'username': '18702978864',
    'password': '73eafdc5b5b606cf2769846bf5f666b1',
    'rid': '20180512155838be457ef96e778d0832'
}

r = requests.post(url, headers=headers, data=data)

print(r.text)

