# Note: from each page we can get max of 25 episodes

from bs4 import BeautifulSoup
import requests


class Torrent:
    # base_url = 'https://nyaa.si'
    base_url = 'https://nyaa.unblockit.li'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }

    providers = {
        'sp': 'subsplease',
        'hs': 'horriblesubs',
        'er': 'Erai-raws'
    }

    def remove_par(self, str):
        res = ''
        if str[0] == '[' or str[0] == '(':
            i = 1
            while str[i] != ']' and str[i] != ')':
                res += str[i]
                i += 1
        return res

    def get_details(self, l, grp):

        d = {}
        if grp == 'sp':
            d['qua'] = self.remove_par(l[-2])
            d['epi'] = l[-3]
        elif grp == 'hs':
            d['qua'] = self.remove_par(l[-1])
            d['epi'] = l[-2]
        elif grp == 'er':
            if "Subtitle].mkv" in l:
                d['qua'] = self.remove_par(l[-2])
                d['epi'] = l[-3]
            else:
                d['qua'] = self.remove_par(l[-1])
                d['epi'] = l[-2]

        return d

    # limit: no. of retries when page is not loaded
    def get_req(self, url, limit=15):
        s = True
        i = 0

        while s:
            if i > limit:
                return

            try:
                r = requests.get(url, headers=self.headers)
                return r
            except Exception:
                i += 1
                print('Retrying....')

    def organise(self, resList, epiList):

        data = {}
        for r in epiList:
            data[f"{r}"] = {
                '480p': {
                    'size': None,
                    'link': None
                },
                '720p': {
                    'size': None,
                    'link': None
                },
                '1080p': {
                    'size': None,
                    'link': None
                }
            }

        for item in resList:
            data[f'{item["epiNo"]}'][f"{item['quality']}"]['size'] = item['size']
            data[f'{item["epiNo"]}'][f"{item['quality']}"]['link'] = item['link']

        return data

    # category: 2-sub, 3-dub
    # provider: subsplease/horriblesubs/eri-raws
    # file: 0-torrent file, 1- magnet
    # page: no. of pages to search
    def search(self, query, category=2, provider='sp', file=1, page=1):
        url = f'{self.base_url}/user/{self.providers[provider]}?f=0&c=1_{category}&q={query}&o=desc&p={page}'

        req = self.get_req(url)
        if req is None:
            return "Try Agian after a minute :("

        soup = BeautifulSoup(req.text, 'html.parser')

        rows = soup.find_all('tr', 'success')
        resultList = []
        epiList = []

        for row in rows:

            res = {}
            links = row.find_all('td', class_='text-center')[0].find_all('a')
            magnet = self.base_url + \
                links[0]['href'] if file else links[1]['href']

            size = row.find_all('td', class_='text-center')[1].text

            res['link'] = magnet
            res['size'] = size

            row_data = row.findAll('a')
            for data in row_data:
                if data.has_attr('title') and query.upper().split()[0] in data['title'].upper():
                    title = data['title'].split(" ")
                    d = self.get_details(title, provider)
                    res['epiNo'] = d['epi']
                    epiList.append(res['epiNo'])
                    res['quality'] = d['qua']
            resultList.append(res)

        return self.organise(resultList, epiList)
