import MySQLdb
import requests


class GetIP(object):
    # 从MySQL数据库中取出代理ip

    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="article_spider", charset="utf8")
    cursor = conn.cursor()

    def delete_ip(self, ip):
        # 删除MySQL数据库中无效的代理ip
        sql = """delete from proxy_ip where ip={0}""".format(ip)
        self.cursor.execute(sql)
        self.conn.commit()
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
                print("invaild ip and port!\n")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从MySQL数据库中随机获取一个代理ip

        sql = """SELECT ip, port from proxy_ip ORDER BY RAND() LIMIT 1"""
        result = self.cursor.execute(sql)

        for ip_info in self.cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judege_re = self.judge_ip(ip, port)
            if judege_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    get_ip = GetIP()
    get_ip.get_random_ip()
