from bs4 import BeautifulSoup
import requests
import re
import urllib.error as err

url = 'http://en.wikipedia.org/wiki/Kevin_Bacon'

pages = set()


def getLinks(wikiURL):
    global pages
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)


try:
    getLinks(url)

except requests.HTTPError as e:
    print(e)

except err.URLError as e:
    print(e)

finally:
    print("soup object created!")

