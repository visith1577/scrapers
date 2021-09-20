# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:39:35 2021

@author: visit
"""

import pymysql
conn = pymysql.connect(host='127.0.0.1', user='visith', passwd='helloPython3.10', db='mysql')

curr = conn.cursor()
curr.execute('USE scraping')
curr.execute('SELECT * FROM pages WHERE id = 3')
print(curr.fetchone())
curr.close()
conn.close()