import time

from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path="D:/Python/chromedriver_win32/chromedriver.exe")

# 模拟知乎登录
# browser.get("https://www.zhihu.com/#signin")
#
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("")
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("")
#
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()

# 模拟新浪微博登录
browser.get("https://www.weibo.com/")

time.sleep(15)

browser.find_element_by_css_selector("#loginname").send_keys("")
browser.find_element_by_css_selector(".info_list.password input[name='password']").send_keys("")

browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()