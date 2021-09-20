from bs4 import BeautifulSoup
import requests
import re

url = " http://www.pythonscraping.com/pages/page3.html."

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

imgs = soup.find_all("img", {'src': re.compile("\.\.\/img\/gifts/img.*\.jpg")})

for img in imgs:
    print(img)

