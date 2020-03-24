from datetime import datetime, timedelta
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import TreeUtils, get_data_file_path
from com.familytree.Tree import Tree
from com.familytree.TreeError import TreeError
from collections import defaultdict

class UserStoriesRK:

    FILE_PATH = '../data/us03&04.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us03(self, file_path=None):
        """Birth before death"""
        file_path = file_path if file_path else get_data_file_path('us03&04.ged')
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesRK.INDI_TAG)
        indi_list_us03 = []
        for indi in indi_list:
            if indi.get_birth_date() and indi.get_death_date() and indi.get_birth_date() >= indi.get_death_date():
                warn_msg = f"Birth {indi.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)} should occur before death {indi.get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)}"
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US03', indi.id, warn_msg)
                indi_list_us03.append(indi)
        # if indi_list_us03:
        #     TreeUtils.print_report("US03 Birth before death", indi_list_us03)
        return indi_list_us03

    def us04(self, file_path=None):
        """Marriage after divorce"""
        file_path = file_path if file_path else get_data_file_path('us03&04.ged')
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)
        indi_list_us04 = []
        for fam in fam_list:
            if fam.get_marr_date() and fam.get_div_date() and fam.get_marr_date() >= fam.get_div_date():
                warn_msg = f"Marriage {fam.get_marr_date(TreeUtils.OUTPUT_DATE_FORMAT)} should occur before divorse {fam.get_div_date(TreeUtils.OUTPUT_DATE_FORMAT)}"
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US04', fam.id, warn_msg)
                indi_list_us04.append(fam)
        # if indi_list_us04:
        #     TreeUtils.print_report("US04 Marriage before divorce", indi_list_us04)
        return indi_list_us04

    def us14(self, file_path=None):
        """ Multiple births <= 5"""
        file_path = file_path if file_path else get_data_file_path('US14.ged')
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)
        fail_list_us14 = []
        for fam in fam_list:
            if len(fam.chil) > 5:
                fail_dict = defaultdict(int)
                for child in fam.chil:
                    birthdate = processed_tree.get(child).get_birth_date()
                    if birthdate:
                        fail_dict[birthdate] += 1
                for key in fail_dict.keys():
                    if fail_dict[key] > 5:
                        warn_msg = f"No more than five siblings should be born at the same time"
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US14', fam.id, warn_msg)
                        fail_list_us14.append(fam)
        return fail_list_us14

    def us21(self, file_path=None):
        """Husband in family should be male and wife in family should be female"""
        file_path = file_path if file_path else get_data_file_path('US14.ged')
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)
        fail_list_us21 = []
        for fam in fam_list:
            if processed_tree.get(fam.husb).sex != 'M' or processed_tree.get(fam.wife).sex != 'F':
                if processed_tree.get(fam.husb).sex != 'M' and processed_tree.get(fam.wife).sex != 'F':
                    warn_msg = f"Husband - {processed_tree.get(fam.husb).name} in family should be male and wife - {processed_tree.get(fam.wife).name} in family should be female"
                elif processed_tree.get(fam.husb).sex != 'M':
                    warn_msg = f"Husband - {processed_tree.get(fam.husb).name} in family should be male"
                else:
                    warn_msg = f"Wife - {processed_tree.get(fam.wife).name} in family should be female"
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US21', fam.id, warn_msg)
                fail_list_us21.append(fam)
        return fail_list_us21
                        
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


