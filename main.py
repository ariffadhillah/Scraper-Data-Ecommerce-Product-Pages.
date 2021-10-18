import requests
from bs4 import BeautifulSoup

import pandas as pd

baseUrl = 'https://www.thewhiskyexchange.com'

headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
# https://www.burlapandbarrel.com/collections/all?page={x}'
productlinks = []

for x in range(1,6):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}&psize=24&sort=pasc')

    soup = BeautifulSoup(r.content, 'lxml')

    productlist = soup.find_all('li', class_='product-grid__item')    

    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseUrl+link['href'])
            # productlinks.append(baseUrl = link['href'])        

# print(productlinks)

# testlink = 'https://www.thewhiskyexchange.com/p/49821/hatozaki-blended-japanese-whisky'
whiskylist = []

for link in productlinks:
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    name =  soup.find('h1', class_='product-main__name').text.strip()
    Price =  soup.find('p', class_='product-action__price').text.strip()
    description =  soup.find('div', class_='product-main__description').text.strip()
    try:
        ranting =  soup.find('span', class_='review-overview__rating').text.strip()
        riviews =  soup.find('span', class_='review-overview__count').text.strip()
    except:
        ranting = 'no ranting'
        riviews = 'no riviews'
    

    wisky = {
        'name' : name,
        'ranting' : ranting,
        'riviews' : riviews,
        'Price' : Price,
        'description' : description

    }

    whiskylist.append(wisky)
    print('Saving:', wisky['name'])


df = pd.DataFrame(whiskylist)
# df.to_csv(index=False)
print(df.head(15))
df.to_csv('file_name.csv', encoding='utf-8')