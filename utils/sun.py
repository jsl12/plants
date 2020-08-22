import re

import bs4
import pandas as pd
import requests


def get_twilights() -> pd.DataFrame:
    soup = bs4.BeautifulSoup(requests.get(r'https://www.timeanddate.com/astronomy/usa/austin').content, 'lxml')
    table = soup.select('tbody')[1]
    rgx = re.compile('\d+:\d+ \w{2}')
    return pd.DataFrame(
        data=[rgx.findall(e.text.upper()) for e in table.select('tr td')],
        columns=['Begin', 'End'],
        index=pd.Index([e.text.strip() for e in table.select('tr th')])
    ).apply(pd.to_datetime)


if __name__ == '__main__':
    df = get_twilights()
    print(df)