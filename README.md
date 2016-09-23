爬取 One 上面的文章、图片以及问答

## 一. 过程分析

打开[ONE](http://wufazhuce.com/)的主页,[ONE](http://wufazhuce.com/)的网站主要有四个部分组成:
- 主页(http://wufazhuce.com/)
- 文章(http://wufazhuce.com/article/xxx)
- 图片(http://wufazhuce.com/one/xxx)
- 问题(http://wufazhuce.com/question/xxx)

我们以文章页面分析,其他页面的爬取与之类似。

![](http://i1.piimg.com/567571/9726131b92242331.png)

如上即为`One`的文章界面。同样分为四个部分:
- 摘要
- 标题
- 作者
- 正文

看`网页源码`如下:
摘要
- ![](http://i1.piimg.com/567571/995bb85212bb9819.png)
标题
- ![](http://i1.piimg.com/567571/a79dfb4e861fb053.png)
作者
- ![](http://i1.piimg.com/567571/894804bad49bc4c2.png)
正文
- ![](http://i1.piimg.com/567571/286700ab889b36a4.png)

`ONE`的代码标签还是挺清晰明了的,可以直接利用`beautiful soup`的`find`函数直接提取对应的数据。


## 二. 抓取代码

```python
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

```

核心代码如上。

* 采用 request 库来进行网络请求。一旦返回的 statusCode 不等于 200,就不会进行下一步动作。


## 三. 数据存储

```python
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
```

* 数据的存储为 leanCloud 云存储。这一块可以自己看看官方文档,非常简单。

* 如上代码。我们采用 property 属性来构建实体类。即面向对象思想的一些体现。这样存储过程就更为直观简单了。

### 爬取结果截图
![](http://i1.piimg.com/567571/36d5ba0930826c14.png)
