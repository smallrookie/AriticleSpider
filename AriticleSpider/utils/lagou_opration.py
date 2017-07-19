def remove_splash(value):
    # 去除所在城市的斜杠

    return value.replace("/", "")


def handle_job_addr(value):
    # 去除多余的空格

    add_list = value.split("\n")
    add_list = [item.strip() for item in add_list if item.strip() != "查看地图"]
    return "".join(add_list)
