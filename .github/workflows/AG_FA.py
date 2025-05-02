import requests
import re
from bs4 import BeautifulSoup
import time

url = 'https://divar.ir/s/tehran'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
data = requests.get(url , headers=headers).text
soup = BeautifulSoup(data , 'html.parser')
a_tag = soup.findAll('a' , class_="kt-accordion-item__header kt-accordion-item__header--with-icon")

data_list = []

for link in a_tag:
    data_list.append('https://divar.ir'+link.get('href'))



for url in data_list:
    time.sleep(0.4)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    a_tags = soup.find_all('a', class_="kt-post-card__action")
    temp_list = []
    for link in a_tags:
        temp_list.append('https://divar.ir' + link.get('href'))

    print(temp_list)
    print('######################')
