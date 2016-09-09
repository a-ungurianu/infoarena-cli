import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from infoarena import user,tasklist
from infoarena.utils import login


login("alexandru70","xTNvBFw35LY7")

first_ten = tasklist.EducationalTaskList.get_tasks(0,10)

for task in first_ten:
    print(task.title)
