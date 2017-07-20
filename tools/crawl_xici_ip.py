import requests
import MySQLdb

from scrapy.selector import Selector

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="article_spider", charset="utf8")
cursor = conn.cursor()

def crawl_ip():
    # 爬取西刺网的免费ip代理

    # 配置header
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    # 通过遍历爬取西刺网的url
    for i in range(2231):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

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

class GetIP(object):
    # 从MySQL数据库中取出代理ip

    def delete_ip(self, ip):
        # 删除MySQL数据库中无效的代理ip

        sql = """delete from proxy_ip where ip={0}""".format(ip)
        cursor.execute(sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断代理ip是否可用

        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "https": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
            return True
        except Exception as e:
            print("invaild ip and port!\n")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                return True
            else:
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从MySQL数据库中随机获取一个代理ip

        sql = """SELECT ip, port from proxy_ip ORDER BY RAND() LIMIT 1"""
        result = cursor.execute(sql)

        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judege_re = self.judge_ip(ip, port)
            if judege_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()

if __name__ == "__main__":
    # crawl_ip()

    get_ip = GetIP()
    get_ip.get_random_ip()