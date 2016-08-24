from bs4 import BeautifulSoup
import requests

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0"

ROOT_URL = "http://www.infoarena.ro"


def get_soup_from_url(url):
    response = requests.get(url,headers={"User-Agent":USER_AGENT})
    soup = BeautifulSoup(response.text,'lxml')
    return soup
