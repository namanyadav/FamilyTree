from datetime import datetime, timedelta

from com.familytree.Tree import Tree
from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
import calendar
from dateutil.relativedelta import relativedelta


class UserStoriesMSK:
    FILE_PATH = '../data/Familytree_test_file.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us09(self, file_path=None):
        """
        returns a list of children who are born before death of mother
         and before 9 months after death of father
        :return:
        """
        # file_path = '../data/us09.ged' if not file_path else file_path
        file_path = './com/familytree/data/us09.ged' if not file_path else file_path
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesMSK.INDI_TAG)
        indi_list_us09_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            mother_death_date = processed_tree.get(processed_tree.get(indi.famc).wife).get_death_date() if processed_tree.get(indi.famc) and processed_tree.get(processed_tree.get(indi.famc).wife) else None
            father_death_date = processed_tree.get(processed_tree.get(indi.famc).wife).get_death_date() if processed_tree.get(indi.famc) and processed_tree.get(processed_tree.get(indi.famc).husb) else None
            if birth_date and mother_death_date and birth_date>mother_death_date:
                warn_msg = f"Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs after mother's death date {mother_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)}"
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                indi_list_us09_fail.append(indi)

            elif birth_date and father_death_date:
                max_birth_date = father_death_date + relativedelta(months=9)
                # days_in_month = calendar.monthrange(father_death_date.year, father_death_date.month)[1]
                # max_birth_date = father_death_date + timedelta(days=days_in_month)
                if birth_date>max_birth_date:
                    warn_msg = f"Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs 9 months after father's death date {father_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)}"
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                    indi_list_us09_fail.append(indi)

            elif birth_date and mother_death_date:
                # days_in_month = calendar.monthrange(father_death_date.year, father_death_date.month)[1]
                # max_birth_date = father_death_date + timedelta(days=days_in_month)
                max_birth_date = father_death_date + relativedelta(months=9)
                if birth_date>mother_death_date and birth_date > max_birth_date:
                    warn_msg = f"Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs after mother's death date {mother_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)} and 9 months after father's death date {father_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)}"
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                    indi_list_us09_fail.append(indi)

        return indi_list_us09_fail

    def us10(self, file_path=None):
        """
        returns list of individuals whose age is less than 14 during marriage
        """
        file_path = '../data/us10.ged' if not file_path else file_path
        # file_path = './com/familytree/data/us10.ged' if not file_path else UserStoriesMSK.FILE_PATH
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesMSK.FAM_TAG)
        indi_list_us10_fail = []
        for fam in fam_list:
            marriage_date = fam.get_marr_date()
            wife_age = processed_tree.get(fam.wife).get_age(marriage_date) if processed_tree.get(fam.wife) else None
            husb_age = processed_tree.get(fam.husb).get_age(marriage_date) if processed_tree.get(fam.husb) else None

            if marriage_date:
                if wife_age and husb_age and wife_age<14 and husb_age<14:
                    warn_msg = f"Husband married before turning 14 and Wife married before turning 14"
                    fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US10',
                                        processed_tree.get(fam.husb).id, warn_msg)
                    indi_list_us10_fail.append(fam)
                elif wife_age and wife_age < 14:
                    warn_msg = f"Wife married before turning 14"
                    fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US10',
                                        processed_tree.get(fam.wife).id, warn_msg)
                    indi_list_us10_fail.append(fam)
                    # continue
                elif husb_age and husb_age < 14:
                    warn_msg = f"Husband married before turning 14"
                    fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US10',
                                        processed_tree.get(fam.husb).id, warn_msg)
                    indi_list_us10_fail.append(fam)
                    # continue
        return indi_list_us10_fail
