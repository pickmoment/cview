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
    '암살교실': 'https://www.mkmk02.com/chapter.php?n=comics&t=2488'
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