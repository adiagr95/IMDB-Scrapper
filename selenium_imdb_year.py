from selenium import webdriver
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
import csv
import re
from mysql_client import *
import sys, traceback

db = Database()
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)

year = int(input("Enter Year : "))
page_count = input("Page Count (Optional) : ")
if page_count:
    page_count = int(page_count)
else:
    page_count = 0

while True:
    A = [] # Index
    B = [] # Link
    C = [] # Title
    D = [] # Year
    E = [] # Certificate
    F = [] # Duration
    G = [] # Generes
    H = [] # Ratings
    I = [] # Desc
    J = [] # Directors
    K = [] # Stars
    L = [] # Votes

    browser = webdriver.Chrome(chrome_options=chromeOptions)

    wiki = f"http://www.imdb.com/search/title?release_date={str(year)}&page={str(page_count + 1)}"
    print("💻  Url : ", wiki)
    browser.get(wiki)
    soup = BeautifulSoup(browser.page_source, "html5lib")
    browser.close()
    table = soup.find('div', class_='lister-list')

    divs = table.findAll("div", class_ = 'lister-item mode-advanced')
    if len(divs) == 0:
        break

    for row in divs:
        div = row.findAll("div")[4]
        A.append(re.sub("[^0-9]", "", div.h3.find("span", class_ = "lister-item-index").text))
        B.append(div.h3.find("a")["href"])
        C.append(div.h3.find("a").text.replace("\"", "\'"))
        D.append(re.sub("[^0-9]", "", div.h3.find("span", class_ = "lister-item-year").text))

        certificate = row.p.find("span", class_ = "certificate")
        runtime = row.p.find("span", class_ = "runtime")
        genre = row.p.find("span", class_ = "genre")

        E.append(certificate.text) if certificate else E.append("")
        F.append(re.sub("[^0-9]", "", runtime.text)) if runtime else F.append("")
        G.append([g.replace(" ", "").replace("\n", "") for g in genre.text.split(",")]) if genre else G.append([])
        H.append(div.find("div", class_ = "ratings-bar").div.strong.text) if div.find("div", class_ = "ratings-bar") and div.find("div", class_ = "ratings-bar").div and div.find("div", class_ = "ratings-bar").div.strong else H.append("")
        I.append(div.findAll("p", class_ = "text-muted")[1].text.replace("\n", "").replace("\"", "\'")) if len(div.findAll("p", class_ = "text-muted")) > 0 else I.append("")

        if len(div.findAll("p", class_ = "")) > 0:
            casts = re.sub(' +',' ',div.findAll("p", class_  = "")[1].text.replace("\n", "")).lower().replace("\"", "\'")
            if not "|" in casts:
                casts = "|" + casts
            casts = casts.split("|")
            J.append([a.strip() for a in casts[0].replace("Directors:", "").replace("Director:", "").split(",")])
            K.append([a.strip() for a in casts[1].replace("Stars:", "").replace("Star:", "").split(",")])
        else:
            J.append([])
            K.append([])

        if div.find("p", class_ = "sort-num_votes-visible") and len(div.find("p", class_ = "sort-num_votes-visible").findAll("span")) > 0:
            try:
                L.append(int(div.find("p", class_ = "sort-num_votes-visible").findAll("span")[1].text.replace(",", "")))
            except:
                L.append("")
        else:
            L.append("")

    db.insert(zip(A, B, C, D, E, F, G, H , I , J , K , L))
    page_count = page_count + 1

print("✅  Scrapping completed, writing")

# df=pd.DataFrame(A,columns=['Number'])
# df['Link']=B
# df['Title']=C
# df['Year']= D
# df['Certificate']= E
# df['Duration']= F
# df['Genere']= G
# df['Ratings']= H
# df['Desc']= I
# df['Directors']= J
# df['Stars']= K
# df['Votes']= L

# file_name = f"imdb_{str(year)}.csv"
# df.to_csv(file_name, sep = ",", encoding='utf-8', index=False)

print("✅  Writing completed")
