import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from infoarena import user,tasklist
from infoarena.session import IASession, IAAuthSession

# These are tests to check if the output of stuff is the same if logged in or not.


username = None
password = None

class TestLoginDoesntDiffer(unittest.TestCase):
    def setUp(self):
        self.logged_in_sess = IAAuthSession(username,password)
        self.not_logged_in_sess = IASession()

    def test_is_user_same(self):
        username_to_test = "darren"

        log_user = self.logged_in_sess.get_user(username_to_test)
        def_user = self.not_logged_in_sess.get_user(username_to_test)

        self.assertEqual(log_user.name,def_user.name, "Different names")
        self.assertEqual(log_user.rating,def_user.rating, "Different ratings")
        self.assertEqual(sorted(map(lambda task:task.name,log_user.tried_tasks)),
                         sorted(map(lambda task:task.name,def_user.tried_tasks)),
                         "Different tried tasks")
        self.assertEqual(sorted(map(lambda task:task.name,log_user.solved_tasks)),
                         sorted(map(lambda task:task.name,def_user.solved_tasks)),
                         "Differnet solved tasks")

    def test_is_task_same(self):
        task_to_test = "bfs"

        log_task = self.logged_in_sess.get_task(task_to_test)
        def_task = self.not_logged_in_sess.get_task(task_to_test)

        self.assertEqual(log_task.description,def_task.description, "Description differs")
        self.assertEqual(log_task.title, def_task.title, "Title differs")
        self.assertEqual(log_task.input_description,def_task.input_description, "Input description differs")
        self.assertEqual(log_task.output_description,def_task.output_description, "Output description differs")


    def test_is_task_list_same(self):
        log_list = self.logged_in_sess.get_tasklist(tasklist.TaskListURL.PROBLEMS)
        def_list = self.not_logged_in_sess.get_tasklist(tasklist.TaskListURL.PROBLEMS)

        logged_tasks = sorted(map(lambda task:task.name,log_list.get_tasks(0,20)))
        def_tasks = sorted(map(lambda task:task.name,def_list.get_tasks(0,20)))

        self.assertEqual(logged_tasks,def_tasks)

if __name__ == "__main__":
    username = input("Enter username to test: ")
    password = input("Enter password to test: ")
    unittest.main()
