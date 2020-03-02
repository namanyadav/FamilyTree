import os
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import TreeUtils
from com.familytree.stories.UserStoriesAm import UserStoriesAm
from com.familytree.stories.UserStoriesDg import UserStoriesDg
from com.familytree.stories.UserStoriesMSK import UserStoriesMSK
from com.familytree.stories.UserStoriesNy import UserStoriesNy
from com.familytree.stories.UserStoriesRK import UserStoriesRK

class Sprint:

    @staticmethod
    def run_sprint1():
        error_list = []
        fp = os.path.join(os.path.realpath('.'), 'com', 'familytree', 'data', 'Familytree_gedcom_yadav.ged')
        tree_line = TreeLine()
        tree_line.tabulate(tree_line.process_data(fp))
        usny, usmsk, usam, usdg, usrk = UserStoriesNy(), UserStoriesMSK(), UserStoriesAm(), UserStoriesDg(), UserStoriesRK()
        error_list.extend(usmsk.us09(fp))
        error_list.extend(usmsk.us10(fp))
        error_list.extend(usny.us01(fp))
        error_list.extend(usny.us08(fp))
        error_list.extend(usam.us02(fp))
        error_list.extend(usam.us06(fp))
        error_list.extend(usdg.us05(fp))
        error_list.extend(usdg.us07(fp))
        error_list.extend(usrk.us03(fp))
        error_list.extend(usrk.us04(fp))
        TreeUtils.print_report('Sprint 1 Report', error_list)
