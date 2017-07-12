# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from AriticleSpider.utils.jobbole_opration import *


class AriticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhihuQuestionItemLoader(ItemLoader):
    # 自定义知乎问题itemloader

    default_output_processor = TakeFirst()


class ZhihuQuestionItem(scrapy.Item):
    # 自定义知乎问题item，用于数据存储

    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    commments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()


class ZhihuAnswerItemLoader(ItemLoader):
    # 自定义知乎回答itemloader

    default_output_processor = TakeFirst()


class ZhihuAnswerItem(scrapy.Item):
    # 自定义知乎回答item，用于数据存储

    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    commments_num = scrapy.Field()
    crawl_time = scrapy.Field()
