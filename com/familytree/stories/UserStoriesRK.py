from datetime import datetime, timedelta
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import TreeUtils
from com.familytree.Tree import Tree
from com.familytree.TreeError import TreeError

class UserStoriesRK:

    FILE_PATH = '../data/us03&04.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us03(self, file_path=None):
        """Birth before death"""
        file_path = file_path if file_path else UserStoriesRK.FILE_PATH
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesRK.INDI_TAG)
        indi_list_us03 = []
        for indi in indi_list:
            if indi.get_birth_date() and indi.get_death_date() and indi.get_birth_date() >= indi.get_death_date():
                warn_msg = f"Birth {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} should occur before death {indi.get_death_date(Tree.OUTPUT_DATE_FORMAT)}"
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US03', indi.id, warn_msg)
                indi_list_us03.append(indi)
        # if indi_list_us03:
        #     TreeUtils.print_report("US03 Birth before death", indi_list_us03)
        return indi_list_us03

    def us04(self, file_path=None):
        """Marriage after divorce"""
        file_path = file_path if file_path else UserStoriesRK.FILE_PATH
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)
        indi_list_us04 = []
        for fam in fam_list:
            if fam.get_marr_date() and fam.get_div_date() and fam.get_marr_date() >= fam.get_div_date():
                warn_msg = f"Marriage {fam.get_marr_date(Tree.OUTPUT_DATE_FORMAT)} should occur before divorse {fam.get_marr_date(Tree.OUTPUT_DATE_FORMAT)}"
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US04', fam.id, warn_msg)
                indi_list_us04.append(fam)
        # if indi_list_us04:
        #     TreeUtils.print_report("US04 Marriage before divorce", indi_list_us04)
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

# if __name__ == '__main__':
#     usrk = UserStoriesRK()
#     usrk.us03()
#     usrk.us04()
    # usrk.print_list('US 03', usrk.us03())
    # usrk.print_list('US 04', usrk.us04())


