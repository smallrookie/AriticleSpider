# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json
import datetime

from scrapy.http import Request
from scrapy.loader import ItemLoader
from AriticleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem

try:
    # 若开发环境为Python 2.X
    import urlparse as parse
except:
    # 若开发环境为Python 3.X
    from urllib import parse


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # question的第一页answer的URL请求
    start_answer_urls = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    # 配置user agent信息
    agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    header = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": agent,
    }

    custom_settings = {
        # 启用cookies
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        '''
        提取HTML页面中的所有URL，并跟踪这些URL进行进一步爬取
        如果提取的URL中格式为 /question/xxx 就下载之后直接进入解析函数
        '''
        all_urls = response.css("a::attr(href)").extract()
        # 将获取的url与知乎主域名拼接成完整的url链接
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 将https开始的url保存至all_urls列表中，过滤其他url
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 若提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                question_id = int(match_obj.group(2))

                yield scrapy.Request(request_url, headers=self.header, meta={"zhihu_id": question_id},
                                     callback=self.parse_question)
            else:
                # 若所提取的URL不为question相关页面，则进一步跟踪提取
                yield scrapy.Request(url, headers=self.header, callback=self.parse)

    def parse_question(self, response):
        # 处理question页面，从页面中提取具体的question item

        zhihu_id = response.meta.get("zhihu_id", "")

        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)

        item_loader.add_css("title", "h1.QuestionHeader-title::text")
        item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
        item_loader.add_css("content", ".QuestionHeader-detail")
        item_loader.add_value("url", response.url)
        item_loader.add_value("zhihu_id", zhihu_id)
        item_loader.add_css("answer_num", ".List-headerText span::text")
        item_loader.add_css("comments_num", ".QuestionHeaderActions button::text")
        item_loader.add_css("watch_user_num", ".NumberBoard-value::text")

        question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_urls.format(zhihu_id, 20, 0), headers=self.header,
                             callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        # 处理answer页面，从页面中提取具体的answer item

        answer_json = json.loads(response.text)
        # 判断能否继续请求后续answer页面
        is_end = answer_json["paging"]["is_end"]
        # 问题回答的总数
        totals_answer = answer_json["paging"]["totals"]
        # 下一个answer页面URL
        next_url = answer_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in answer_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            # 知乎匿名用户回答则无id
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.header, callback=self.parse_answer)

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
            cookies = {}

            yield scrapy.Request(captcha_url, headers=self.header, meta={"post_data": post_data}, callback=self.login)

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
                # 此处未调用callback函数，将默认回调parse()
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
        else:
            print("登录失败！\n")
