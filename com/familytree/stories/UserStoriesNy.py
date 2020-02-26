from datetime import datetime, timedelta
from com.familytree.TreeLine import TreeLine
import calendar


class UserStoriesNy:

    FILE_PATH = '../data/Familytree_test_file.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def __init__(self):
        self.indi_failed = []
        self.fam_failed = []

    def us01(self):
        """
        returns a list of objects containing dates after current date
        :return:
        """
        file_path = self.get_file_path('us01')
        family_tree = TreeLine().process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        fam_list = family_tree.get_sorted_list(UserStoriesNy.FAM_TAG)
        today_date = datetime.today()
        indi_list_us01 = []
        fam_list_us01 = []
        for indi in indi_list:
            if indi.get_birth_date() and indi.get_birth_date() > today_date:
                indi.warn_msg = f'Birth date {indi.get_birth_date()} is after current date {today_date}'
                indi_list_us01.append(indi)
                continue
            if indi.get_death_date() and indi.get_death_date() > today_date:
                indi.warn_msg = f'Death date {indi.get_death_date()} is after current date {today_date}'
                indi_list_us01.append(indi)
                # continue

        for fam in fam_list:
            if fam.get_marr_date() and fam.get_marr_date() > today_date:
                fam.warn_msg = f'Marriage date {fam.get_marr_date()} is after current date {today_date}'
                fam_list_us01.append(fam)
                continue
            if fam.get_div_date() and fam.get_div_date() > today_date:
                fam.warn_msg = f'Divorce date {fam.get_div_date()} is after current date {today_date}'
                fam_list_us01.append(fam)
                # continue

        # self.print_list('US 01', indi_list_us01 + fam_list_us01)
        # self.indi_failed.append(indi_list_us01)
        # self.fam_failed.append(fam_list_us01)
        self.print_report('INDI', indi_list_us01, family_tree)
        self.print_report('FAM', fam_list_us01, family_tree)
        return indi_list_us01 + fam_list_us01
        # return "naman"

    def us08(self):
        """
        returns a list of individuals whose birth date is before parent's marriage date
        or nine months after parent's divorce date
        """
        file_path = self.get_file_path('us08')
        family_tree = TreeLine().process_data(file_path)
        indi_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        indi_list_us08_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            parent_marr_date = family_tree.get(indi.famc).get_marr_date() if family_tree.get(indi.famc) else None
            parent_div_date = family_tree.get(indi.famc).get_div_date() if family_tree.get(indi.famc) else None
            if birth_date and parent_marr_date and birth_date < parent_marr_date:
                indi.warn_msg = f'Birth date {birth_date} is before parent\'s marriage date {parent_marr_date}'
                indi_list_us08_fail.append(indi)
                continue
            if birth_date and parent_div_date:
                days_in_month = calendar.monthrange(parent_div_date.year, parent_div_date.month)[1]
                max_birth_date = parent_div_date + timedelta(days=days_in_month)
                if birth_date > max_birth_date:
                    indi.warn_msg = f'Birth date {birth_date} is 9 months after parent\'s divorce date {parent_div_date}'
                    indi_list_us08_fail.append(indi)

        # self.print_list('US08', indi_list_us08_fail)
        # self.indi_failed(indi_list_us08_fail)
        self.print_report('INDI', indi_list_us08_fail, family_tree)
        return indi_list_us08_fail

    # @staticmethod
    # def generate_warning_msg(obj, msg):

    @staticmethod
    def print_report(obj_type, obj_list, family_tree):
        indi_heading_list = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse", "Warning"]
        fam_heading_list = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                            "Children", "Warning"]

        treeline = TreeLine()

        if obj_type == 'INDI':
            indi_printer = treeline.get_table_printer('INDI', indi_heading_list)
            for indi in obj_list:
                treeline.process_for_pretty_table('INDI', indi, family_tree)
                indi_printer.add_row(
                    [indi.id, indi.name, indi.sex, indi.birt_disp, indi.age_disp, indi.alive_disp, indi.deat_disp,
                     indi.famc_disp, indi.fams_disp, indi.warn_msg])

            if obj_list:
                print(indi_printer)

        if obj_type == 'FAM':
            fam_printer = treeline.get_table_printer('FAM', fam_heading_list)
            for fam in obj_list:
                treeline.process_for_pretty_table('FAM', fam, family_tree)
                fam_printer.add_row([fam.id, fam.marr_disp, fam.div_disp, fam.husb, fam.husb_name, fam.wife, fam.wife_name, fam.chil, fam.warn_msg])

            if obj_list:
                print(fam_printer)

    @staticmethod
    def print_list(list_name, obj_list):
        print(f'\n******************** {list_name} ********************')
        for item in obj_list:
            print(item)

    @staticmethod
    def get_file_path(user_story):
        return f'../data/{user_story}.ged'
