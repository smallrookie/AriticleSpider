# -*- coding: utf-8 -*-

# 爬取伯乐在线的文章

import scrapy
import re

from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # 所需要爬取的URL
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1. 获取文章列表页中的文章url并交给scrapy下载并解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        '''

        # 解析列表页中的所有文章的url并交给scrapy下载并解析
        post_urls = response.css("#archive div.floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            # 通过调用urljoin()将response.url与post_url拼接成一个完整的域名
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        # 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # 提取文章的具体字段

        # 通过css选择器提取文章的具体字段
        # 文章标题
        title = response.css(".entry-header h1::text").extract()[0]
        # 文章发布时间
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·', '').strip()
        # 点赞数
        praise_num = response.css(".vote-post-up h10::text").extract()[0]
        # 收藏数
        fav_num = self.get_num(response.css("span.bookmark-btn::text").extract()[0])
        # 评论数
        comments_num = self.get_num(response.css("a[href='#article-comment'] span::text").extract()[0])
        # 文章内容
        content = response.css("div.entry").extract()[0]
        # 文章标签
        tags_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # 去除标签中的评论
        tags_list = [element for element in tags_list if not element.strip().endswith('评论')]
        tags = ','.join(tags_list)
        pass

    def get_num(self, value):
        # 利用正则表达式获取相应的数值

        match_re = re.match('.*(\d+).*', value)
        if match_re:
            num = int(match_re.group(1))
        else:
            num = 0
        return num
