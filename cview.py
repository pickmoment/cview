import monkey_comics as api

import eel

# Set web files folder and optionally specify which file types to check for eel.expose()
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose
def search(title):
    return api.search(title)

@eel.expose
def snapshot():
    return api.snapshot()

@eel.expose
def chapters(url):
    return api.chapters(url)

@eel.expose
def pages(url):
    return api.pages(url)

@eel.expose
def view(comic_url, title, chapter_url, page):
    api.view(comic_url, title, chapter_url, page)

@eel.expose
def download_chapter(title, chapter_url):
    api.download(title, chapter_url)
        
@eel.expose
def download_book(book_url):
    chaps = api.chapters(book_url)
    for chap in chaps:
        api.download(chap['title'], chap['url'])


if __name__ == '__main__':
    web_app_options = {
        'mode': "chrome-app", #or "chrome"
        'port': 5555,
        'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
    }

    # eel.start('index.html', options=web_app_options)    # Start
    eel.start('index.html')    # Start