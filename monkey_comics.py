import requests
from bs4 import BeautifulSoup
import json
import re

import eel

# Set web files folder and optionally specify which file types to check for eel.expose()
eel.init('web', allowed_extensions=['.js', '.html'])


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

view_snapshot = {}
view_snapshot_file = 'view_snapshot.json'

@eel.expose
def search(title):
    url = 'https://www.mkmk02.com/search.php'
    data = {'q': title}
    r = requests.post(url, data=data)
    books = r.json()['area']
    result = {}
    for book in books:
        key = book['href']
        result[key] = {}
        result[key]['title'] = book['title']
        if key in view_snapshot:
            result[key]['chapter'] = view_snapshot[key]['chapter']
            result[key]['page'] = view_snapshot[key]['page']
    return result

@eel.expose
def snapshot():
    return view_snapshot

@eel.expose
def chapters(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.find_all('a', {'class': 'chapterLink'})
    if len(links) > 1 and links[0]['title'] > links[1]['title']:
        links = reversed(links)
    
    return [{'title': link['title'], 'url': link['href']} for link in links]

@eel.expose
def pages(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find_all('img', {'class': 'viewPng'})
    return [img.attrs.get('data-src') for img in imgs]

@eel.expose
def view(comic_url, title, chapter_url, page):
    view_snapshot[comic_url] = {
        'title': title,
        'chapter': chapter_url,
        'page': page
    }
    with open(view_snapshot_file, 'w', encoding='UTF-8-sig') as outfile:  
        json.dump(view_snapshot, outfile, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    with open(view_snapshot_file, encoding='UTF-8-sig') as json_file:  
        view_snapshot = json.load(json_file)

    web_app_options = {
        'mode': "chrome-app", #or "chrome"
        'port': 5555,
        'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
    }

    # eel.start('index.html', options=web_app_options)    # Start
    eel.start('index.html')    # Start