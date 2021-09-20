# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 10:04:35 2021

@author: visit
"""

from urllib.request import urlopen 
from urllib.error import HTTPError
from bs4 import BeautifulSoup 
import re 
import pymysql 
import random

URL = "https://en.wikipedia.org/wiki/Kevin_Bacon"

conn = pymysql.connect(host='127.0.0.1', user='visith', passwd='helloPython3.10', db='mysql', charset='utf8')

curr = conn.cursor() 
curr.execute('USE scraping')

def get_url(url):
    try:
        results = urlopen(url)
        bs = BeautifulSoup(results, 'html.parser')
    except HTTPError:
        print("Request failed!")
    finally:
        return bs 
            
def find_data(url):
    results = urlopen(url)
    bs = BeautifulSoup(results, 'html.parser')
    title = bs.find('h1').text
    content = bs.find('div', {'id': 'mw-content-text'}).find('p').text 
    store(title, content)
    return bs.find('div', {'id':'bodyContent'}).findAll('a',
             href=re.compile('^(/wiki/)((?!:).)*$'))


def store(title, content):
    curr.execute('INSERT INTO pages (title, content) VALUES ''("%s", "%s")', (title, content))
    curr.connection.commit()
    
if __name__ == '__main__':
    links = find_data(URL)
    try:
        while len(links)>0:
            newArticle = links[random.randint(0, len(links)-1)].attrs['href']
            print(newArticle)
            links=find_data('https://en.wikipedia.org' + newArticle)
    finally:
            curr.close()
            conn.close()