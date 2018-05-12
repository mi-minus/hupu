# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:minus 
@file: main_spider.py 
@time: 2018/05/12 
"""
import re

import math
import scrapy
import time
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
        for ind in range(1):
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
            yield scrapy.Request(url=thread_url, callback=self.parse_thread, meta={"reply_num": thread_reply})
            print('+++++++++++++++')

    def parse_thread(self, response):
        """
        function: 进入到帖子详情页面，进行解析回复帖子
        :param response:
        :return:
        """
        # 计算回复总页数
        reply_num = response.meta["reply_num"]
        print(reply_num)
        page_num = math.ceil(reply_num/20.0)

        # 对response进行格式化，对象化
        sel = Selector(text=response.body, type='html')
        bs4_content = BeautifulSoup(response.body, 'html5lib')

        reply_list = sel.xpath('//form[@name="delatc"]/div[@class="floor"]')
        print(len(reply_list))

        # 该页是否有<下一页>的按钮，通过总条数和一页20条进行计算共多少页

        # try:
        #     next_page = bs4_content.find("a", class_="nextPage").get("href").strip()
        #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #     print("next_page:" + next_page)
        #     with open("~/page.txt", "a+") as f:
        #         f.write(next_page)
        # except(AttributeError):
        #     next_page = None

        for ind, reply in enumerate(reply_list):
            soup = BeautifulSoup(reply.extract())
            ''' 楼主帖子 注意:需要获取并保存图片'''
            if ind == 0:
                # 楼主主页地址
                main_post = soup.find_all("div", attrs={"id":"tpc"})[0]
                auth_main_url = main_post.find_all("a", class_="headpic")[0].get("href")
                print(auth_main_url)

                # 楼主头像地址
                auth_main_pic_url = main_post.find_all("a", class_="headpic")[0].find("img").get("src")
                print(auth_main_pic_url)

                # 楼主级数
                level_msg = soup.find_all("span", class_="f666")[0].get_text().strip()
                print(level_msg)

                # 楼主发帖时间
                post_time = soup.find_all("span", class_="stime")[0].get_text().strip()
                print(post_time)

                # 楼主帖子的 子标题
                sub_title = soup.find_all("div", class_="subhead")[0].get_text().strip()
                print(sub_title)

                # 楼主帖子的 帖子正文
                content = soup.find_all("div", class_="quote-content")[0].get_text().strip()
                print(content)

                # 楼主帖子的发布来源
                try:
                    origin = soup.find_all("small", class_="f999")[0].get_text().strip()
                    print(origin)
                except(IndexError):
                    origin = None

                ''' 其他回复贴'''
            else:
                # 回帖人主页地址
                replyer_main_url = soup.find_all("a", class_="headpic")[0].get("href")
                print(replyer_main_url)

                # 回帖人头像地址
                replyer_main_img_url = soup.find_all("a", class_="headpic")[0].find("img").get("src")
                print(replyer_main_img_url)

                # 回帖人昵称
                replyer_name = soup.find("div", class_="left").find("a", class_="u").get_text().strip()
                print("reply_name:" + replyer_name)

                # 回帖人级别
                replyer_level = soup.find("span", class_="f666").get_text().strip()
                print(replyer_level)

                # 回帖人回帖时间
                replyer_time = soup.find("span", class_="stime").get_text().strip()
                print(replyer_time)

                # 回帖人的点亮数
                replyer_highlight_num = soup.find("span", class_="ilike_icon_list").get_text().strip()
                print(replyer_highlight_num)

                # 回帖人所处的层数
                replyer_floor_num = soup.find("a", class_="floornum").get_text().strip()
                print(replyer_floor_num)

                # 回帖人的发布来源
                try:
                    origin = soup.find("small", class_="f999").get_text().strip()
                    print(origin)
                except(AttributeError, IndexError):
                    origin = None

                # 回帖人引用内容(判断是否有)
                try:
                    quote_content = soup.find("table", class_="case").find("blockquote").get_text().strip()
                    print(quote_content)
                except(IndexError, AttributeError):
                    quote_content = None
                    reply_content = soup.find("table", class_="case").get_text().strip()
                    print(reply_content)




