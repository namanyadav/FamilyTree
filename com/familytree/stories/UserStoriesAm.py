from datetime import datetime, timedelta

from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import TreeUtils

class UserStoriesAm:

    FILE_PATH = './com/familytree/data/Family_US02_US06.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'
    
    def us02(self, file_path=None):
        """return a list of objects whose birth date is after their marriage date """
        file_path = file_path if file_path else UserStoriesAm.FILE_PATH
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        indi_list_us02_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            for spouse in indi.fams:
                marriage_date = processed_tree.get(spouse).get_marr_date() if processed_tree.get(spouse) else None
                if marriage_date and birth_date > marriage_date:
                    warn_msg = f"birth date should not occur after marriage date"
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US02', indi.id, warn_msg)
                    indi_list_us02_fail.append(indi)
                    continue
        # if indi_list_us02_fail:
        #     TreeUtils.print_report("US02 birth date is after marriage date ", indi_list_us02_fail)
        return indi_list_us02_fail 
    
    def us06(self, file_path=None):
        """ return a list of objects whose divorce date is after death date """
        file_path = file_path if file_path else UserStoriesAm.FILE_PATH
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        fam_list = processed_tree.get_sorted_list(UserStoriesAm.FAM_TAG)
        indi_list_us06_fail = []
        for fam in fam_list:
            husband_death_date = processed_tree.get(fam.husb).get_death_date() if processed_tree.get(fam.husb) else None
            wife_death_date = processed_tree.get(fam.wife).get_death_date() if processed_tree.get(fam.wife) else None
            divorce_date = fam.get_div_date() 
            if divorce_date:
                if husband_death_date and wife_death_date:
                    if divorce_date > husband_death_date and divorce_date > wife_death_date:
                        warn_msg = f"death date is before the divorce date for both"
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US06', fam.id, warn_msg)
                        indi_list_us06_fail.append(fam)
                elif husband_death_date or wife_death_date:
                    if husband_death_date and divorce_date > husband_death_date:
                        warn_msg = f"death date of husband is  before the divorce date"
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US06', fam.id, warn_msg)
                        indi_list_us06_fail.append(fam)
                    if wife_death_date and divorce_date > wife_death_date:
                        warn_msg = f"death date of wife is  before the divorce date"
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US06', fam.id, warn_msg)
                        indi_list_us06_fail.append(fam)
                else:
                    continue   
        # if indi_list_us06_fail:
        #     TreeUtils.print_report("US06 divorce date is after death date ", indi_list_us06_fail)
        return indi_list_us06_fail 
