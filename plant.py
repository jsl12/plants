import bs4
import re
import requests

class Plant:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(self.url)

        self.name = self.soup.find(class_='title').get_text()
        self.species = self.soup.find(class_=re.compile('.*species', re.I)).get_text()
        self.care = self.get_care()

    def get_soup(self, url):
        print('Making soup from: {}'.format(url))
        return bs4.BeautifulSoup(requests.get(url).content, 'lxml')

    def get_care(self):
        tab = self.soup.find('div', title=re.compile('.*care', re.I))
        res = {t.get_text(): t.find_next('div') for t in tab.find_all("div", class_=re.compile('post-meta-key'))}
        res = {name: self.extract_text(div) for name, div in res.items()}
        return res

    def extract_text(self, div):
        res = ''
        for c in div.children:
            if isinstance(c, bs4.NavigableString):
                res += c
            elif isinstance(c, bs4.Tag):
                res += next(c.strings)
        res = self.correct_text(res)
        return res

    def correct_text(self, text):
        text = text.replace('  ', ' ')
        text = text.replace(' ,', ',')
        text = text.replace(' .', '.')
        return text

    def to_dict(self):
        return {
            'URL': self.url,
            'Name': self.name,
            'Species': self.species,
            'Care': self.care
        }

    def from_dict(self, dict):
        self.url = dict['URL']
        self.name = dict['Name']
        self.species = dict['Species']
        self.care = dict['Care']

if __name__ == '__main__':
    p = Plant('https://www.houseplant411.com/houseplant/how-to-grow-an-african-violet-plant-care-guide-saintpaulia-ionantha')
    pass