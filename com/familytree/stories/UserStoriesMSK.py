from datetime import datetime, timedelta

from com.familytree.Tree import Tree
from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import TreeUtils
import calendar
from dateutil.relativedelta import relativedelta

from com.familytree.TreeUtils import date_greater_than, add_to_date, get_data_file_path


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

            if date_greater_than(birth_date, mother_death_date):
                warn_msg = f"Birthday {indi.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)} occurs after mother's death date {mother_death_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)}"
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                indi_list_us09_fail.append(indi)
            elif date_greater_than(birth_date, add_to_date(father_death_date, months=9)):
                warn_msg = f"Birthday {indi.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)} occurs 9 months after father's death date {father_death_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)}"
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                indi_list_us09_fail.append(indi)
            elif date_greater_than(birth_date, mother_death_date) and date_greater_than(birth_date, add_to_date(father_death_date, months=9)):
                warn_msg = f"Birthday {indi.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)} occurs after mother's death date {mother_death_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)} and 9 months after father's death date {father_death_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)}"
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
                indi_list_us09_fail.append(indi)

            # if birth_date and mother_death_date and birth_date>mother_death_date:
            #     warn_msg = f"Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs after mother's death date {mother_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)}"
            #     indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
            #     indi_list_us09_fail.append(indi)
            #
            # elif birth_date and father_death_date:
            #     max_birth_date = father_death_date + relativedelta(months=9)
            #     # days_in_month = calendar.monthrange(father_death_date.year, father_death_date.month)[1]
            #     # max_birth_date = father_death_date + timedelta(days=days_in_month)
            #     if birth_date>max_birth_date:
            #         warn_msg = f"Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs 9 months after father's death date {father_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)}"
            #         indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
            #         indi_list_us09_fail.append(indi)
            #
            # elif birth_date and mother_death_date:
            #     # days_in_month = calendar.monthrange(father_death_date.year, father_death_date.month)[1]
            #     # max_birth_date = father_death_date + timedelta(days=days_in_month)
            #     max_birth_date = father_death_date + relativedelta(months=9)
            #     if birth_date>mother_death_date and birth_date > max_birth_date:
            #         warn_msg = f"Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs after mother's death date {mother_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)} and 9 months after father's death date {father_death_date.strftime(Tree.OUTPUT_DATE_FORMAT)}"
            #         indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US09', indi.id, warn_msg)
            #         indi_list_us09_fail.append(indi)

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


    def us17(self, file_path=None):
        """
                returns list of individuals who are married to their children
        """
        file_path = file_path if file_path else get_data_file_path('us17.ged')
        family_tree = TreeLine().process_data(file_path)
        us17_fail = []
        indi_list = family_tree.get_indi_list()
        for indi in indi_list:
            children_list = indi.get_children(family_tree)
            spouse_list = indi.get_spouses(family_tree)
            common_indi_list = set(children_list) & set(spouse_list)
            if common_indi_list:
                for child in common_indi_list:
                    warn_msg = f'{indi.name} married child {child.name}'
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US17', indi.id, warn_msg)
                    us17_fail.append(indi)

        return us17_fail

    def us18(self, file_path=None):
        """
                returns list of individuals who are married to their siblings
        """
        file_path = file_path if file_path else get_data_file_path('us18.ged')
        family_tree = TreeLine().process_data(file_path)
        us18_fail = []
        indi_list = family_tree.get_indi_list()
        for indi in indi_list:
            real_siblings_list = indi.get_real_siblings(family_tree)
            spouse_list = indi.get_spouses(family_tree)
            common_indi_list = set(real_siblings_list) & set(spouse_list)
            if common_indi_list:
                for real_sibling in common_indi_list:
                    warn_msg = f'{indi.name} married sibling {real_sibling.name}'
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US18', indi.id, warn_msg)
                    us18_fail.append(indi)

        return us18_fail

    def us20(self, file_path=None):
        """
                        returns list of individuals who are married to Aunts and uncles
        """
        file_path = file_path if file_path else get_data_file_path('US20.ged')
        family_tree = TreeLine().process_data(file_path)
        us20_fail = []
        indi_list = family_tree.get_indi_list()
        for indi in indi_list:
            # print("indi: ",indi)
            indi_father = indi.get_father(family_tree)
            indi_mother = indi.get_mother(family_tree)
            # spouse_list = indi.get_spouses(family_tree)
            if indi_father:
                # print("indi: ",indi.name, " father: ", indi_father.name)
                father_real_sibling_list = indi_father.get_real_siblings(family_tree)
                if father_real_sibling_list:
                    spouse_list = indi.get_spouses(family_tree)
                    common_indi_list = set(father_real_sibling_list) & set(spouse_list)
                    if common_indi_list:
                        for father_real_sibling in common_indi_list:
                            warn_msg = f'{indi.name} married fathers sibling {father_real_sibling.name}'
                            # print("warn_msg: ", warn_msg)
                            indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US20', indi.id, warn_msg)
                            us20_fail.append(indi)

            if indi_mother:
                # print("indi: ", indi.name, " mother: ", indi_mother.name)
                mother_real_sibling_list = indi_mother.get_real_siblings(family_tree)
                if mother_real_sibling_list:
                    spouse_list = indi.get_spouses(family_tree)
                    common_indi_list = set(mother_real_sibling_list) & set(spouse_list)
                    if common_indi_list:
                        for mother_real_sibling in common_indi_list:
                            warn_msg = f'{indi.name} married mothers sibling {mother_real_sibling.name}'
                            # print("warn_msg: ", warn_msg)
                            indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US20', indi.id, warn_msg)
                            us20_fail.append(indi)

        return us20_fail

    def us31(self, file_path=None):
        """"
                        returns list of living individuals who are over 30 and have never been married
        """
        file_path = file_path if file_path else get_data_file_path('US31.ged')
        family_tree = TreeLine().process_data(file_path)
        us31_fail = []
        indi_list = family_tree.get_indi_list()
        for indi in indi_list:
            spouse_list = indi.get_spouses(family_tree)
            if len(spouse_list) == 0:
                age = indi.get_age()
                if age and age > 30:
                    warn_msg = f'{indi.name} age is {age} and has never been married'
                    print(warn_msg)
                    indi.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_INDI, 'US31', indi.id, warn_msg)
                    us31_fail.append(indi)
        return us31_fail
