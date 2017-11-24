from selenium import webdriver
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
import csv

browser = webdriver.Chrome()
wiki = "http://www.imdb.com/india/top-rated-indian-movies"
browser.get(wiki)
soup = BeautifulSoup(browser.page_source, "html5lib")
browser.close()

table = soup.find('table', class_='chart full-width')
count = 0

titles = []
years = []
ratings = []

for row in table.findAll("tr"):
    count = count + 1
    items = row.findAll('td')

    if len(items) > 0:
        titles.append(items[1].a.text)
        years.append(items[1].span.text[1:-1])
        ratings.append(items[2].strong.text)

df=pd.DataFrame()
df['Title']=titles
df['Year']=years
df['Ratings']=ratings

print("DataFrame : ", df.shape)
file_name = "imdb_top.csv"
df.to_csv(file_name, sep = ",", encoding='utf-8', index=False)

print("✅  Writing completed")
