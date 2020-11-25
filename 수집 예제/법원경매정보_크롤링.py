import requests as req
from bs4 import BeautifulSoup as bs
import xml

url ="https://www.courtauction.go.kr/RetrieveRealEstMgakGyulgwaMulList.laf"
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

res = req.post(url,headers=headers)
soup = bs(res.text, 'lxml')

new_pro = soup.select('td')
for key in new_pro:
    key2 =" ".join(key.text.split())
    print(key2)
