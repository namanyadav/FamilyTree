from datetime import datetime, timedelta
from TreeLine import TreeLine
import calendar

class Divya_UserStories:

    FILE_PATH = '../data/Familytree_test_file.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us07(self):
        """
        returns a list of objects with age greater than 150
        """
        file_path = './data/Familytree_test_file.ged'
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(Divya_UserStories.INDI_TAG)
        indi_list_us07 = []
        for indi in indi_list:
            if indi.get_age() >= 150:
                indi_list_us07.append(indi)
                continue
        #TreeLine.printwarnings(indi_list_us07, "Age cannot be greater than or equal to 150")
        return indi_list_us07


    def us05(self):
        """
        returns a list of objects whose divorse date is before death date
        """

        file_path = './data/SampleTestFile.ged'
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(Divya_UserStories.FAM_TAG)
        #indi_list = processed_tree.get_sorted_list(Divya_UserStories.INDI_TAG)
        fam_list_us05 = []
        for fam in fam_list:
            marr_date = fam.get_marr_date()
            hus_death_date = processed_tree.get(fam.husb).get_death_date() if processed_tree.get(fam.husb) else None
            wife_death_date = processed_tree.get(fam.wife).get_death_date() if processed_tree.get(fam.wife) else None
            if marr_date:
                if hus_death_date and wife_death_date:
                    if wife_death_date < marr_date and hus_death_date < marr_date:
                        fam_list_us05.append(fam)
                elif hus_death_date or wife_death_date:
                    if hus_death_date and hus_death_date < marr_date:
                        fam_list_us05.append(fam)
                    elif wife_death_date and wife_death_date < marr_date:
                        fam_list_us05.append(fam)
                    else:
                        continue
                else:
                    pass
        return fam_list_us05

if __name__ == '__main__':
    usdg = Divya_UserStories()
    usdg.us07()
    usdg.us05()

