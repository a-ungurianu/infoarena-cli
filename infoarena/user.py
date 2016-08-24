from .utils import ROOT_URL,get_soup_from_url
import re

USER_ROOT = ROOT_URL + "/utilizator/{user}?action=stats"

class User(object):
    def __init__(self,username):
        self.username = username

    def _retrieve_data(self):
        soup = get_soup_from_url(USER_ROOT.format(user=self.username))

        badge_soup = soup.find(class_="compact")

        self.name = badge_soup.tr.findAll("td")[1].get_text().strip()

        self.rating = int(badge_soup.findAll("tr")[2].td.get_text().strip())

        stats_section = soup.findAll(class_="wiki_text_block")[2]

        all_problem_links = stats_section.findAll("a",href=re.compile(r"/problema/(.+)"))

        all_problems = set(a.get_text().strip() for a in all_problem_links)

        tried_problems_header = stats_section.find("h3",text="Probleme incercate")


        tried_problems = set()

        for span in tried_problems_header.find_next_siblings("span"):
            links = span.findAll("a",href=re.compile(r"/problema/(.+)"))
            problems = set(a.get_text().strip() for a in links)
            tried_problems.update(problems)

        solved_problems = all_problems - tried_problems

        print(solved_problems)
        print()
        print(tried_problems)

        # for tag in solved_problems_header.find_next_siblings():
        #     if tag == tried_problems_header:
        #         break
        #
        #     all_anchors = tag.findAll("a",href=re.compile("/problema/"))
        #
        #     if all_anchors != []:
