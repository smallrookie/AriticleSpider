# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

import MySQLdb
import MySQLdb.cursors

class AriticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    # 自定义ArticleImagePipeline，下载文章封面图，并获取文章封面图保存路径

    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                # 获取文章封面图保存路径
                image_file_path = value["path"]
                # 获取文章封面图URL
                image_url = value["url"]
            item["front_image_path"] = image_file_path
            # 将front_image_url转为str类型进行数据库存储
            item["front_image_url"] = image_url
        return item


class MysqlPipeline(object):
    # 连接数据库及插入数据操作

    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
                    insert into jobbole_article(title, url, create_date, fav_num, content, url_object_id, front_image_path, comments_num, praise_num, tags, front_image_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        # execute()与commit()为同步操作
        self.cursor.execute(insert_sql,
                            (item["title"], item["url"], item["create_date"], item["fav_num"], item["content"],
                             item["url_object_id"], item["front_image_path"], item["comments_num"], item["praise_num"],
                             item["tags"], item["front_image_url"]))
        self.conn.commit()