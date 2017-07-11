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


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader

    # TakeFirst()默认返回第一个不为None的值
    # 由于在爬取过程中，一些值为None造成项目异常，故采用TakeFirst()重写default_output_processor，其返回值为str类型
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    # 自定义item，用于数据的存储

    # 文章标题
    title = scrapy.Field()
    # 文章发布时间
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    # 当前文章URL
    url = scrapy.Field()
    # 文章URLmd5
    url_object_id = scrapy.Field()
    # 文章封面图
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    # 文章封面图存储路径
    front_image_path = scrapy.Field()
    # 点赞数
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    # 评论数
    comments_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    # 收藏数
    fav_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    # 文章标签
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    # 文章内容
    content = scrapy.Field()