# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

from AriticleSpider.utils.jobbole_opration import *
from AriticleSpider.utils.lagou_opration import *
from AriticleSpider.utils.common import extract_num, gen_suggestions
from AriticleSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
from AriticleSpider.models.es_types import ArticleType


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
        # 由于采用自定义
        output_processor=MapCompose(return_value)
    )
    # 文章封面图存储路径
    front_image_path = scrapy.Field()
    # 点赞数
    praise_num = scrapy.Field(
        input_processor=MapCompose(extract_num)
    )
    # 评论数
    comments_num = scrapy.Field(
        input_processor=MapCompose(extract_num)
    )
    # 收藏数
    fav_num = scrapy.Field(
        input_processor=MapCompose(extract_num)
    )
    # 文章标签
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    # 文章内容
    content = scrapy.Field()

    def get_insert_sql(self):
        # 具体实现存储伯乐在线文章的SQL语句

        insert_sql = """
                    insert into jobbole_article(title, url, create_date, fav_num, content, url_object_id,
                    front_image_path, comments_num, praise_num, tags, front_image_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                    content=VALUES(fav_nums)
                    """

        params = (
            self["title"], self["url"], self["create_date"], self["fav_num"], self["content"], self["url_object_id"],
            self["front_image_path"], self["comments_num"], self["praise_num"], self["tags"], self["front_image_url"])

        return insert_sql, params

    def save_to_es(self):
        # 将item转换为es的数据

        article = ArticleType()
        article.title = self["title"]
        article.create_date = self["create_date"]
        article.content = remove_tags(self["content"])
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.praise_num = self["praise_num"]
        article.comments_num = self["comments_num"]
        article.fav_num = self["fav_num"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.meta.id = self["url_object_id"]

        # 搜索建议词
        article.suggestions = gen_suggestions(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))

        article.save()


class ZhihuQuestionItem(scrapy.Item):
    # 自定义知乎问题item，用于数据存储

    # 问题id
    zhihu_id = scrapy.Field()
    # 问题所属话题
    topics = scrapy.Field()
    # 问题的URL链接
    url = scrapy.Field()
    # 问题的标题
    title = scrapy.Field()
    # 问题的内容
    content = scrapy.Field()
    # 问题的回答数
    answer_num = scrapy.Field()
    # 问题的评论数
    comments_num = scrapy.Field()
    # 问题的关注人数
    watch_user_num = scrapy.Field()
    # 问题的浏览数
    click_num = scrapy.Field()
    # 问题的爬取时间
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 具体实现存储知乎问题的SQL语句

        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num, 
            watch_user_num, click_num, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """

        # 由于itemloader会将item中的值转变为list类型，故需将这些值转为str类型
        # 此处采用有别于存储伯乐在线文章的方法
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topics, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time,)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 自定义知乎回答item，用于数据存储

    # 问题回答的id
    zhihu_id = scrapy.Field()
    # 问题回答的url链接
    url = scrapy.Field()
    # 问题的id
    question_id = scrapy.Field()
    # 回答者的id
    author_id = scrapy.Field()
    # 回答的内容
    content = scrapy.Field()
    # 点赞数
    praise_num = scrapy.Field()
    # 回答发布时间
    create_time = scrapy.Field()
    # 回答更新时间
    update_time = scrapy.Field()
    # 回答的评论数
    comments_num = scrapy.Field()
    # 回答的爬取时间
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 具体实现存储知乎回答的SQL语句

        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, create_time,
            update_time, comments_num, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),
              update_time=VALUES(update_time)
        """
        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATE_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATE_FORMAT)

        params = (
            self["zhihu_id"], self["url"], self["question_id"], self["author_id"], self["content"], self["praise_num"],
            create_time, update_time, self["comments_num"],
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),)

        return insert_sql, params


class LagouJobItemLoader(ItemLoader):
    # 自定义item loader

    default_output_processor = TakeFirst()


class LagouJob(scrapy.Item):
    # 自定义拉勾网item，用于数据存储

    # 职位名称
    title = scrapy.Field()
    # 职位信息URL
    url = scrapy.Field()
    # 职位信息URL的MD5值
    url_object_id = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 职位所在城市
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    # 工作经验
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    # 学历要求
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    # 职位类型
    job_type = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 职位诱惑
    job_advantage = scrapy.Field()
    # 职位描述
    job_desc = scrapy.Field()
    # 工作地址
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_job_addr)
    )
    # 公司名称
    company_name = scrapy.Field()
    # 公司信息页面的URL
    company_url = scrapy.Field()
    # 职位标签
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    # 爬取时间
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 具体实现存储拉勾职位信息的SQL语句

        insert_sql = """
            insert into lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need, job_type, 
            publish_time, job_advantage, job_desc, job_addr, company_name, company_url, tags, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE
            salary=VALUES(salary), job_desc=VALUES(job_desc), publish_time=VALUES(publish_time)
        """
        params = (self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"],
                  self["work_years"], self["degree_need"], self["job_type"], self["publish_time"],
                  self["job_advantage"], self["job_desc"], self["job_addr"], self["company_name"],
                  self["company_url"], self["tags"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT))

        return insert_sql, params
