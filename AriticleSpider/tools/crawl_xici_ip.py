import requests
import MySQLdb

from scrapy.selector import Selector


def crawl_ip():
    # 爬取西刺网的免费ip代理

    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="article_spider", charset="utf8")
    cursor = conn.cursor()

    # 清空MySQL数据库中的数据
    sql = "delete from proxy_ip"
    cursor.execute(sql)
    conn.commit()

    # 配置header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    # 通过遍历爬取西刺网的url
    re = requests.get("http://www.xicidaili.com/nn/1", headers=headers)

    ip_list = []

    selector = Selector(text=re.text)
    all_trs = selector.css("#ip_list tr")
    for tr in all_trs[1:]:
        speed_str = tr.css(".bar::attr(title)").extract()[0]
        if speed_str:
            speed = float(speed_str.split("秒")[0])
        all_texts = tr.css("td::text").extract()
        ip = all_texts[0]
        port = all_texts[1]
        proxy_type = all_texts[5]

        if proxy_type == "HTTP":
            ip_list.append((ip, port, speed, proxy_type))

    # 将所爬取的代理ip存储至MySQL数据库
    for ip_info in ip_list:
        cursor.execute(
            "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, '{3}')"
                .format(ip_info[0], ip_info[1], ip_info[2], ip_info[3])
        )
        conn.commit()


if __name__ == "__main__":
    crawl_ip()
