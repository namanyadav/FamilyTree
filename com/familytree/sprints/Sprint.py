import os

from com.familytree.TreeUtils import TreeUtils
from com.familytree.stories.UserStoriesMSK import UserStoriesMSK

from com.familytree.stories.UserStoriesNy import UserStoriesNy


class Sprint:

    @staticmethod
    def run_sprint1():
        error_list = []
        fp=os.path.join(os.path.realpath('.'), 'com', 'familytree', 'data', 'Familytree_gedcom_yadav.ged')
        usny = UserStoriesNy()
        usmsk = UserStoriesMSK()
        error_list.extend(usmsk.us09(fp))
        error_list.extend(usmsk.us10(fp))
        error_list.extend(usny.us01(fp))
        error_list.extend(usny.us08(fp))
        TreeUtils.print_report('Sprint 1 Report', error_list)

# if __name__ == '__main__':
