from bs4 import BeautifulSoup
import urllib.request

USER_AGENT = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"

def get_soup_from_url(url):
    request = urllib.request.Request(url,headers={"User-Agent":USER_AGENT})
    html_doc = urllib.request.urlopen(request)
    html_doc = html_doc.read()

    soup = BeautifulSoup(html_doc,'html.parser')
    return soup
