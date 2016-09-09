from bs4 import BeautifulSoup
import requests
ROOT_URL = "http://www.infoarena.ro"

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent":USER_AGENT})

def get_soup_from_url(url):
    response = SESSION.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    return soup
