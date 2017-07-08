# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline

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
            item["front_image_path"] = image_file_path
        return item
