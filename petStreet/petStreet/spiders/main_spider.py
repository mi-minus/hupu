# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:minus 
@file: main_spider.py 
@time: 2018/05/12 
"""
import re

import scrapy
from scrapy import Selector
from bs4 import BeautifulSoup


class MainStreetSpider(scrapy.Spider):
    name = 'main'

    def __init__(self):
        self.auth_id_pa = re.compile(r'https://.*?/(\d+)$', re.S)
        self.thread_id_pa = re.compile(r'/(\d+).html$', re.S)
        self.thread_reply_pa = re.compile(r'^(\d+).*?(\d+)', re.S)
        self.thread_posttime_pa = re.compile(r'(\d{4}-\d{2}-\d{2})')

    def start_requests(self):
        """
        function: 该spider的入口函数，初始访问地址都在此初始化
        :return:
        """
        url_base = 'https://bbs.hupu.com/bxj-postdate-'
        for ind in range(10):
            url = url_base + str(ind+1)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        function: 主帖子的解析都这里定义，包括帖子的基本信息（发帖人／发帖时间／发帖地址等等）
        :param response:
        :return:
        """
        response_text = response.body
        # with open('main.txt', 'wb') as f:
        #     f.write(response_text)
        sel = Selector(text=response_text, type='html')
        bs4_content = BeautifulSoup(response.body, 'html5lib')

        threads_list = sel.xpath('//ul[@class="for-list"]/li')
        for topic in threads_list:
            soup = BeautifulSoup(topic.extract())

            # 获取 帖子id, url
            thread_url_part = soup.find_all('a', class_='truetit')[0].get('href')
            thread_id = re.findall(self.thread_id_pa, thread_url_part)[0].strip()
            print(thread_id)
            thread_url = 'https://bbs.hupu.com' + thread_url_part

            # 获取 帖子标题
            thread_title = soup.find_all('a', class_='truetit')[0].get_text().strip()
            print(thread_title)

            # 获取 帖子 作者
            thread_auth = soup.find_all('a', class_='aulink')[0].get_text().strip()
            print(thread_auth)
            thread_auth_link = soup.find_all('a', class_='aulink')[0].get('href').strip()
            # print(thread_auth_link)
            thread_auth_id = re.findall(self.auth_id_pa, thread_auth_link)[0].strip()
            print(thread_auth_id)

            # 获取 帖子 发帖时间
            thread_auth_mess = soup.find_all('div', attrs={'class': 'author box'})[0].get_text().strip()
            thread_date = re.findall(self.thread_posttime_pa, thread_auth_mess)[0].strip()
            print(thread_date)

            # 获取 帖子 回复/浏览
            thread_post_message = soup.find_all('span', class_='ansour box')[0].get_text().strip()
            thread_reply, thread_read = re.findall(self.thread_reply_pa, thread_post_message)[0]
            print(thread_reply, thread_read)
            print('+++++++++++++++')
