from datetime import datetime, timedelta

from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
import calendar


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
        file_path = '../data/us09&10.ged' if not file_path else file_path
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesMSK.INDI_TAG)
        indi_list_us09_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            mother_death_date = processed_tree.get(processed_tree.get(indi.famc).wife).get_death_date() if processed_tree.get(indi.famc) and processed_tree.get(processed_tree.get(indi.famc).wife) else None
            father_death_date = processed_tree.get(processed_tree.get(indi.famc).wife).get_death_date() if processed_tree.get(indi.famc) and processed_tree.get(processed_tree.get(indi.famc).husb) else None
            if birth_date and mother_death_date and birth_date > mother_death_date:
                warn_msg = f"Birthday {indi.get_birth_date()} occurs after mother's death date {mother_death_date}"
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                indi_list_us09_fail.append(indi)
            if birth_date and father_death_date:
                # TODO: add or subtract 9 months
                days_in_month = calendar.monthrange(father_death_date.year, father_death_date.month)[1]
                max_birth_date = father_death_date + timedelta(days=days_in_month)
                if birth_date > max_birth_date:
                    warn_msg = f"Birthday {indi.get_birth_date()} occurs 9 months after father's death date {father_death_date}"
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                    indi_list_us09_fail.append(indi)
        return indi_list_us09_fail

    def us10(self, file_path=None):
        """
        returns list of individuals whose age is less than 14 during marriage
        """
        file_path = '../data/us09&10.ged' if not file_path else file_path
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesMSK.FAM_TAG)
        indi_list_us10_fail = []
        for fam in fam_list:
            marriage_date = fam.get_marr_date()
            wife_age = processed_tree.get(fam.wife).get_age(marriage_date) if processed_tree.get(fam.wife) else None
            husb_age = processed_tree.get(fam.husb).get_age(marriage_date) if processed_tree.get(fam.husb) else None

            if marriage_date:
                if wife_age and wife_age < 14:
                    warn_msg = f"Wife married before turning 14"
                    fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US10',
                                        processed_tree.get(fam.wife).id, warn_msg)
                    indi_list_us10_fail.append(fam)
                if husb_age and husb_age < 14:
                    warn_msg = f"Husband married before turning 14"
                    fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US10',
                                        processed_tree.get(fam.husb).id, warn_msg)
                    indi_list_us10_fail.append(fam)
        return indi_list_us10_fail

    def print_list(self, list_name, list):
        print(f'\n******************** {list_name} ********************')
        for item in list:
            print(item)
