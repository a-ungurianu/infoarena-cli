from .utils import ROOT_URL,get_soup_from_url
import re

PROBLEM_ROOT_URL = ROOT_URL + "/problema"

class Task(object):
    """
    Contains data for each task.
    Task is identified by id/name (the id used by the site to reference the problem)
    Data is being loaded lazily so object initialization doesn't infer any cost.
    """
    def __init__(self,name,session):
        self.session = session
        self.name = name

    @property
    def description(self):
        """ The general description of the task """
        if not hasattr(self,"_description"):
            self._retrieve_data()
        return self._description

    @property
    def title(self):
        if not hasattr(self,"_title"):
            self._retrieve_data()
        return self._title

    @title.setter
    def title(self,title):
        # The setter is added as we can infer the title from other requests,
        # which might avoid useless data retrieval for this object
        self._title = title

    @property
    def input_description(self):
        """
        The description of the input for this task.
        This usually explains how the data should be read from the input file.
        """
        if not hasattr(self,"_input_description"):
            self._retrieve_data()
        return self._input_description

    @property
    def output_description(self):
        """
        The description of the output of this task.
        This usually explains how the data should be written to the output file.
        """
        if not hasattr(self,"_output_description"):
            self._retrieve_data()
        return self._output_description

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Task name={name}>".format(name=self.name)

    def _retrieve_data(self):
        url = PROBLEM_ROOT_URL + "/" + self.name
        page = self.session.get_soup_from_url(url)

        problem_data_block = page.find(id="main").find(class_="wiki_text_block")

        # Luckly, the only h1 header is the title of the task
        problem_header = problem_data_block.h1
        self._title = problem_header.get_text().strip()

        # Problem restrictions are found at the top table, on the third row
        problem_restriction_row = problem_data_block.table.findAll("tr")[2].findAll("td")

        self._time_limit = problem_restriction_row[1].get_text().strip()
        self._memory_limit = problem_restriction_row[3].get_text().strip()

        # Next sibling is called twice because the whitespace between them is considered as a tag
        input_paragraph = problem_data_block.find("h2",text=re.compile("Date de [iI]n")).next_sibling.next_sibling
        self._input_description = input_paragraph.get_text().strip()
        output_paragraph = problem_data_block.find("h2",text=re.compile("Date de [iI]e")).next_sibling.next_sibling
        self._output_description = output_paragraph.get_text().strip()

        # We assume that everything between the problem title and the input description
        # header is part of the description
        self._description = ""
        for paragraph in problem_header.find_next_siblings("p"):
            if paragraph == input_paragraph:
                break

            # If the paragraph has a header before it, add it as well
            # This shows up in some lengthly problems
            maybe_para_header = paragraph.previous_sibling.previous_sibling
            if maybe_para_header.name == "h2":
                self._description += "\n" + maybe_para_header.get_text() + "\n\n"
            self._description += paragraph.get_text().strip() + "\n"
