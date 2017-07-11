# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json

from scrapy.http import Request


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 配置user agent信息
    agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    header = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": agent,
    }

    def parse(self, response):
        pass

    def start_requests(self):
        # 通过重写start_requests()，模拟知乎登录

        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.header, callback=self.login_info)]

    def login_info(self, response):
        # 配置登录的相关信息

        # 获取用户登录信息
        account = input("请输入手机号或邮箱>")
        password = input("请输入密码>")

        # 获取xsrf
        xsrf = ""
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            # 手机号登录
            if re.match("^1\d{10}", account):
                post_data = {
                    "_xsrf": xsrf,
                    "phone_num": account,
                    "password": password,
                    "captcha": "",
                }
            else:
                # 邮箱登录
                if "@" in account:
                    post_data = {
                        "_xsrf": xsrf,
                        "email": account,
                        "password": password,
                        "captcha": "",
                    }

            # 获取验证码
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.header, meta={"post_data":post_data}, callback=self.login)

    def login(self, response):
        # scrapy模拟登录

        post_data = response.meta.get("post_data", {})
        if "phone_num" in post_data:
            post_url = "https://www.zhihu.com/login/phone_num"
        else:
            post_url = "https://www.zhihu.com/login/email"

        # 获取验证码
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()
        captcha = input("请输入验证码>")
        post_data["captcha"] = captcha

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.header,
            callback=self.isJump,
        )]

    def isJump(self, response):
        # 验证登录是否成功，并跳转至知乎首页

        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
        else:
            print("登录失败！\n")
