from datetime import datetime, timedelta

from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils, get_data_file_path


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
