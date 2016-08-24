from .utils import ROOT_URL,get_soup_from_url
import re

PROBLEM_ROOT_URL = ROOT_URL + "/problema"

class Task(object):
    def __init__(self,name):
        self.name = name
        self.data_retrieved = False

    def get_description(self):
        if not self.data_retrieved:
            self.retrieve_data()
        return self.description

    def get_title(self):
        if not self.data_retrieved:
            self.retrieve_data()
        return self.title

    def get_input_description(self):
        if not self.data_retrieved:
            self.retrieve_data()
        return self.input_description


    def retrieve_data(self):
        url = PROBLEM_ROOT_URL + "/" + self.name
        page = get_soup_from_url(url)

        problem_data_block = page.find(id="main").find(class_="wiki_text_block")

        problem_header = problem_data_block.h1
        self.title = problem_header.get_text().strip()

        problem_restriction_row = problem_data_block.table.findAll("tr")[2].findAll("td")

        self.time_limit = problem_restriction_row[1].get_text().strip()
        self.memory_limit = problem_restriction_row[3].get_text().strip()

        # Next sibling is called twice because the whitespace between them is considered as a tag
        input_paragraph = problem_data_block.find("h2",text=re.compile("Date de in")).next_sibling.next_sibling
        self.input_description = input_paragraph.get_text().strip()
        output_paragraph = problem_data_block.find("h2",text=re.compile("Date de ie")).next_sibling.next_sibling
        self.output_description = output_paragraph.get_text().strip()

        self.description = ""
        for paragraph in problem_header.find_next_siblings("p"):
            if paragraph == input_paragraph:
                break

            maybe_para_header = paragraph.previous_sibling.previous_sibling
            if maybe_para_header.name == "h2":
                self.description += "\n" + maybe_para_header.get_text() + "\n\n"
            self.description += paragraph.get_text().strip() + "\n"

        self.data_retrieved = True
