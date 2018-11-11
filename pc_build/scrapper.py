from bs4 import BeautifulSoup
from urllib.request import urlopen
import json


def scrape(product, n):
    scrape_url = "https://www.newegg.com/global/in-en/Product/ProductList.aspx?Submit=ENE&IsNodeId=1&Description="
    l = []
    for i in range(int(n)):

        webpage = urlopen(scrape_url + str(product) + "&Page=" + str(i+1))
        html_data = BeautifulSoup(webpage.read(), "html.parser")
        webpage.close()
        containers = html_data.findAll("div", {"class": "item-container"})
        if len(containers) <= 0:
            break
        print("Page: " + str(i))
        print("Products: " + str(len(containers)))
        for container in containers:
            try:
                loc_dict = {}
                img_src = container.findAll("a", {"class": "item-img"})[0].img["src"]
                title = container.findAll("a", {"class": "item-title"})[0].text
                brand = title.split()[0]
                price = container.findAll("li", {"class": "price-current"})[0].text.strip()
                if price != "":
                    price_num = "".join(price.split()[1].split(',')[:])
                else:
                    price = "OUT OF STOCK"
                    price_num = 0
                price = " ".join(price.split()[:2])
                loc_dict["Brand"] = brand
                loc_dict["Img_Src"] = img_src
                loc_dict["Title"] = title
                loc_dict["Currency"] = price[0]
                loc_dict["Price"] = price_num
                l.append(loc_dict)
                print(title + " " + price[0] + " " + price_num)
            except Exception as e:
                print(e)
    return l