from datetime import datetime, timedelta
from com.familytree.TreeLine import TreeLine
from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils
import calendar


class UserStoriesNy:

    FILE_PATH = '../data/Familytree_test_file.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'
    REPORT_NAMES = {
        'us01': 'US01 Dates before current date',
        'us08': 'US08 Birth before marriage of parents'
    }

    def us01(self, file_path=None):
        """ returns a list of objects containing dates after current date
        """
        print(f'\n{TreeUtils.form_heading("Starting User Story 1", "#")}')
        file_path = file_path if file_path else TreeUtils.get_file_path('us01')
        tree_line = TreeLine()
        family_tree = tree_line.process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        fam_list = family_tree.get_sorted_list(UserStoriesNy.FAM_TAG)
        today_date = datetime.today()
        today_date_formatted = today_date.strftime(Tree.OUTPUT_DATE_FORMAT)
        indi_list_us01 = []
        fam_list_us01 = []
        for indi in indi_list:
            if indi.get_birth_date() and indi.get_birth_date() > today_date:
                indi.warn_msg = f'Birth date {indi.get_birth_date(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is after current date {today_date_formatted}'
                indi_list_us01.append(indi)
                continue
            if indi.get_death_date() and indi.get_death_date() > today_date:
                indi.warn_msg = f'Death date {indi.get_death_date(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is after current date {today_date_formatted}'
                indi_list_us01.append(indi)
                # continue

        for fam in fam_list:
            if fam.get_marr_date() and fam.get_marr_date() > today_date:
                fam.warn_msg = f'Marriage date {fam.get_marr_date(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is after current date {today_date_formatted}'
                fam_list_us01.append(fam)
                continue
            if fam.get_div_date() and fam.get_div_date() > today_date:
                fam.warn_msg = f'Divorce date {fam.get_div_date().strftime(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is after current date {today_date_formatted}'
                fam_list_us01.append(fam)
                # continue

        tree_line.tabulate(family_tree)
        TreeUtils.print_report(self.REPORT_NAMES['us01'], indi_list_us01 + fam_list_us01)
        print(TreeUtils.form_heading('Ending User Story 1', '#'))
        return indi_list_us01 + fam_list_us01

    def us08(self, file_path=None):
        """ returns a list of individuals whose birth date is before parent's marriage date
        or nine months after parent's divorce date
        """
        print(TreeUtils.form_heading('Starting User Story 8', '#'))
        file_path = file_path if file_path else TreeUtils.get_file_path('us08')
        tree_line = TreeLine()
        family_tree = tree_line.process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        indi_list_us08_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            parent_marr_date = family_tree.get(indi.famc).get_marr_date() if family_tree.get(indi.famc) else None
            parent_div_date = family_tree.get(indi.famc).get_div_date() if family_tree.get(indi.famc) else None
            if birth_date and parent_marr_date and birth_date < parent_marr_date:
                indi.warn_msg = f'Birth date {birth_date.strftime(Tree.OUTPUT_DATE_FORMAT)} ' \
                    f'is before parent\'s marriage date {parent_marr_date.strftime(Tree.OUTPUT_DATE_FORMAT)}'
                indi_list_us08_fail.append(indi)
                continue
            if birth_date and parent_div_date:
                days_in_month = calendar.monthrange(parent_div_date.year, parent_div_date.month)[1]
                max_birth_date = parent_div_date + timedelta(days=days_in_month)
                if birth_date > max_birth_date:
                    indi.warn_msg = f'Birth date {birth_date.strftime(Tree.OUTPUT_DATE_FORMAT)} ' \
                        f'is 9 months after parent\'s divorce date {parent_div_date.strftime(Tree.OUTPUT_DATE_FORMAT)}'
                    indi_list_us08_fail.append(indi)

        tree_line.tabulate(family_tree)
        TreeUtils.print_report(self.REPORT_NAMES['us08'], indi_list_us08_fail)
        print(TreeUtils.form_heading('Ending User Story 8', '#'))
        return indi_list_us08_fail


# if __name__ == '__main__':
#     us = UserStoriesNy()
#     us.us01()
