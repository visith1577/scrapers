# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 15:42:01 2021

@author: visit
"""

from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import re
import pymysql
from random import shuffle

conn = pymysql.connect(host='127.0.0.1', 
                       user='visith', passwd='helloPython3.10', db='mysql', 
                       charset='utf8')

cur = conn.cursor()
cur.execute('USE wikipedia')

def insertPageIfNotExists(url):
    cur.execute('SELECT * FROM pages WHERE url = %s', (url))
    if cur.rowcount == 0:
        cur.execute('INSERT INTO pages (url) VALUES (%s)', (url))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0] 


def loadPages():
    cur.execute('SELECT * FROM pages')
    pages = [row[1] for row in cur.fetchall()]
    return pages        


def insertLink(fromPageId, toPageId):
    cur.execute('SELECT * FROM links WHERE fromPageId = %s '
     'AND toPageId = %s', (int(fromPageId), int(toPageId)))
    if cur.rowcount == 0:
        cur.execute('INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)',
                    (int(fromPageId), int(toPageId)))
        conn.commit()


def get_links(pageURL, recursionLevel, pages):
    if recursionLevel > 4:
        return 
    
    pageId = insertPageIfNotExists(pageURL)
    html = urlopen('http://en.wikipedia.org{}'.format(pageURL))
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    links = [link.attrs['href'] for link in links]
    
    
    for link in links:
        insertLink(pageId, insertPageIfNotExists(link))
        if link not in pages:
            pages.append(link)
            get_links(link, recursionLevel+1, pages)
            
            
if __name__ == '__main__':
    try:
        get_links('/wiki/Kevin_Bacon', 0, loadPages())
    finally:
        cur.close()
        conn.close()            