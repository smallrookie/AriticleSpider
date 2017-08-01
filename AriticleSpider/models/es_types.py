from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, analyzer, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    # 自定义analyzer

    def get_analysis_definition(self):
        # 避免使用默认的analyzer异常报错问题

        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(DocType):
    # 伯乐在线文章类型

    # 搜索建议
    suggestions = Completion(analyzer=ik_analyzer)

    # 文章标题
    title = Text(analyzer="ik_max_word")
    # 文章发布时间
    create_date = Date()
    # 当前文章URL
    url = Keyword()
    # 文章URLmd5
    url_object_id = Keyword()
    # 文章封面图
    front_image_url = Keyword()
    # 文章封面图存储路径
    front_image_path = Keyword()
    # 点赞数
    praise_num = Integer()
    # 评论数
    comments_num = Integer()
    # 收藏数
    fav_num = Integer()
    # 文章标签
    tags = Text(analyzer="ik_max_word")
    # 文章内容
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = 'jobble'
        doc_type = "article"


if __name__ == "__main__":
    ArticleType.init()
