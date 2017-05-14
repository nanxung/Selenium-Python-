# encoding=utf-8

import time
from selenium import webdriver
import requests
import logging
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING) 



kyzg_account = [
  {'no': '18079954801', 'psw': 'chenbo01'}

]

'''下面使用selenium这个强大的库来登录开源中国，获取cookie'''
def getCookies(weibo):
    cookies = []
    loginURL = 'https://www.oschina.net/home/login?goto_page=https%3A%2F%2Fwww.oschina.net%2F'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        try:
            browser = webdriver.Chrome()
            browser.get(loginURL)
            time.sleep(1)
            while "登录" in browser.title:
                username = browser.find_element_by_id("userMail")
                username.clear()
                username.send_keys(account)
                psd = browser.find_element_by_id("userPassword")
                psd.clear()
                psd.send_keys(password)
                commit = browser.find_element_by_tag_name("button")
                commit.click()
                time.sleep(3)

            cookie =''
            if "开源中国 - 找到您想要的开源项目，分享和交流" in browser.title:
                time.sleep(3)
                for elem in browser.get_cookies():
                    cookie+=elem["name"]+"="+ elem["value"]+"; "
                if len(cookie) > 0:
                    logger.warning("获取cookie成功: %s" % account)
                    cookies.append(cookie)
                    continue
            logger.warning("获取cookie失败: %s!" % account)
        except Exception:
            logger.warning("失败 %s!" % account)
        finally:
            try:
                browser.quit()
            except Exception:
                pass
    return cookies



if __name__=='__main__':
    cookies = getCookies(kyzg_account)
    logger.warning("cookie获取完成!( Cookie数目为:%d)" % len(cookies))
    headers={
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
    'Cookie':cookies[0],
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
'hd-token':'hello',
'X-Requested-With':'XMLHttpRequest'
}
    req=requests.Session()
    t=req.get(url='https://www.oschina.net/question/ask?user=3392136',headers=headers)
    with open('a.html','w') as a:
        a.write(t.text)

