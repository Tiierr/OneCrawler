# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests,re
import leancloud
from leancloud import Object
import time

'''
爬虫类,用来从 one 上抓取图片
'''
class One:
    def __init__(self):
        leancloud.init("36awYtC2m4AN1dvLxwv7udxI-gzGzoHsz", "b29MzvGA0aqQQlERUGQJJdBr")
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.num = 42

    def getContent(self,url):
        reqContent = requests.get(url,headers=self.headers)
        if reqContent.status_code == 200:
            story = OneStory()

            soup = BeautifulSoup(reqContent.text,'lxml')
            imgUrl = soup.find('img')['src'].encode('utf-8')
            imgIntr = soup.find('div',{'class':'one-cita'}).get_text().strip().encode('utf-8')
            imgAuth = soup.find('div',{'class':'one-imagen-leyenda'}).get_text().strip().encode('utf-8')
            day = soup.find('p',{'class':'dom'}).get_text().strip().encode('utf-8')
            my = soup.find('p',{'class':'may'}).get_text().strip().encode('utf-8')
            imgDate = day + ' ' + my

            story.set('imgUrl',imgUrl).save()
            story.set('imgIntr',imgIntr).save()
            story.set('imgAuth',imgAuth).save()
            story.set('imgDate',imgDate).save()

            print '正在保存第'+ str(self.num)+'张图片'
            self.num += 1
        else:
            pass

    def start(self):
        baseUrl = 'http://wufazhuce.com/one/'
        for pageNum in range(1,1475):
             url = baseUrl + str(pageNum)
             time.sleep(3)
             self.getContent(url)

'''
实体类用来存储到 Leancloud
'''

class OneImg(Object):

    # imgUrl
    @property
    def imgUrl(self):
        return self.get('imgUrl')
    @imgUrl.setter
    def imgUrl(self, value):
        return self.set('imgUrl', value)

    # imgIntr
    @property
    def imgIntr(self):
        return self.get('imgIntr')
    @imgIntr.setter
    def imgIntr(self, value):
        return self.set('imgIntr', value)

    # imgAuth
    @property
    def imgAuth(self):
        return self.get('imgAuth')
    @imgAuth.setter
    def imgAuth(self, value):
        return self.set('imgAuth', value)

    # imgDate
    @property
    def imgDate(self):
        return self.get('imgDate')
    @imgDate.setter
    def imgDate(self, value):
        return self.set('imgDate', value)

one = One()
one.start()
