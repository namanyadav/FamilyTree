import os
import sys
import traceback

from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils, get_data_file_path
from com.familytree.stories.UserStoriesAm import UserStoriesAm
from com.familytree.stories.UserStoriesDg import UserStoriesDg
from com.familytree.stories.UserStoriesMSK import UserStoriesMSK
from com.familytree.stories.UserStoriesNy import UserStoriesNy
from com.familytree.stories.UserStoriesRK import UserStoriesRK


class Sprint:

    logger = TreeUtils.get_logger()

    @staticmethod
    def run_sprint1():
        error_list = []
        fp = get_data_file_path('data_sprint_1.ged')
        Sprint.logger.error('######################################## starting sprint 1 ... ########################################')
        try:
            tree = Tree().grow(fp).pretty_print()
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
        Sprint.logger.error('######################################## ending sprint 1 ... ########################################\n')

    @staticmethod
    def run_sprint2():
        error_list = []
        fp = get_data_file_path('data_sprint_2.ged')
        Sprint.logger.error('######################################## starting sprint 2 ... ########################################')
        try:

            Tree().grow(fp).pretty_print()
            usny, usmsk, usam, usdg, usrk = UserStoriesNy(), UserStoriesMSK(), UserStoriesAm(), UserStoriesDg(), UserStoriesRK()
            error_list.extend(usny.us13(fp))
            error_list.extend(usny.us19(fp))
            error_list.extend(usdg.us15(fp))
            error_list.extend(usdg.us12(fp))
            error_list.extend(usrk.us14(fp))
            error_list.extend(usrk.us21(fp))
            error_list.extend(usam.us11(fp))
            error_list.extend(usam.us16(fp))
            error_list.extend(usmsk.us17(fp))
            error_list.extend(usmsk.us18(fp))
            TreeUtils.print_report('Sprint 2 Report', error_list)
        except FileNotFoundError:
            print(f'File not found: {fp}')
        Sprint.logger.error('######################################## ending sprint 2 ... ########################################\n')

    @staticmethod
    def run_sprint3():
        error_list = []
        fp = get_data_file_path('data_sprint_3.ged')
        Sprint.logger.error('######################################## starting sprint 3 ... ########################################')
        Tree().grow(fp).pretty_print()
        usny, usmsk, usam, usdg, usrk = UserStoriesNy(), UserStoriesMSK(), UserStoriesAm(), UserStoriesDg(), UserStoriesRK()
        error_list.extend(usny.us22(fp))
        error_list.extend(usny.us26(fp))
        usrk.us28(fp)
        usrk.us29(fp)
        usam.us27(fp)
        usam.us30(fp)
        error_list.extend(usdg.us23(fp))
        error_list.extend(usdg.us25(fp))
        error_list.extend(usmsk.us20(fp))
        error_list.extend(usmsk.us31(fp))
        TreeUtils.print_report('Sprint 3 Report', error_list)
        Sprint.logger.error('######################################## ending sprint 3 ... ########################################\n')

    @staticmethod
    def run_sprint4():
        error_list = []
        fp = get_data_file_path('data_sprint_4.ged')
        Sprint.logger.error(
            '######################################## starting sprint 4 ... ########################################')
        Tree().grow(fp).pretty_print()
        usny, usmsk, usam, usdg, usrk = UserStoriesNy(), UserStoriesMSK(), UserStoriesAm(), UserStoriesDg(), UserStoriesRK()
        error_list.extend(usny.us37(fp))
        error_list.extend(usny.us40(fp))
        error_list.extend(usdg.us33(fp))
        error_list.extend(usdg.us35(fp))
        TreeUtils.print_report('Sprint 4 Report', error_list)
        Sprint.logger.error(
            '######################################## ending sprint 4 ... ########################################\n')

    @staticmethod
    def run_sprint_test():
        usny = UserStoriesNy()
        error_list = usny.us37()
        TreeUtils.print_report('Sprint 4 Report', error_list)
        # error_list = []
        # # fp = os.path.join(os.path.realpath('.'), 'com', 'familytree', 'data', 'us10.ged')
        # fp = get_data_file_path('us26.ged')
        # try:
        #     family_tree = Tree().grow(fp)
        #     family_tree.pretty_print()
        #     error_list.extend(UserStoriesNy().us26(fp))
        #     TreeUtils.print_report('US 26', error_list)
        # except FileNotFoundError:
        #     print(f'File not found: {fp}')
        # except Exception as e:
        #     # print(f'Exception occurred: {str(e)}')
        #     # e.print_exception()
        #     traceback.print_exc(file=sys.stderr)
        #     # track = traceback.format_exc()
        #     # print(track)


if __name__ == '__main__':
    Sprint.run_sprint1()
    Sprint.run_sprint2()
    Sprint.run_sprint3()
