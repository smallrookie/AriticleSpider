# -*- coding: utf-8 -*-

# 爬取伯乐在线的文章

import scrapy
import re

from scrapy.http import Request
from urllib import parse
from AriticleSpider.items import JobBoleArticleItem
from AriticleSpider.utils.common import get_md5


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
        post_nodes = response.css("#archive div.floated-thumb .post-thumb a")
        for post_node in post_nodes:
            # 获取文章列表页中文章的封面图的url
            image_url = post_node.css("img::attr(src)").extract_first("")
            # 获取文章列表页中文章的url
            post_url = post_node.css("::attr(href)").extract_first("")
            # 通过调用urljoin()将response.url与post_url拼接成一个完整的域名
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
        # 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # 提取文章的具体字段

        # 通过css选择器提取文章的具体字段
        # 文章标题
        title = response.css(".entry-header h1::text").extract()[0]
        # 文章封面图
        front_image_url = response.meta.get("front_image_url", "")
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

        # 实例化JobBoleArticleItem
        article_item = JobBoleArticleItem()

        article_item["title"] = title
        article_item['url_object_id'] = get_md5(response.url)
        article_item["url"] = response.url
        article_item["create_date"] = create_date
        # 由于ImagesPipeline中url的值为list类型，故此需将front_image_url转为list类型
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_num"] = praise_num
        article_item["comments_num"] = comments_num
        article_item["fav_num"] = fav_num
        article_item["tags"] = tags
        article_item["content"] = content

        yield article_item

        pass


    def get_num(self, value):
        # 利用正则表达式获取相应的数值

        match_re = re.match('.*(\d+).*', value)
        if match_re:
            num = int(match_re.group(1))
        else:
            num = 0
        return num
