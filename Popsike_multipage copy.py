import requests
import results as results
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

headers = {"Accept-Language": "en-US, en;q=0.5"}


title = []
date = []
URL = []
price = []


pages = np.arange(1, 100, 1)

for page in pages:

    page = requests.get("https://www.popsike.com/php/quicksearch.php?searchtext=rhino+records+%7C+elektra+records+%7C+atlantic+records+%7C+parlophone+records+%7C+warner+music+%7C+warner+records+%7C+sire+records+%7C+reprise+records+%7C+nonesuch+records+%7C+maverick+records+%7C+asylum+records+%7C+eastwest+records+%7C+roadrunner+records+-test&sortord=dprice&pagenum="
    + str(page) + "&incldescr=1&sprice=100&eprice=&endfrom=2020&endthru=2020&bidsfrom=&bidsthru=&layout=&flabel=&fcatno=", headers=headers)

    soup = BeautifulSoup(page.text, "html5lib")

    record_div = soup.find_all('div', class_='item-list')

    sleep(randint(2,10))

    for container in record_div:

        description = container.select('h5.add-title > a')[0].text.strip(' \t\n\r')
        title.append(description)

        link = container.find('a')
        URL.append(link.get('href'))

        purchase_date = container.select('span.date > b')[0].text.strip(' \t\n\r')
        date.append(purchase_date)

        purchase_price = container.select('h2.item-price > table > tbody > tr > td:nth-child(4) > b')[0].text.strip(' \t\n\r')
        price.append(purchase_price)

test_data = pd.DataFrame({
'record_description': title,
'link': URL,
'date_of_purchase': date,
'purchased_price': price
})


test_data['link'] = test_data['link'].str.replace('../','https://www.popsike.com/',1)


print(test_data)

test_data.to_csv('popsikeauditallpages.csv')