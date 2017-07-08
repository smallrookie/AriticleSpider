# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AriticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleItem(scrapy.Item):
    # 自定义item，用于数据的存储

    # 文章标题
    title = scrapy.Field()
    # 文章发布时间
    create_date = scrapy.Field()
    # 当前文章URL
    url = scrapy.Field()
    # 文章URLmd5，由于URL长度可变，故采用MD5将其长度固定，便于存取
    url_object_id = scrapy.Field()
    # 文章封面图
    front_image_url = scrapy.Field()
    # 文章封面图存储路径
    front_image_path = scrapy.Field()
    # 点赞数
    praise_num = scrapy.Field()
    # 评论数
    comments_num = scrapy.Field()
    # 收藏数
    fav_num = scrapy.Field()
    # 文章标签
    tags = scrapy.Field()
    # 文章内容
    content = scrapy.Field()
