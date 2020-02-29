from datetime import datetime, timedelta
from TreeLine import TreeLine
import calendar


class UserStoriesRK:

    FILE_PATH = './com/familytree/data/us03&04.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'
    # file_path = './com/familytree/us03&04.ged'

    def us03(self):
        """Birth before death"""

        processed_tree = TreeLine().process_data(UserStoriesRK.FILE_PATH)
        indi_list = processed_tree.get_sorted_list(UserStoriesRK.INDI_TAG)
        indi_list_us03 = []

        for indi in indi_list:
            if indi.get_birth_date() and indi.get_death_date() and indi.get_birth_date() > indi.get_death_date():
                indi.warn_msg = "Birth should occur before death"
                indi_list_us03.append(indi)

        return indi_list_us03

    def us04(self):
        """Marriage after divorce"""
        processed_tree = TreeLine().process_data(UserStoriesRK.FILE_PATH)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)

        indi_list_us04 = []

        for fam in fam_list:
            if fam.get_marr_date() and fam.get_div_date() and fam.get_marr_date() > fam.get_div_date():
                fam.warn_msg = "Marriage should occur before divorse"
                indi_list_us04.append(fam)

        return indi_list_us04

    def print_list(self, list_name, list):
        print(f'\n******************** {list_name} ********************')
        for item in list:
            print(item)

if __name__ == '__main__':
    usrk = UserStoriesRK()
    usrk.print_list('US 03', usrk.us03())
    usrk.print_list('US 04', usrk.us04())


