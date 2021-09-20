# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 13:58:16 2021

@author: visit
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv 


URL = "https://en.wikipedia.org/wiki/Comparison_of_text_editors"

def get_url(url):
    try:
        results = urlopen(url)
        bs = BeautifulSoup(results, 'html.parser')
    except HTTPError:
        print("Request failed!")
    finally:
        return bs 
            
def find_data(url):
    bs = get_url(url)
    table = bs.find_all('table', {'class': 'wikitable'})[0]
    rows = table.find_all('tr')
    return rows 


def write_csv(url):
    csvFile = open('editors.csv', 'wt+', encoding='utf-8')
    writer = csv.writer(csvFile)
    rows = find_data(url)
    
    try:
        for row in rows:
            csvRow=[]
            for cell in row.find_all(['td', 'th']):
                csvRow.append(cell.get_text())
                writer.writerow(csvRow)
    finally:
        csvFile.close()
        
if __name__ == '__main__':
    write_csv(URL)        
    
    

