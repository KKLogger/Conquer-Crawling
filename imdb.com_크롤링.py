import pandas as pd
import numpy as np
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


# Top Rated Movie 크롤링
base_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
res = req.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
html_text = bs(res.text, "html.parser")
num = 250

title_list = html_text.find_all("td", {"class": "titleColumn"})
title_list = [x.text.strip().replace("\n", '').split('      ')[1].split('(')[0] for x in title_list]
rank_list = np.arange(num) + 1
year_list = html_text.find_all("span", {"class": "secondaryInfo"})
year_list = [x.text for x in year_list]
rating_list = html_text.find_all("strong")
rating_list = [x.text for x in rating_list]

# rating_list=rating_list[:10]


# 세부 내용 크롤링
href_list = html_text.find_all("td", {"class": "titleColumn"})
href_list = [x.find("a").get("href") for x in href_list]

url_list = [urljoin(base_url, x) for x in href_list]

genres_list = []
runtime_list = []
director_list = []
total_revenue_list = []
cnt = 1
for x in url_list:
    print(cnt)
    cnt = cnt+1
    # x=url_list[0]
    res = req.get(x)
    html_text = bs(res.text, "html.parser")
    # 장르 리스트
    genres = html_text.find_all("div", {"class": "see-more inline canwrap"})
    genres = [x.find("a") for x in genres]
    genres = genres[1].text.strip()
    genres_list.append(genres)
    # 상영시간 리스트
    runtime = html_text.find_all("time")
    runtime_list.append(runtime[0].text.strip())

    director = html_text.find("div", {"class": "credit_summary_item"}).find("a").text
    director_list.append(director)

    total_revenue = html_text.find_all("div", {"id": "titleDetails"})
    total_revenue = total_revenue[0].find_all("div", {"class": "txt-block"})
    total_revenue = [x.text.strip().replace("\n", "").split(":") for x in total_revenue]
    temp = "None"
    for i in range(len(total_revenue)):
        if total_revenue[i][0] == "Cumulative Worldwide Gross":
            temp=total_revenue[i][1].strip()
            break
    total_revenue_list.append(temp)


df = pd.DataFrame(title_list,index=rank_list, columns=["title"])
df["year"] = year_list
df["rating"] = rating_list
df["genres"] = genres_list
df["runtime"] = runtime_list
df["director"] = director_list
df["total revenue"] = total_revenue_list


df.index.names = ["rank"]
df.columns.names = ["Info"]
# 덮어쓰기 mode =a 기 추가
df.to_excel('imdb.com_크롤링.xlsx', sheet_name='TOP250정보')