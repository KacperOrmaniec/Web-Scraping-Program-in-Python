import os #Żeby odczytać dane z env
import time #sekundy w delay
import json #zapisywanie yield w json
from bs4 import BeautifulSoup #Webscraping
from dotenv import load_dotenv #aby odczytać env
from selenium import webdriver #Rozwiązanie na Javascript delay

#ładowanie oraz przypisywanie parametrów
load_dotenv()

INPUT_URL = os.getenv('INPUT_URL')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')

BASE_URL = 'http://quotes.toscrape.com' #Url bez js-delay w celu testów
DELAY = 10  # Delay w sekundach podczas otwierania nowej strony

session = None #selenium

def init_session():
    global session
    session = webdriver.Chrome()

def scrape_quotes(url):
    session.get(url)
    time.sleep(15)  #Czekanie na opóźnienie JS
    soup = BeautifulSoup(session.page_source, 'html.parser')
    quotes = soup.select('.quote') #ekstraktowanie z html za pomocą soup

    scraped_data = [] #Array w celu zbierania tekstu, autorów, tagów
    for quote in quotes: #for loop żeby tekst, auto, tag był obok siebie
        text = quote.select_one('span.text').get_text(strip=True).replace('\u201c', '').replace('\u201d', '').replace('\u2023', '').replace('\u2019', '')
        #.replace ponieważ w wyniku pojawiło się \u201c oraz \u201d
        author = quote.select_one('.author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
        scraped_data.append({'text': text, 'by': author, 'tags': tags}) #Dodawanie wyniku do array

    return scraped_data

def main(): #Funkcja
    init_session() #inicjuje przeglądarkę
    page_url = INPUT_URL
    all_quotes = [] #Przechowywanie zyskanych cytatów

    while page_url: #While loop dopóki nie dojdziemy do ostatniej strony
        quotes = scrape_quotes(page_url)
        all_quotes.extend(quotes)

# sprawdzanie czy jest następna strona
        next_page = BeautifulSoup(session.page_source, 'html.parser').select_one('.next a')
        if next_page:
            page_url = BASE_URL + next_page['href']
        else:
            page_url = None

        time.sleep(DELAY) #Dodatkowy delay

    session.quit() #zamykanie przeglądarki

    with open(OUTPUT_FILE, 'w') as file: #zapisywanie w json
        for quote in all_quotes:
            json.dump(quote, file, ensure_ascii=False, indent=4) #poprawny format
            file.write('\n')

if __name__ == '__main__': #call funkcji
    main()