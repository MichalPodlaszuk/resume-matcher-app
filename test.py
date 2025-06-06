import requests
from bs4 import BeautifulSoup
import cloudscraper
from serpapi import GoogleSearch


def extract_text_from_indeed(url, api_key):
    scraper = cloudscraper.create_scraper(
        interpreter="nodejs",
        delay=10,
        browser={
            "browser": "chrome",
            "platform": "ios",
            "desktop": False,
        }
    )
    response = scraper.get(url)
    print(response.text)
    return None



print(extract_text_from_indeed("https://pl.indeed.com/q-junior-python-oferty-pracy.html?vjk=36a0eaaee543b83f", "38c08b8eb505aa238569388c83ba797cc47c005f58af2b27335b338afb70ff35"))