from datetime import datetime, timedelta
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import TreeUtils, get_data_file_path
from com.familytree.Tree import Tree
from com.familytree.TreeError import TreeError
from collections import defaultdict
from prettytable import PrettyTable

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
    
    def us29(self, file_path = None):
        """List all deceased individuals in a GEDCOM file"""
        file_path = file_path if file_path else get_data_file_path('us03&04.ged')
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesRK.INDI_TAG)
        indi_deceasedlist_us29 = []
        pt = PrettyTable()
        pt.field_names = ["ID", "Name", "Birth", "Death"]
        hasrows = False
        for indi in indi_list:
            if indi.deat != None:
                hasrows = True
                pt.add_row([indi.id, indi.name, indi.birt, indi.deat])
                indi_deceasedlist_us29.append(indi)
        if hasrows:
            print("US29 - List of all deceased individuals ")    
            print(pt)
        return indi_deceasedlist_us29

    def us28(self, file_path = None):
        """List siblings in families by decreasing age, i.e. oldest siblings first"""
        file_path = file_path if file_path else get_data_file_path("./com/familytree/data/us28.ged")
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)
        pt = PrettyTable()
        pt.field_names = ["Family ID", "siblings"]
        sib_list = []
        fam_list_us28 = []
        hasrows = False
        for fam in fam_list:
            sib_list = fam.chil
            dict1 = defaultdict(list)
            if len(sib_list) != 0:
                for sib in sib_list:
                    if processed_tree.get(sib).get_age():
                        dict1[processed_tree.get(sib).get_age()].append(sib)
                        lst1 = sorted(dict1.keys(), reverse=True)
                        lst2 = []
                for i in lst1:
                    lst2.extend(dict1[i])
                hasrows = True
                pt.add_row([fam.id, lst2])
                fam_list_us28.append(lst2)
        if hasrows:
            print("US28 - List of siblings by decreasing age")
            print(pt)
        return fam_list_us28

    def us32(self, file_path=None):
        """List all multiple births in a GEDCOM file"""
        file_path = file_path if file_path else get_data_file_path('US14.ged')
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)
        fam_list_us32 = []
    
        for fam in fam_list:
            if len(fam.chil) >= 2:
                cnt_dict = defaultdict(int)
                birth_dict = defaultdict(list)
                for child in fam.chil:
                    birthdate = processed_tree.get(child).get_birth_date()
                    if birthdate:
                        cnt_dict[birthdate] += 1
                        birth_dict[birthdate].append(child)
                list_children = ""
                for key in cnt_dict.keys():
                    if cnt_dict[key] >= 2:
                        list_children += str(birth_dict[key])
                if list_children != "":
                    warn_msg = f"Children {list_children} in {fam.id} has multiple births"
                    fam.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_FAM, 'US32', fam.id, warn_msg)
                    fam_list_us32.append(fam)
        return fam_list_us32
                       
    def us24(self, file_path=None):
        """No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file"""
        file_path = file_path if file_path else get_data_file_path('us24.ged')
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesRK.FAM_TAG)
        fam_list_us24 = []
        fam_dict1 = {}
        fam_dict2 = {}
        for fam in fam_list:
            husb_name  = processed_tree.get(fam.husb).name
            wife_name  = processed_tree.get(fam.wife).name
            mrg_dt = fam.get_marr_date(TreeUtils.OUTPUT_DATE_FORMAT)
            print(mrg_dt)
            if husb_name and wife_name and mrg_dt:
                husb_name = husb_name.replace('/', '')
                wife_name = wife_name.replace('/', '')
                if mrg_dt not in fam_dict1:
                    fam_dict1[mrg_dt] = husb_name
                    fam_dict2[mrg_dt] = wife_name
                else:
                    if fam_dict1[mrg_dt] == husb_name and fam_dict2[mrg_dt] == wife_name:
                        warn_msg = f'more than one family with same spouse names {husb_name}, {wife_name} and same marriage date {mrg_dt}'
                        fam.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_FAM, 'US24', fam.id, warn_msg)
                        fam_list_us24.append(fam)
                        continue
                    else:
                        fam_dict1[mrg_dt] = husb_name
                        fam_dict2[mrg_dt] = wife_name
        return fam_list_us24
                        
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


