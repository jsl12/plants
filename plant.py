import bs4
import re
import requests

class Plant:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(self.url)

        self.name = self.soup.find(class_='title').get_text()
        self.species = self.soup.find(class_=re.compile('.*species', re.I)).get_text()

    def get_soup(self, url):
        return bs4.BeautifulSoup(requests.get(url).content, 'lxml')

    def get_care(self):
        tab = self.soup.find('div', title=re.compile('.*care', re.I))
        res = {t.get_text(): t.find_next('div') for t in tab.find_all("div", class_=re.compile('post-meta-key'))}
        res = {name: self.extract_text(div) for name, div in res.items()}
        return res

    def extract_text(self, div):
        res = []
        for c in div.children:
            if isinstance(c, bs4.NavigableString):
                res.append(c.strip())
            elif isinstance(c, bs4.Tag):
                res.append(next(c.strings).strip())
        res = ' '.join(res)
        return res

if __name__ == '__main__':
    p = Plant('https://www.houseplant411.com/houseplant/how-to-grow-an-african-violet-plant-care-guide-saintpaulia-ionantha')
    p.get_care()
    pass