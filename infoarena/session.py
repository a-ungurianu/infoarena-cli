from bs4 import BeautifulSoup
import requests
from .utils import USER_AGENT


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

    def __init__(self,username,password):
        self.username = username
        self.session = requests.Session()
        self.session.headers.update({"User-Agent":USER_AGENT})

        if username != None and password != None:
            self._login_session(username,password)
