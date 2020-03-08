import os
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import TreeUtils, get_data_file_path
from com.familytree.stories.UserStoriesAm import UserStoriesAm
from com.familytree.stories.UserStoriesDg import UserStoriesDg
from com.familytree.stories.UserStoriesMSK import UserStoriesMSK
from com.familytree.stories.UserStoriesNy import UserStoriesNy
from com.familytree.stories.UserStoriesRK import UserStoriesRK

class Sprint:

    @staticmethod
    def run_sprint1():
        error_list = []
        fp = get_data_file_path('Familytree_gedcom_yadav.ged')
        try:
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
        except FileNotFoundError:
            print(f'File not found: {fp}')

    @staticmethod
    def run_sprint2():
        error_list = []
        fp = get_data_file_path('data_sprint_2.ged')
        tree_line = TreeLine()
        tree_line.tabulate(tree_line.process_data(fp))
        usny, usmsk, usam, usdg, usrk = UserStoriesNy(), UserStoriesMSK(), UserStoriesAm(), UserStoriesDg(), UserStoriesRK()
        error_list.extend(usny.us13(get_data_file_path('us13.ged')))
        error_list.extend(usny.us19(get_data_file_path('us19.ged')))
        TreeUtils.print_report('Sprint 2 Report', error_list)

    @staticmethod
    def run_sprint_test():
        error_list = []
        fp = os.path.join(os.path.realpath('.'), 'com', 'familytree', 'data', 'us10.ged')
        try:
            tree_line = TreeLine()
            tree_line.tabulate(tree_line.process_data(fp))
            error_list.extend(UserStoriesMSK().us10(fp))
            TreeUtils.print_report('USMSK', error_list)
        except FileNotFoundError:
            print(f'File not found: {fp}')
        except Exception as e:
            print(f'Exception occurred: {str(e)}')
