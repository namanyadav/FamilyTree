from datetime import datetime, timedelta
from com.familytree.TreeLine import TreeLine
import calendar


class UserStoriesMSK:

    FILE_PATH = '../data/Familytree_test_file.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us09(self):
        """
        returns a list of children who are born before death of mother
         and before 9 months after death of father
        :return:
        """
        file_path = '/home/manas/Stevens/CS 555 Agile/Project/US08&09/us09&10.ged'
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesMSK.INDI_TAG)
        indi_list_us09_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            mother_death_date = processed_tree.get(processed_tree.get(indi.famc).wife).get_death_date() if processed_tree.get(indi.famc) else None
            father_death_date = processed_tree.get(processed_tree.get(indi.famc).husb).get_death_date() if processed_tree.get(indi.famc) else None
            if birth_date and mother_death_date and birth_date > mother_death_date:
                indi_list_us09_fail.append(indi)
                continue
            if birth_date and father_death_date:
                # TODO: add or subtract 9 months
                days_in_month = calendar.monthrange(father_death_date.year, father_death_date.month)[1]
                max_birth_date = father_death_date + timedelta(days=days_in_month)
                if birth_date > max_birth_date:
                    indi_list_us09_fail.append(indi)
        return indi_list_us09_fail

    def us10(self):
        """
        returns a list of individuals whose birth date is before parent's marriage date
        or nine months after parent's divorce date
        """
        file_path = '/home/manas/Stevens/CS 555 Agile/Project/US08&09/us09&10.ged'
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesMSK.INDI_TAG)
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
    usmsk = UserStoriesMSK()
    usmsk.print_list('US 01', usmsk.us09())
    #usny.print_list('US 08', usny.us08())