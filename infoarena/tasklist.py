from .utils import get_soup_from_url,ROOT_URL
from .task import Task

from enum import Enum

class TaskListURL(Enum):
    PROBLEMS = ROOT_URL + "/arhiva"
    EDUCATIONAL = ROOT_URL + "/arhiva-educationala"
    MONTHLY = ROOT_URL + "/arhiva-monthly"
    ACM = ROOT_URL + "/arhiva-acm"


class TaskList(object):
    """
    The website contains 4 problem lists. This class is used to interface with
    those lists.
    The list is initialized using the url that points to it on the site.
    """
    def __init__(self,list_url,session):
        self.session = session
        self.url = list_url.value+"?display_entries={count}&first_entry={start}"
        self.tasks = []

    def get_tasks(self,start,count):
        """ Gets `count` tasks from the list, starting from id `start` """
        slice_url = self.url.format(count=count,start=start)
        page_soup = self.session.get_soup_from_url(slice_url)

        task_table = page_soup.find(class_="tasks")

        tasks = []
        for row in task_table.find("tbody").findAll("tr"):
            id = int(row.find(class_="number").get_text(),10)
            link = row.find(class_="task").find("a")
            name = link["href"].split("/")[-1]
            # The task table already contains the title of the task, so might
            # as well initialize it.
            new_task = self.session.get_task(name)
            new_task.title = link.get_text().strip()
            tasks.append(new_task)

        return tasks

class AuthTaskList(TaskList):
    pass
