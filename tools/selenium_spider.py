import time

from selenium import webdriver
from scrapy.selector import Selector

# browser = webdriver.Chrome(executable_path="D:/Python/chromedriver_win32/chromedriver.exe")

# 模拟知乎登录
# browser.get("https://www.zhihu.com/#signin")
#
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("")
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("")
#
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()

# 模拟新浪微博登录
# browser.get("https://www.weibo.com/")
#
# time.sleep(15)
#
# browser.find_element_by_css_selector("#loginname").send_keys("")
# browser.find_element_by_css_selector(".info_list.password input[name='password']").send_keys("")
#
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

# 模拟鼠标下滑操作
# browser.get("https://www.oschina.net/blog")
#
# time.sleep(5)
#
# for i in range(3):
#     browser.execute_script(
#         "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
#     time.sleep(3)

# 设置chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(executable_path="D:/Python/chromedriver_win32/chromedriver.exe", chrome_options=chrome_opt)
# browser.get("https://www.taobao.com")

# phantomjs获取动态页面
browser = webdriver.PhantomJS(executable_path="D:/Python/phantomjs-2.1.1-windows/bin/phantomjs.exe")
browser.get("https://detail.tmall.com/item.htm?spm=a1z10.1-c-s.w12075169-15146113259.31.3910d3c510iTDI&id=540677596153&scene=taobao_shop&sku_properties=10004:1162302684;5919063:6536025")
print(browser.page_source)
browser.quit()
