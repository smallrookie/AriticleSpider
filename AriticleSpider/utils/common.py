# coding=utf-8

import hashlib

# md5函数
def get_md5(url):
    # 若url为Unicode，则将其转为utf-8
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# 测试MD5函数
if __name__ == '__main__':
    print(get_md5("http://jobbole.com".encode("utf-8")))