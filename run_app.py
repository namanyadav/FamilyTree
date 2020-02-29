from com.familytree.sprints.Sprint import Sprint
from com.familytree.stories.UserStoriesNy import UserStoriesNy
import os
from os import sys, path

# sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# print(sys.executable)
# print(os.getcwd())
# print(sys.path)
us = UserStoriesNy()
# us.us01(r"C:\Users\naman\PycharmProjects\CS-555\com\familytree\data\us01.ged")
# us.us08(r"C:\Users\naman\PycharmProjects\CS-555\com\familytree\data\us08.ged")
# us.log()
Sprint.run_sprint1()
