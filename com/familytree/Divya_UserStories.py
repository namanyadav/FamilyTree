from datetime import datetime, timedelta
from TreeUtils import TreeUtils
from TreeLine import TreeLine
import calendar

class Divya_UserStories:

    FILE_PATH = './data/us05&07.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us07(self):
        """
        returns a list of objects with age greater than or equal to 150
        """
        processed_tree = TreeLine().process_data(Divya_UserStories.FILE_PATH)
        indi_list = processed_tree.get_sorted_list(Divya_UserStories.INDI_TAG)
        indi_list_us07 = []
        for indi in indi_list:
            if indi.get_age() >= 150:
                indi.warn_msg = f'Age is greater than or equal to 150, Age: {indi.get_age()}'
                indi_list_us07.append(indi)
                continue
        
        if indi_list_us07:
            #TreeLine().tabulate(processed_tree)
            TreeUtils.print_report("US07 Less then 150 years old", indi_list_us07)
        return indi_list_us07


    def us05(self):
        """
        returns a list of objects whose divorse date is before death date
        """

        processed_tree = TreeLine().process_data(Divya_UserStories.FILE_PATH)
        fam_list = processed_tree.get_sorted_list(Divya_UserStories.FAM_TAG)
        fam_list_us05 = []
        for fam in fam_list:
            marr_date = fam.get_marr_date()
            hus_death_date = processed_tree.get(fam.husb).get_death_date() if processed_tree.get(fam.husb) else None
            wife_death_date = processed_tree.get(fam.wife).get_death_date() if processed_tree.get(fam.wife) else None
            if marr_date:
                fam.warn_msg = f'Marriage date should occur before death of spouses {processed_tree.get(fam.husb).name}, {processed_tree.get(fam.wife).name}'
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
        if fam_list_us05:
            #TreeLine().tabulate(processed_tree)
            TreeUtils.print_report("US07 Less then 150 years old", fam_list_us05)
        return fam_list_us05

if __name__ == '__main__':
    usdg = Divya_UserStories()
    usdg.us05()
    usdg.us07()

