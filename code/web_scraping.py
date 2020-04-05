import requests
import pandas as pd
from bs4 import BeautifulSoup
import math
import glob

class web_scrape:
    def __init__(self,website_name,url):
        self.website_name = website_name
        self.url = url

    def get_soup(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def get_contents(self,items, class_name):
        name_tags = items.select(".product-tile")
        funko_name = []
        for name in name_tags:
            if name.find("div" , {"class" : class_name}) is None:
                funko_name.append('NONE')
            else:
                funko_name.append(name.find("div" , {"class" : class_name}).get_text().strip())
        return funko_name

    def get_info(self,url):
        soup = self.get_soup(url)
        items = soup.find(id="search-result-items")

        # a list of all the funko names on the current page
        name_tags = items.select(".product-tile .product-name")
        funko_names = [name.get_text().strip() for name in name_tags]

        # a list of all the funko prices on the current page
        price_tags = items.select(".product-tile .product-pricing")
        funko_prices = [price.get_text().strip() for price in price_tags]

        # a list of all the funko promos on the current page
        funko_promos = self.get_contents(items, "product-promo")

        # a list that lets you know if these are online exclusives
        funko_onlineExcs = self.get_contents(items, "online-only")

        return funko_names, funko_prices, funko_promos, funko_onlineExcs

    def create_dataframe(self,master_df, names, prices, promos, online):
        temp_df = pd.DataFrame({
            "Names": names, 
            "Prices": prices,
            "Online": online,
            "Promos": promos
        })
        master_df = master_df.append(temp_df, ignore_index=True)
        return master_df

    def scraping_website(self):
        size = '120'
        start = '0'

        soup = self.get_soup(self.url)
        res = soup.find('div', {"class" : "results-hits"})
        val = res.string.strip().split(' ')
        pages = math.ceil(int(val[0])/int(size))

        master_df = pd.DataFrame()

        for page in range(pages):
            start = str(page*int(size))
            url = self.url + '?sz=' + size + '&start=' + start
            print('Scraping ' + url)
            funko_info = self.get_info(url)
            master_df = self.create_dataframe(master_df, funko_info[0], funko_info[1], funko_info[2], funko_info[3])
            print(len(master_df))

        master_df = master_df.set_index('Names')
        master_df.to_excel("../output/{}output.xlsx".format(self.website_name))

# This works for now I want to see if I can integrate it somewhere in scraping_website()
def combine_doc():
    filename = glob.glob('../output/*.xlsx')
    master_df = pd.DataFrame()

    for file in filename:
        prev_df = pd.read_excel(file)
        master_df = master_df.append(prev_df, ignore_index=True)

    master_df = master_df.set_index('Names')
    master_df.to_excel("../output/masterOutput.xlsx")


if __name__ == '__main__':
    HotTopic = web_scrape('HotTopic','https://www.hottopic.com/funko/')
    BoxLunch = web_scrape('BoxLunch','https://www.boxlunch.com/funko/')
    HotTopic.scraping_website()
    BoxLunch.scraping_website()
    combine_doc()



# TODO: Figure out how to create this into an app. Beeware or kivy of restful API with Flask 
# https://realpython.com/mobile-app-kivy-python/
# Need to do webscarping on the following sites: BoxLunch, Target, Amazon, Walmart, FYI, Funko shop
# Once I have a websire scraped i can look for comaprisions to update the list