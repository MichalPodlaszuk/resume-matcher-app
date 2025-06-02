import requests
from bs4 import BeautifulSoup


def extract_text_from_indeed(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    soup_text="\n".join([",".join([tag.name, tag.get_text()]) for tag in soup.find_all()])
    print(soup_text)
    job_text = "\n".join([tag.get_text(strip=True) for tag in soup.find_all('li')])
    return job_text

extract_text_from_indeed("https://pl.indeed.com/q-junior-python-oferty-pracy.html?vjk=36a0eaaee543b83f")