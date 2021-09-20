import requests
from bs4 import BeautifulSoup
import re


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f"URL: {self.url}")
        print(f"Title : {self.title}")
        print(f"Body : \n {self.body}")


class Website:
    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    @staticmethod
    def getPage(url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException as e:
            return print(e)
        return BeautifulSoup(req.text, 'html.parser')

    @staticmethod
    def safeGet(pageObj, selecter):
        selectedElems = pageObj.select(selecter)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for
                              elem in selectedElems])
        return ''

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.title)
            body = self.safeGet(bs, self.site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        bs = self.getPage(self.site.url)
        targetPages = bs.find_all('a',
                                  href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)
            if not self.site.absoluteUrl:
                targetPage = '{}{}'.format(self.site.url, targetPage)
            self.parse(targetPage)


reuters = Website('Reuters', 'https://www.reuters.com', '^(/article/)', False,
                  'span', 'div.StandardArticleBody_body_1gnLA')
crawler = Crawler(reuters)
crawler.crawl()
