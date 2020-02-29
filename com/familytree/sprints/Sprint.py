import os

from com.familytree.TreeUtils import TreeUtils
from com.familytree.stories.UserStoriesNy import UserStoriesNy


class Sprint:

    @staticmethod
    def run_sprint1():
        error_list = []
        usny = UserStoriesNy()
        error_list.extend(usny.us01(os.path.join(os.path.realpath('.'), 'com', 'familytree', 'data', 'Familytree_gedcom_yadav.ged')))
        error_list.extend(usny.us08(os.path.join(os.path.realpath('.'), 'com', 'familytree', 'data', 'Familytree_gedcom_yadav.ged')))
        TreeUtils.print_report('Sprint 1 Report', error_list)

# if __name__ == '__main__':
