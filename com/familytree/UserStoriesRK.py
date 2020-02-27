from datetime import datetime, timedelta
from TreeLine import TreeLine
from TreeUtils import TreeUtils


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

        if indi_list_us03:
            TreeUtils.print_report("US03 Birth before death", indi_list_us03)
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

        if indi_list_us04:
            TreeUtils.print_report("US04 Marriage before divorce", indi_list_us04)
        return indi_list_us04

    def get_id_list(self, obj_list):
        """ Returns id of family or individual"""
        id_list = []
        if obj_list:
            for obj in obj_list:
                id_list.append(obj.id)
        return id_list

    # def print_list(self, list_name, list):
    #     print(f'\n******************** {list_name} ********************')
    #     for item in list:
    #         print(item)

if __name__ == '__main__':
    usrk = UserStoriesRK()
    usrk.us03()
    usrk.us04()
    # usrk.print_list('US 03', usrk.us03())
    # usrk.print_list('US 04', usrk.us04())


