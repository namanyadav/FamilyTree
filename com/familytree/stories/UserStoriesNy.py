from datetime import datetime
from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils, date_greater_than, date_equal_to, add_to_date


# TODO: use only one gedcom file
# TODO: convert warn_msg to list of warning messages

# TODO: 9 months check in US08 and US09
# TODO: Change error report as given in sample
# TODO: what about Homework 5? Pair programming
class UserStoriesNy:

    FILE_PATH = '../data/Familytree_test_file.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'
    REPORT_NAMES = {
        'us01': 'US01 Dates before current date',
        'us08': 'US08 Birth before marriage of parents'
    }
    logger = TreeUtils.get_logger()

    def us01(self, file_path=None):
        """ returns a list of objects containing dates after current date
        """
        # self.logger.error(TreeUtils.form_heading("Starting User Story 1", "#", 70))
        file_path = file_path if file_path else TreeUtils.get_file_path('us01')
        family_tree = TreeLine().process_data(file_path)
        indi_list, fam_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG), \
                              family_tree.get_sorted_list(UserStoriesNy.FAM_TAG)
        today_date = datetime.today()
        indi_list_us01, fam_list_us01 = [], []
        # if there is error in both birth and death criteria, only birth will be listed
        for indi in indi_list:
            if date_greater_than(indi.get_birth_date(), today_date):
                warn_msg = f'Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US01', indi.id, warn_msg)
                indi_list_us01.append(indi)
            if date_greater_than(indi.get_death_date(), today_date):
                warn_msg = f'Death day {indi.get_death_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US01', indi.id, warn_msg)
                indi_list_us01.append(indi)

        # if there is error in both marriage and divorce criteria, only marriage will be listed
        for fam in fam_list:
            if date_greater_than(fam.get_marr_date(), today_date):
                warn_msg = f'Marriage date {fam.get_marr_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US01', fam.id, warn_msg)
                fam_list_us01.append(fam)
            if date_greater_than(fam.get_div_date(), today_date):
                warn_msg = f'Divorce date {fam.get_div_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US01', fam.id, warn_msg)
                fam_list_us01.append(fam)

        return indi_list_us01 + fam_list_us01

    def us08(self, file_path=None):
        """ returns a list of individuals whose birth date is before parent's marriage date
        or nine months after parent's divorce date
        """
        # self.logger.error(TreeUtils.form_heading('Starting User Story 8', '#', 70))
        file_path = file_path if file_path else TreeUtils.get_file_path('us08')
        family_tree = TreeLine().process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        indi_list_us08_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            parent_marr_date = indi.get_parent_marr_date(family_tree)
            parent_div_date = indi.get_parent_div_date(family_tree)
            # if birth date is on or before marriage date, add indi to failure list
            # if birth_date and parent_marr_date and birth_date <= parent_marr_date:
            if date_greater_than(parent_marr_date, birth_date) or date_equal_to(parent_marr_date, birth_date):
                warn_msg = f'Birth date {birth_date.strftime(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is before or on parent\'s marriage date {parent_marr_date.strftime(Tree.OUTPUT_DATE_FORMAT)}'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US08', indi.id, warn_msg)
                indi_list_us08_fail.append(indi)
            if date_greater_than(birth_date, add_to_date(parent_div_date, months=9)):
                warn_msg = f'Birth date {birth_date.strftime(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is more than 9 months after parent\'s divorce date {parent_div_date.strftime(Tree.OUTPUT_DATE_FORMAT)}'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US08', indi.id, warn_msg)
                indi_list_us08_fail.append(indi)

        return indi_list_us08_fail
