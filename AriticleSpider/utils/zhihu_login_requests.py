# 模拟知乎登录

import requests

try:
    # 若开发环境为Python 2.X
    import cookielib
except:
    # 若开发环境为Python 3.X
    import http.cookiejar as cookielib

import re
import time
import os

from PIL import Image

session = requests.session()
# 配置cookies保存路径
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

# 导入已存储的cookies
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookies未能加载")

# 配置user agent信息
agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent,
}


def is_login():
    # 通过个人中心页面返回的状态码判断是否登录

    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)

    if response.status_code != 200:
        return zhihu_login()
    else:
        return get_index()


def get_index():
    # 获取知乎首页，若登录成功，则将知乎首页数据写入自定义的html文件

    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
        f.close()


def get_xsrf():
    # 获取xsrf

    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    try:
        if match_obj:
            return (match_obj.group(1))
    except:
        print("获取xsrf失败！\n")


def get_captcha():
    # 获取验证码

    t = str(int(time.time() * 1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    r = session.get(captcha_url, headers=header)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    captcha = input(u"输入验证码>")
    return captcha


def zhihu_login():
    # 知乎登录

    account = input(u"输入手机号或邮箱>")
    password = input(u"输入密码>")

    # 手机号码登录
    if re.match("^1\d{10}", account):
        post_url = "https://www.zhihu.com/login/phone_num"
        # 请求获取验证码
        captcha = get_captcha()
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": captcha,
        }
    # 邮箱登录
    else:
        if "@" in account:
            post_url = "https://www.zhihu.com/login/phone_num"
            # 请求获取验证码
            captcha = get_captcha()
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                "captcha": captcha,
            }
    response_text = session.post(post_url, data=post_data, headers=header)
    # 将cookies保存至本地
    session.cookies.save()
    get_index()


if __name__ == "__main__":
    is_login()
