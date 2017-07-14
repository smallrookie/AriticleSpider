# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

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


class MysqlTwistedPipline(object):
    # 采用连接池方式连接数据库并插入数据

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入，根据不同的item构建不同的sql语句将数据保存至Mysql数据库

        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql,
                       (item["title"], item["url"], item["create_date"], item["fav_num"], item["content"],
                        item["url_object_id"], item["front_image_path"], item["comments_num"], item["praise_num"],
                        item["tags"], item["front_image_url"]))
