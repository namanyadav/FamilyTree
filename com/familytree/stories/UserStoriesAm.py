from datetime import datetime, timedelta
from collections import defaultdict
from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils, get_data_file_path
from prettytable import PrettyTable



class UserStoriesAm:

    FILE_PATH = '../data/Familytree_gedcom_yadav.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'
    
    def us02(self, file_path=None):
        """return a list of objects whose birth date is after or on their marriage date """
        file_path = file_path if file_path else get_data_file_path('us02.ged')
        family_tree = TreeLine().process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        indi_list_us02_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            for spouse in indi.fams:
                marriage_date = family_tree.get(spouse).get_marr_date() if family_tree.get(spouse) else None
                if marriage_date and birth_date >= marriage_date:
                    warn_msg = f"birth date {indi.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)} should not occur after or on marriage date {family_tree.get(spouse).get_marr_date(TreeUtils.OUTPUT_DATE_FORMAT)}"
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US02', indi.id, warn_msg)
                    indi_list_us02_fail.append(indi)
                    continue
        # if indi_list_us02_fail:
        #     TreeUtils.print_report("US02 birth date is after marriage date ", indi_list_us02_fail)
        # print('prining indi us02 failed:')
        # for indi in indi_list_us02_fail:
        #     print(indi)
        return indi_list_us02_fail 
    
    def us06(self, file_path=None):
        """ return a list of objects whose divorce date is after death date """ 
        file_path = file_path if file_path else get_data_file_path('us06.ged')
        family_tree = TreeLine().process_data(file_path)
        fam_list = family_tree.get_fam_list()
        indi_list_us06_fail = []
        for fam in fam_list:
            husband_death_date = family_tree.get(fam.husb).get_death_date() if family_tree.get(fam.husb) else None
            wife_death_date = family_tree.get(fam.wife).get_death_date() if family_tree.get(fam.wife) else None
            divorce_date = fam.get_div_date() 
            if divorce_date:
                if husband_death_date and wife_death_date:
                    if divorce_date >= husband_death_date and divorce_date >= wife_death_date:
                        warn_msg = f"death date {family_tree.get(fam.husb).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)}, {family_tree.get(fam.wife).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)}  is before the divorce date for both {fam.get_div_date(TreeUtils.OUTPUT_DATE_FORMAT)}"
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US06', fam.id, warn_msg)
                        indi_list_us06_fail.append(fam)
                elif husband_death_date or wife_death_date:
                    if husband_death_date and divorce_date >= husband_death_date:
                        warn_msg = f"death date {family_tree.get(fam.husb).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)} of husband is  before the divorce date {fam.get_div_date(TreeUtils.OUTPUT_DATE_FORMAT)}"
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US06', fam.id, warn_msg)
                        indi_list_us06_fail.append(fam)
                    if wife_death_date and divorce_date >= wife_death_date:
                        warn_msg = f"death date {family_tree.get(fam.wife).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)} of wife is  before the divorce date {fam.get_div_date(TreeUtils.OUTPUT_DATE_FORMAT)}"
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US06', fam.id, warn_msg)
                        indi_list_us06_fail.append(fam)
                else:
                    continue   
        # if indi_list_us06_fail:
        #     TreeUtils.print_report("US06 divorce date is after death date ", indi_list_us06_fail)
        return indi_list_us06_fail 

    def us11(self, file_path=None):
        """ returns list of individuals whose marriage occured with two spouses at the same time """
        family_tree = TreeLine().process_data(file_path)
        fam_list = family_tree.get_fam_list()
        indi_list_us11_fail = []
        indi_list = family_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        for indi in indi_list:
            if len(indi.fams) > 1:
                indi_marr_dict = defaultdict(int) 
                for spouse in indi.fams:
                    marriage_date = family_tree.get(spouse).get_marr_date()
                    if marriage_date:
                        indi_marr_dict[marriage_date]+=1
                for key, val in indi_marr_dict.items():
                    if val > 1:
                        warn_msg = f"{indi.name} should not marry more than one person at same time" 
                        indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US11', indi.id, warn_msg)
                        indi_list_us11_fail.append(indi)     
        return indi_list_us11_fail


    def us16(self, file_path=None):
        """ returns list of males whose last name do not match their family name """
        #file_path = file_path if file_path else get_data_file_path('us02.ged')
        family_tree = TreeLine().process_data(file_path)
        fam_list = family_tree.get_fam_list()
        indi_list_us16_fail = []
        indi_list = family_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        for fam in fam_list:
            parent_full_name = (family_tree.get(fam.husb).name).split("/")
            parent_last_name = parent_full_name[1]
            for child in fam.chil:
                child_full_name = (family_tree.get(child).name).split("/")
                child_last_name = child_full_name[1]
                if parent_last_name != child_last_name:
                    warn_msg = f"Last name of {family_tree.get(child).name} doesnot match with last name of family {family_tree.get(fam.husb).name}"
                    fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US16', fam.id, warn_msg)
                    indi_list_us16_fail.append(fam)
                else:
                    continue
    
        return indi_list_us16_fail
    
    def us27(self, file_path=None):
        """ returns list of individuals with their ages"""
        family_tree = TreeLine().process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        indi_list_us27 = []
        dictt = defaultdict(int)
        for indi in indi_list:
            dictt[indi.id] = indi.get_age()
        return dictt


    def us30(self, file_path=None):
        """ returns list of sll living married people """
        family_tree = TreeLine().process_data(file_path)
        x = PrettyTable()
        indi_list_us30 = []
        indi_list = family_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        x.field_names = ["ID","Name","Gender","Number of spouses"]
        for indi in indi_list:
            if indi.fams and indi.get_death_date() == None:
                x.add_row([indi.id, indi.name, indi.sex, len(indi.fams)])
                indi_list_us30.append(indi)
            else:
                continue
        print("Individuals Living Married")
        return indi_list_us30                                 