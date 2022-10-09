# https://pt.teamlyzer.com/companies/?page=1
import logging
from unicodedata import name
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os.path
import re

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[], page = 1):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.page = page

    def download_url(self, url):
        return requests.get(url).text

    def get_names(self, url, html):
        names = []
        images = []
        urls = []
        soup = BeautifulSoup(html, 'html.parser')
        for h3 in soup.find_all("h3", {"class": "voffset0"}):
            for a in h3.find_all('a'):
                names.append(a.string)
                companie_url = 'https://pt.teamlyzer.com%s'% (a['href'])
                urls.append(companie_url)
        for img in soup.find_all("img", {"class": "img-responsive img-thumbnail"}):
            img_url = 'https://pt.teamlyzer.com%s'% (img['src'])
            images.append(img_url)
        return [names, images, urls]

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        script_dir = os.path.dirname(__file__)
        script_dir = script_dir + "/files/"
        try: 
            os.mkdir(script_dir) 
        except OSError as error: 
            pass

        for name in self.get_names(url, html)[0]:
            file_path = os.path.join(script_dir, 'names.txt')
            with open(file_path, "a") as text_file:
                text_file.write("%s \n" % (name.strip()))

        for image in self.get_names(url, html)[1]:
            file_path = os.path.join(script_dir, 'images.txt')
            with open(file_path, "a") as text_file:
                text_file.write("%s \n" % (image))
        
        for url in self.get_names(url, html)[2]:
            file_path = os.path.join(script_dir, 'urls.txt')
            with open(file_path, "a") as text_file:
                text_file.write("%s \n" % (url))
    
        self.page = self.page + 1
        url="{}{}".format('https://pt.teamlyzer.com/companies/?page=', self.page)
        self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(urls=['https://pt.teamlyzer.com/companies/?page=1'], page=1).run()