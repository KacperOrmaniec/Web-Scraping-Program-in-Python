import os
import time
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

PROXY = os.getenv('PROXY')
INPUT_URL = os.getenv('INPUT_URL')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')

BASE_URL = 'http://quotes.toscrape.com'
DELAY = 20

session = requests.Session()
session.proxies = {'http': 'http://' + PROXY, 'https': 'https://' + PROXY}


def scrape_quotes(url):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    quotes = soup.select('.quote')

    scraped_data = []
    for quote in quotes:
        text = quote.select_one('span.text').get_text(strip=True)
        author = quote.select_one('.author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
        scraped_data.append({'text': text, 'by': author, 'tags': tags})

    return scraped_data


def main():
    page_url = INPUT_URL
    all_quotes = []

    while page_url:
        quotes = scrape_quotes(page_url)
        all_quotes.extend(quotes)

        next_page = BeautifulSoup(session.get(page_url).content, 'html.parser').select_one('.next a')
        if next_page:
            page_url = BASE_URL + next_page['href']
        else:
            page_url = None

        time.sleep(DELAY)

    with open(OUTPUT_FILE, 'w') as file:
        for quote in all_quotes:
            file.write(json.dumps(quote) + '\n')


if __name__ == '__main__':
    main()