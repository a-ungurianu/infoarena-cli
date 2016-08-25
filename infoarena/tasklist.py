from .utils import get_soup_from_url,ROOT_URL
from .task import Task

ARCHIVE_URLS = {
    "problems": ROOT_URL + "/arhiva",
    "educational": ROOT_URL + "/arhiva-educationala",
    "monthly": ROOT_URL + "/arhiva-monthly",
    "acm": ROOT_URL + "/arhiva-acm"
}

class TaskList(object):
    """
    The website contains 4 problem lists. This class is used to interface with
    those lists.
    The list is initialized using the url that points to it on the site.
    """
    def __init__(self,list_url):
        self.url = list_url+"?display_entries={count}&first_entry={start}"
        self.tasks = []

    def get_tasks(self,start,count):
        """ Gets `count` tasks from the list, starting from id `start` """
        slice_url = self.url.format(count=count,start=start)
        page_soup = get_soup_from_url(slice_url)

        task_table = page_soup.find(class_="tasks")

        tasks = []
        for row in task_table.find("tbody").findAll("tr"):
            id = int(row.find(class_="number").get_text(),10)
            link = row.find(class_="task").find("a")
            name = link["href"].split("/")[-1]
            # The task table already contains the title of the task, so might
            # as well initialize it.
            new_task = Task(name)
            new_task.title = link.get_text().strip()
            tasks.append(new_task)

        return tasks

# Task lists are not likely to change, so objects for each of them are already
# constructed.
EducationalTaskList = TaskList(ARCHIVE_URLS["educational"])
ProblemTaskList = TaskList(ARCHIVE_URLS["problems"])
MonthlyTaskList = TaskList(ARCHIVE_URLS["monthly"])
ACMTaskList = TaskList(ARCHIVE_URLS["acm"])
