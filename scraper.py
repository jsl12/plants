from bs4 import BeautifulSoup
import re
import requests

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.pages = self.get_all_pages(max=2)
        self.soups = self.create_soups(self.pages)

    def create_soups(self, pages):
        return [BeautifulSoup(p.content, 'lxml') for p in pages]

    def get_page(self, num):
        return requests.get('https://www.houseplant411.com/houseplant/page/{}'.format(num))

    def get_all_pages(self, max=None):
        pages = []
        i = 1
        while True:
            try:
                pages.append(self.get_page(i))
                print('Downloaded page {}'.format(i))
                if max is not None:
                    if len(pages) >= max:
                        break
                i += 1
            except:
                print('Reached the final page')
                break
        return pages

    def get_plant_links(self, soup):
        links = [link for link in soup.find_all('a', href=re.compile('https:\/\/www.houseplant411.com\/houseplant\/(\w+-?)+$'))]
        links = [link for link in links if link.get_text() != '' and link.get_text() != 'Read More']
        links = {link.get_text(): link['href'] for link in links}
        return links

    def get_all_plant_links(self, soups):
        links = {}
        for soup in soups:
            links.update(self.get_plant_links(soup))
        return links

if __name__ == '__main__':
    s = Scraper('https://www.houseplant411.com/houseplant')
    s.links = s.get_all_plant_links(s.soups)
    pass