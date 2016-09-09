from .utils import ROOT_URL,get_soup_from_url
from .task import Task
import re

USER_ROOT = ROOT_URL + "/utilizator/{user}?action=stats"

class User(object):
    """
    This is an object that holds data about an user.
    The user is selected using its username.
    The data is loaded lazily, so there is no network cost for initializing
    Users, just for retrieving specific data.
    """

    def __init__(self,username,session):
        self.session = session
        self.username = username

    @property
    def name(self):
        if not hasattr(self,"_name"):
            self._retrieve_data()
        return self._name

    @name.setter
    def name(self,name):
        self._name = name

    @property
    def rating(self):
        if not hasattr(self,"_rating"):
            self._retrieve_data()
        return self._rating

    @rating.setter
    def rating(self,rating):
        self._rating = rating

    @property
    def solved_tasks(self):
        if not hasattr(self,"_solved_tasks"):
            self._retrieve_data()
        return self._solved_tasks

    @property
    def tried_tasks(self):
        if not hasattr(self,"_tried_tasks"):
            self._retrieve_data()
        return self._tried_tasks

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<User name={name}>".format(name=self.username)

    def _retrieve_data(self):
        """ This function does most of the work, retrieving data from the site. """
        # Retrieve the soup of the user page
        soup = self.session.get_soup_from_url(USER_ROOT.format(user=self.username))

        # Find the user badge that each account page has and retrieve relevant
        # information from there
        badge_soup = soup.find(class_="compact")

        self._name = badge_soup.tr.findAll("td")[1].get_text().strip()

        self._rating = int(badge_soup.findAll("tr")[2].td.get_text().strip())


        # This is the bottom section of the user page, which contains the tasks
        # solved by this user
        stats_section = soup.findAll(class_="wiki_text_block")[2]

        # We know that all the tasks in the lists are hyperlinks so we can just
        # find all the hyperlinks that match the problem url
        all_problem_links = stats_section.findAll("a",href=re.compile(r"/problema/(.+)"))

        # Retrive the problem id from the url
        all_problems = set(a.get_text().strip() for a in all_problem_links)

        # Due to how the page is designed, there is no clean separation between
        # the tried problems and the solved problems.
        # So the only thing we can do is to get everything below the tried problems
        # header.
        tried_problems_header = stats_section.find("h3",text="Probleme incercate")

        tried_problems = set()

        # Find all next siblings is not recursive by definition so we have to apply
        # the task id finding algorithm to each span below the header
        for span in tried_problems_header.find_next_siblings("span"):
            links = span.findAll("a",href=re.compile(r"/problema/(.+)"))
            problems = set(a.get_text().strip() for a in links)
            tried_problems.update(problems)

        # Knowing that problems are either in the solved set or the tried set,
        # we can just set-difference all_problems and tried_problems to get the
        # solved ones
        solved_problems = all_problems - tried_problems

        # Construct Task objects for each tasks and assign them to our object
        self._solved_tasks = list(map(lambda task_name: Task(task_name,self.session),solved_problems))
        self._tried_tasks = list(map(lambda task_name: Task(task_name,self.session),tried_problems))
