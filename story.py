# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests,re
import leancloud
from leancloud import Object
import time

'''
爬虫类,用来从 one 上抓取文章
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
            intro = soup.find('div',{'class':'comilla-cerrar'}).get_text().strip().encode('utf-8')
            title =  soup.find('h2',{'class':"articulo-titulo"}).get_text().strip().encode('utf-8')
            author = soup.find('p',{'class':"articulo-autor"}).get_text().strip()[3:].encode('utf-8')
            body =  soup.find('div',{'class':'articulo-contenido'}).get_text().strip().encode('utf-8')

            story.set('storyIntr',intro).save()
            story.set('storyTitle',title).save()
            story.set('storyAuthor',author).save()
            story.set('storyBody',body).save()

            print '正在保存第'+ str(self.num)+'篇文章'
            self.num += 1
        else:
            pass

    def start(self):
        baseUrl = 'http://wufazhuce.com/article/'
        for pageNum in range(60,1537):
             url = baseUrl + str(pageNum)
             time.sleep(3)
             self.getContent(url)

'''
实体类用来存储到 Leancloud
'''

class OneStory(Object):
    # storyIntr
    @property
    def storyIntr(self):
        return self.get('storyIntr')
    @storyIntr.setter
    def storyIntr(self, value):
        return self.set('storyIntr', value)

    # storyTitle
    @property
    def storyTitle(self):
        return self.get('storyTitle')
    @storyTitle.setter
    def storyTitle(self, value):
        return self.set('storyTitle', value)

    # storyAuthor
    @property
    def storyAuthor(self):
        return self.get('storyAuthor')
    @storyAuthor.setter
    def storyAuthor(self, value):
        return self.set('storyAuthor', value)

    # storyBody
    @property
    def storyBody(self):
        return self.get('storyBody')
    @storyBody.setter
    def storyBody(self, value):
        return self.set('storyBody', value)


one = One()
one.start()
