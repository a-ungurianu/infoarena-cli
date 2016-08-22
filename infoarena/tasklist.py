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
        if len(self.tasks) >= start+count and self.tasks[start] is not None and self.tasks[start+count-1] is not None:
            return self.tasks[start:start+count]
        else:
            self._retrieve_task_segment(start,count)

    def _retrieve_task_segment(self,start,count):
        slice_url = self.url.format(count=count,start=start)
        page_soup = get_soup_from_url(slice_url)

        task_table = page_soup.find(class_="tasks")

        for row in task_table.find("tbody").findAll("tr"):
            id = int(row.find(class_="number").get_text(),10)
            name = row.find(class_="task").find("a")["href"].split("/")[-1]
            self.tasks[id] = Task(name)
