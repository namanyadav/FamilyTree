from datetime import datetime, timedelta

from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils
import calendar
import logging
import os
import sys


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
        tree_line = TreeLine()
        family_tree = tree_line.process_data(file_path)
        indi_list, fam_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG), \
                              family_tree.get_sorted_list(UserStoriesNy.FAM_TAG)
        today_date = datetime.today()
        today_date_formatted = today_date.strftime(Tree.OUTPUT_DATE_FORMAT)
        indi_list_us01, fam_list_us01 = [], []
        # if there is error in both birth and death criteria, only birth will be listed
        for indi in indi_list:
            if indi.get_birth_date() and indi.get_birth_date() > today_date:
                warn_msg = f'Birthday {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US01', indi.id, warn_msg)
                indi_list_us01.append(indi)
                # continue
            if indi.get_death_date() and indi.get_death_date() > today_date:
                warn_msg = f'Death day {indi.get_death_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US01', indi.id, warn_msg)
                indi_list_us01.append(indi)
                # continue

        # if there is error in both marriage and divorce criteria, only marriage will be listed
        for fam in fam_list:
            if fam.get_marr_date() and fam.get_marr_date() > today_date:
                warn_msg = f'Marriage date {fam.get_marr_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US01', fam.id, warn_msg)
                fam_list_us01.append(fam)
                # continue
            if fam.get_div_date() and fam.get_div_date() > today_date:
                warn_msg = f'Divorce date {fam.get_div_date(Tree.OUTPUT_DATE_FORMAT)} occurs in future'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US01', fam.id, warn_msg)
                fam_list_us01.append(fam)
                # continue

        # tree_line.tabulate(family_tree)
        # TreeUtils.print_report(self.REPORT_NAMES['us01'], indi_list_us01 + fam_list_us01)
        # self.logger.error(TreeUtils.form_heading('Ending User Story 1', '#', 70))
        # for indi in indi_list_us01:
        #     print(indi.err)
        return indi_list_us01 + fam_list_us01

    def us08(self, file_path=None):
        """ returns a list of individuals whose birth date is before parent's marriage date
        or nine months after parent's divorce date
        """
        # self.logger.error(TreeUtils.form_heading('Starting User Story 8', '#', 70))
        file_path = file_path if file_path else TreeUtils.get_file_path('us08')
        tree_line = TreeLine()
        family_tree = tree_line.process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        indi_list_us08_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            parent_marr_date = family_tree.get(indi.famc).get_marr_date() if family_tree.get(indi.famc) else None
            parent_div_date = family_tree.get(indi.famc).get_div_date() if family_tree.get(indi.famc) else None
            # if birth date is on or before marriage date, add indi to failure list
            if birth_date and parent_marr_date and birth_date <= parent_marr_date:
                warn_msg = f'Birth date {birth_date.strftime(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is before or on parent\'s marriage date {parent_marr_date.strftime(Tree.OUTPUT_DATE_FORMAT)}'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US08', indi.id, warn_msg)
                indi_list_us08_fail.append(indi)
                # continue
            if birth_date and parent_div_date:
                days_in_month = calendar.monthrange(parent_div_date.year, parent_div_date.month)[1]
                max_birth_date = parent_div_date + timedelta(days=days_in_month)
                if birth_date > max_birth_date:
                    warn_msg = f'Birth date {birth_date.strftime(Tree.OUTPUT_DATE_FORMAT)} ' \
                        f'is more than 9 months after parent\'s divorce date {parent_div_date.strftime(Tree.OUTPUT_DATE_FORMAT)}'
                    indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US08', indi.id, warn_msg)
                    indi_list_us08_fail.append(indi)

        return indi_list_us08_fail
