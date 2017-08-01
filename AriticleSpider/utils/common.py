# coding=utf-8

import hashlib
import re

from elasticsearch_dsl.connections import connections

from AriticleSpider.models.es_types import ArticleType


# md5函数
def get_md5(url):
    # 若url为Unicode，则将其转为utf-8
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(value):
    # 利用正则表达式获取相应的数值

    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num


def gen_suggestions(index, info_tuple):
    # 根据字符串生成搜索建议

    used_words = set()
    suggestions = []
    es = connections.create_connection(ArticleType._doc_type.using)

    for text, weight in info_tuple:
        if text:
            # 调用es的analyze分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={"filter": ["lowercase"]}, body=text)
            analyzer_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzer_words - used_words
        else:
            new_words = set()

        if new_words:
            suggestions.append({"input": list(new_words), "weight": weight})

    return suggestions


# 测试MD5函数
if __name__ == '__main__':
    print(get_md5("http://jobbole.com".encode("utf-8")))
