from bs4 import BeautifulSoup
import requests
from .utils import USER_AGENT
from .task import Task
from .tasklist import TaskList
from .user import User


class IASession(object):

    def _login_session(self,username,password):
        """
        This uses the provided user and password to authenticate the current session.
        """
        login_data = {"username":username,"password":password}

        response = self.session.post("https://infoarena.ro/login",data=login_data).text

        login_soup = BeautifulSoup(response,"lxml")

        page_title = login_soup.title

        if "Auten" in page_title.text:
            raise Exception("Login error, credentials invalid")

    def __init__(self,username=None,password=None):
        self.username = username
        self.session = requests.Session()
        self.session.headers.update({"User-Agent":USER_AGENT})

        if username != None and password != None:
            self._login_session(username,password)

    def get_soup_from_url(self,url):
        response = self.session.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        return soup

    def get_task(self,task_id):
        return Task(task_id,self)

    def get_user(self,username):
        return User(username,self)

    def get_tasklist(self,taskUrl):
        return TaskList(taskUrl,self)
