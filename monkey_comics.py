import requests
from bs4 import BeautifulSoup
import json
import re
import zipfile
import os

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

def snapshot():
    with open(view_snapshot_file, encoding='UTF-8-sig') as json_file:  
        view_snapshot = json.load(json_file)
    return view_snapshot

def chapters(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.find_all('a', {'class': 'chapterLink'})
    if len(links) > 1 and links[0]['title'] > links[1]['title']:
        links = reversed(links)
    
    return [{'title': link['title'], 'url': link['href']} for link in links]

def pages(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find_all('img', {'class': 'viewPng'})
    return [img.attrs.get('data-src') for img in imgs]

def view(comic_url, title, chapter_url, page):
    view_snapshot[comic_url] = {
        'title': title,
        'chapter': chapter_url,
        'page': page
    }
    with open(view_snapshot_file, 'w', encoding='UTF-8-sig') as outfile:  
        json.dump(view_snapshot, outfile, indent=2, ensure_ascii=False)

def download(title, chapter_url):
    imgs = pages(chapter_url)
    zip_file = zipfile.ZipFile(title + '.zip', 'w')
    for i, img in enumerate(imgs):
        ext = img.split('.')[-1]
        r = requests.get(img, stream=True)
        file_name = '{}_{:03d}.{}'.format(title, i, ext)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        zip_file.write(file_name, compress_type=zipfile.ZIP_DEFLATED)
        os.remove(file_name)

    zip_file.close()
        
