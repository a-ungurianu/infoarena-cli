from .utils import get_soup_from_url,ROOT_URL
from .task import Task

ARCHIVE_URLS = {
    "problems": ROOT_URL + "/arhiva",
    "educational": ROOT_URL + "/arhiva-educationala",
    "monthly": ROOT_URL + "/arhiva-monthly",
    "acm": ROOT_URL + "/arhiva-acm"
}

class TaskList(object):
    def __init__(self,list_url):
        self.url = list_url+"?display_entries={count}&first_entry={start}"
        self.tasks = []

    def get_tasks(self,start,count):
        slice_url = self.url.format(count=count,start=start)
        page_soup = get_soup_from_url(slice_url)

        task_table = page_soup.find(class_="tasks")

        tasks = []
        for row in task_table.find("tbody").findAll("tr"):
            id = int(row.find(class_="number").get_text(),10)
            name = row.find(class_="task").find("a")["href"].split("/")[-1]
            tasks.append(Task(name))

        return tasks
