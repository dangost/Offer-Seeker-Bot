from bs4 import BeautifulSoup
import requests
import time

from models.item import Item

ad_in_page = 42


def search(search_setting):
    proxy = {"http": "37.17.9.28:44938"}
    html = requests.get(f"https://www.kufar.by/listings?prn={search_setting.cat}&rgn={search_setting.region}", proxies=proxy).text

    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()

    ads = soup.find_all("a")

    a_dict = {}
    ad_class = ""
    for ad in ads:
        try:
            name = ad.attrs['class'][0]
        except KeyError:
            continue

        if name not in a_dict.keys():
            a_dict[name] = 1
        else:
            a_dict[name] = a_dict[name] + 1
            if a_dict[name] == ad_in_page:
                ad_class = name
                break

    ads = soup.find_all('a', ad_class)

    items = []
    for ad in ads:
        try:
            link = ad.attrs['href']
            photo = ad.contents[0].contents[0].attrs['data-src']
            name = ad.contents[0].contents[0].attrs['alt']
            price = ad.contents[1].contents[1].contents[0].contents[0].contents[0].contents[0]

            item = Item(str(name), str(photo), str(price), str(link))
            items.append(item)
        except KeyError:
            continue

    found = []
    print(f"Setting: {search_setting.name} {search_setting.price}")
    for item in items:
        if item.name.lower().find(search_setting.name.lower()) != -1:
            pr = item.price.split()
            if pr[0] == "Договорная" or float(pr[0]) <= float(search_setting.price):
                if item.link not in search_setting.links:
                    found.append(item)
    time.sleep(3)
    return found

