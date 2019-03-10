import webview
import requests
from bs4 import BeautifulSoup

comics_dict = {
    '킹덤': 'https://www.mkmk02.com/chapter.php?n=comics&t=3703',
    '베르세르크': 'https://www.mkmk02.com/chapter.php?n=comics&t=1699',
    '원피스': 'https://www.mkmk02.com/chapter.php?n=comics&t=2424',
    '무한의 주인': 'https://www.mkmk02.com/chapter.php?n=comics&t=1203',
    '드래곤볼': 'https://www.mkmk02.com/chapter.php?n=comics&t=768',
    '슬램덩크': 'https://www.mkmk02.com/chapter.php?n=comics&t=6399',
    '배가본드': 'https://www.mkmk02.com/chapter.php?n=comics&t=1686',
    '암살교실': 'https://www.mkmk02.com/chapter.php?n=comics&t=2488',
    '도박마': 'https://www.mkmk02.com/chapter.php?n=comics&t=860',
    '우주형제': 'https://www.mkmk02.com/chapter.php?n=comics&t=2486',
    '20세기 소년': 'https://www.mkmk02.com/chapter.php?n=comics&t=4916',
    '마스터 키튼': 'https://www.mkmk02.com/chapter.php?n=comics&t=1196',
    '약속의 네버랜드': 'https://www.mkmk02.com/chapter.php?n=comics&t=2429',
    '하이큐': 'https://www.mkmk02.com/chapter.php?n=comics&t=4148',
    '사채꾼 우시지마': 'https://www.mkmk02.com/chapter.php?n=comics&t=2217',
    '창천항로': 'https://www.mkmk02.com/chapter.php?n=comics&t=3458',
    '나의 지구를 지켜줘': 'https://www.mkmk02.com/chapter.php?n=comics&t=5567',
    '이누야시키': 'https://www.mkmk02.com/chapter.php?n=comics&t=2478',
    '시티헌터': 'https://www.mkmk02.com/chapter.php?n=comics&t=2092',
    '도박묵시록 카이지': 'https://www.mkmk02.com/chapter.php?n=comics&t=675',
    '펌프킨 시저스': 'https://www.mkmk02.com/chapter.php?n=comics&t=3939',
    '주식회사 천재패밀리': 'https://www.mkmk02.com/chapter.php?n=comics&t=3266',
    '신세기 에반게리온': 'https://www.mkmk02.com/chapter.php?n=comics&t=2297',
    '아키라': 'https://www.mkmk02.com/chapter.php?n=comics&t=5066',
    'MIX 믹스': 'https://www.mkmk02.com/chapter.php?n=comics&t=6375'
}

class Api:
    def comics(self, param):
        result = [{'title': key, 'url': value} for key, value in comics_dict.items()]
        return result

    def chapters(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        links = soup.find_all('a', {'class': 'chapterLink'})
        return [{'title': link['title'], 'url': link['href']} for link in reversed(links)]

    def pages(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        imgs = soup.find_all('img', {'class': 'viewPng'})
        return [img.attrs.get('data-src') for img in imgs]

if __name__ == '__main__':
    api = Api()
    webview.create_window('commics', 'index.html', fullscreen=True, js_api=api, debug=True)