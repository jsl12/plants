from bs4 import BeautifulSoup
import re
import requests

result = requests.get("https://www.houseplant411.com/houseplant/anthurium-plant-how-to-grow-care-flaming-flower")

soup = BeautifulSoup(result.content, 'lxml')

res = {t.get_text(): t.find_next('div').get_text() for t in soup.find('div', title='Care').find_all("div", {"class" : re.compile('post-meta-key')})}

pass