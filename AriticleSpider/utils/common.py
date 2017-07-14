# coding=utf-8

import hashlib
import re


# md5函数
def get_md5(url):
    # 若url为Unicode，则将其转为utf-8
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(value):
    # 利用正则表达式获取相应的数值

    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num


# 测试MD5函数
if __name__ == '__main__':
    print(get_md5("http://jobbole.com".encode("utf-8")))
