import requests
from bs4 import BeautifulSoup
import cloudscraper
from serpapi import GoogleSearch


def extract_text_from_indeed(url, api_key):
    params = {
        "engine": "google_jobs_listing",
        "url": url,
        "api_key": api_key
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    return data.get("description")



print(extract_text_from_indeed("https://pl.indeed.com/q-junior-python-oferty-pracy.html?vjk=36a0eaaee543b83f", ))