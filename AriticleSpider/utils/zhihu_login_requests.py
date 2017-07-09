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
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

# 配置user agent信息
agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent,
}


def get_xsrf():
    # 获取xsrf

    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


def get_captcha():
    # 获取验证码

    t = str(int(time.time() * 1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    r = session.get(captcha_url, headers=header)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input(u"输入验证码\n>")
    return captcha


def zhihu_login(account, password):
    # 知乎登录

    # 手机号码登录
    if re.match("^1\d{10}", account):
        post_url = "https://www.zhihu.com/login/phone_num"
        captcha = get_captcha()
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": captcha,
        }
        response_text = session.post(post_url, data=post_data, headers=header)

        session.cookies.save()

zhihu_login("xxxx", "xxxx")
