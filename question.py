# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests,re
import leancloud
from leancloud import Object
import time

'''
爬虫类,用来从 one 上抓取问题以及回答
'''
class One:
    def __init__(self):
        leancloud.init("36awYtC2m4AN1dvLxwv7udxI-gzGzoHsz", "b29MzvGA0aqQQlERUGQJJdBr")
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.num = 1

    def getContent(self,url):
        reqContent = requests.get(url,headers=self.headers)
        if reqContent.status_code == 200:
            question = Onequestion()

            soup = BeautifulSoup(reqContent.text,'lxml')
            title = soup.find('div',{'class':'one-cuestion'}).findAll('h4')[0].get_text().strip().encode('utf-8')
            detail = soup.findAll('div',{'class':'cuestion-contenido'})[0].get_text().strip().encode('utf-8')
            headAns = soup.find('div',{'class':'one-cuestion'}).findAll('h4')[1].get_text().strip().encode('utf-8')
            answer = soup.findAll('div',{'class':'cuestion-contenido'})[1].get_text().strip().encode('utf-8')

            question.set('qaIntr',title).save()
            question.set('qaDetail',detail).save()
            question.set('qaAnsw',headAns+answer).save()

            print '正在保存第'+ str(self.num)+'个问题'
            self.num += 1
        else:
            pass

    def start(self):
        baseUrl = 'http://wufazhuce.com/question/'
        for pageNum in range(1,1480):
             url = baseUrl + str(pageNum)
             time.sleep(3)
             self.getContent(url)

'''
实体类用来存储到 Leancloud
'''

class OneQa(Object):

    # qaIntr
    @property
    def qaIntr(self):
        return self.get('qaIntr')
    @qaIntr.setter
    def qaIntr(self, value):
        return self.set('qaIntr', value)

    # qaDetail
    @property
    def qaDetail(self):
        return self.get('qaDetail')
    @qaDetail.setter
    def qaDetail(self, value):
        return self.set('qaDetail', value)

    # qaAnsw
    @property
    def qaAnsw(self):
        return self.get('qaAnsw')
    @qaAnsw.setter
    def qaAnsw(self, value):
        return self.set('qaAnsw', value)

one = One()
one.start()
