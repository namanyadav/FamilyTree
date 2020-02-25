from datetime import datetime, timedelta
from com.familytree.TreeLine import TreeLine
import calendar


class UserStoriesNy:

    FILE_PATH = '../data/Familytree_test_file.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us01(self):
        """
        returns a list of objects containing dates after current date
        :return:
        """
        file_path = '../data/us01.ged'
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        fam_list = processed_tree.get_sorted_list(UserStoriesNy.FAM_TAG)
        today_date = datetime.today()
        indi_list_us01 = []
        fam_list_us01 = []
        for indi in indi_list:
            if indi.get_birth_date() and indi.get_birth_date() > today_date:
                indi_list_us01.append(indi)
                continue
            if indi.get_death_date() and indi.get_death_date() > today_date:
                indi_list_us01.append(indi)
                # continue

        for fam in fam_list:
            if fam.get_marr_date() and fam.get_marr_date() > today_date:
                fam_list_us01.append(fam)
                continue
            if fam.get_div_date() and fam.get_div_date() > today_date:
                fam_list_us01.append(fam)
                # continue

        return indi_list_us01 + fam_list_us01

    def us08(self):
        """
        returns a list of individuals whose birth date is before parent's marriage date
        or nine months after parent's divorce date
        """
        file_path = '../data/us08.ged'
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesNy.INDI_TAG)
        indi_list_us08_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            parent_marr_date = processed_tree.get(indi.famc).get_marr_date() if processed_tree.get(indi.famc) else None
            parent_div_date = processed_tree.get(indi.famc).get_div_date() if processed_tree.get(indi.famc) else None
            if birth_date and parent_marr_date and birth_date < parent_marr_date:
                indi_list_us08_fail.append(indi)
                continue
            if birth_date and parent_div_date:
                days_in_month = calendar.monthrange(parent_div_date.year, parent_div_date.month)[1]
                max_birth_date = parent_div_date + timedelta(days=days_in_month)
                if birth_date > max_birth_date:
                    indi_list_us08_fail.append(indi)
        return indi_list_us08_fail

    def print_list(self, list_name, list):
        print(f'\n******************** {list_name} ********************')
        for item in list:
            print(item)


if __name__ == '__main__':
    usny = UserStoriesNy()
    usny.print_list('US 01', usny.us01())
    usny.print_list('US 08', usny.us08())