import datetime
import re


def date_convert(value):
    # 时间转换，由于所爬取的时间为str类型，故需转为date类型进行数据库存储

    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def remove_comment_tags(value):
    # 去除tag中的评论

    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    # 覆盖default_output_processor = TakeFirst()，将front_image_url的值变回list类型

    return value


def get_num(value):
    # 利用正则表达式获取相应的数值

    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num
