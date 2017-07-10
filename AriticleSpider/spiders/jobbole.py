# -*- coding: utf-8 -*-

# 爬取伯乐在线的文章

import scrapy
import re

from scrapy.http import Request
from urllib import parse
from AriticleSpider.items import JobBoleArticleItem, ArticleItemLoader
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

        # 文章封面图
        front_image_url = response.meta.get("front_image_url", "")

        # 通过自定义的item loader机制加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # 文章标题
        item_loader.add_css("title", ".entry-header h1::text")
        # 文章详情页URL
        item_loader.add_value("url", response.url)
        # 文章详情页URL的MD5
        item_loader.add_value("url_object_id", get_md5(response.url))
        # 文章发布时间
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        # 文章封面图URL，由于
        item_loader.add_value("front_image_url", front_image_url)
        # 点赞数
        item_loader.add_css("praise_num", ".vote-post-up h10::text")
        # 评论数
        item_loader.add_css("comments_num", "a[href='#article-comment'] span::text")
        # 收藏数
        item_loader.add_css("fav_num", ".bookmark-btn::text")
        # 文章标签
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        # 文章内容
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item
