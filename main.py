# 用于scrapy调试

from scrapy.cmdline import execute

import sys
import os

# 添加工程目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 调用execute()执行scrapy命令，爬取伯乐在线
# execute(['scrapy', 'crawl', 'jobbole'])

# 调用execute()执行scrapy命令，爬取知乎
execute(['scrapy', 'crawl', 'zhihu'])