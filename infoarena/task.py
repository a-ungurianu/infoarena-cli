from bs4 import BeautifulSoup
import urllib.request
import re

ROOT_URL = "http://www.infoarena.ro"
ARCHIVE_URL = ROOT_URL + "/arhiva"

PROBLEM_ROOT_URL = ROOT_URL + "/problema"

USER_AGENT = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"

def get_soup_from_url(url):
    request = urllib.request.Request(url,headers={"User-Agent":USER_AGENT})
    html_doc = urllib.request.urlopen(request)
    html_doc = html_doc.read()

    soup = BeautifulSoup(html_doc,'html.parser')
    return soup

class Task(object):
    def __init__(self,name):
        self.name = name
        self.data = None

    def get_description(self):
        if self.data is None:
            self.retrieve_data()
        return self.data["description"]

    def retrieve_data(self):
        url = PROBLEM_ROOT_URL + "/" + self.name
        page = get_soup_from_url(url)
        self.data = {}

        problem_data_block = page.find(id="main").find(class_="wiki_text_block")

        problem_header = problem_data_block.h1
        self.data["title"] = problem_header.get_text().strip()

        problem_restriction_row = problem_data_block.table.findAll("tr")[2].findAll("td")

        self.data["time"] = problem_restriction_row[1].get_text().strip()
        self.data["memory"] = problem_restriction_row[3].get_text().strip()

        input_paragraph = problem_data_block.find("var",text=re.compile(self.name + ".in")).parent
        self.data["input_description"] = input_paragraph.get_text().strip()
        output_paragraph = problem_data_block.find("var",text=re.compile(self.name + ".out")).parent
        self.data["output_description"] = output_paragraph.get_text().strip()

        self.data["description"] = ""
        for paragraph in problem_header.find_next_siblings("p"):
            if paragraph == input_paragraph:
                break
            self.data["description"] += paragraph.get_text().strip() + "\n"
