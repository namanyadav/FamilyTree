
from datetime import datetime

from com.familytree.TreeError import TreeError
from com.familytree.TreeUtils import TreeUtils, date_greater_than
from com.familytree.TreeLine import TreeLine
from com.familytree.Tree import Tree
from collections import defaultdict

class UserStoriesDg:

    FILE_PATH1 = '../data/us07.ged'
    FILE_PATH2 = '../data/us05.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us07(self, file_path=None):
        """returns a list of objects with age greater than or equal to 150"""
        # file_path = file_path if file_path else UserStoriesDg.FILE_PATH1
        # processed_tree = TreeLine().process_data(file_path)
        indi_list = self.get_treedata(file_path).get_sorted_list(UserStoriesDg.INDI_TAG)
        indi_list_us07 = []
        for indi in indi_list:
            if indi.get_age() >= 150:
                warn_msg = f'Age is greater than or equal to 150, {indi.name} Age: {indi.get_age()}'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US07', indi.id, warn_msg)
                indi_list_us07.append(indi)
        return indi_list_us07

    def us05(self, file_path=None):
        """ returns a list of objects whose marriage date is after death date"""
        family_tree = self.get_treedata(file_path)
        fam_list = family_tree.get_sorted_list(UserStoriesDg.FAM_TAG)
        fam_list_us05 = []
        for fam in fam_list:
            marr_date = fam.get_marr_date()
            hus_death_date = fam.get_husb_death_date(family_tree)
            wife_death_date = fam.get_wife_death_date(family_tree)

            # if marr_date and hus_death_date and wife_death_date and wife_death_date <= marr_date and hus_death_date <= marr_date:
            if date_greater_than(marr_date, wife_death_date, True) and date_greater_than(marr_date, hus_death_date, True):
                warn_msg = f'Marriage {fam.get_marr_date(TreeUtils.OUTPUT_DATE_FORMAT)} should occur before death of {family_tree.get(fam.husb).name} - {family_tree.get(fam.husb).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)}, {family_tree.get(fam.wife).name} - {family_tree.get(fam.wife).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)}'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US05', fam.id, warn_msg)
                fam_list_us05.append(fam)

            # elif marr_date and hus_death_date and hus_death_date <= marr_date:
            elif date_greater_than(marr_date, hus_death_date, True):
                warn_msg = f'Marriage date {fam.get_marr_date(TreeUtils.OUTPUT_DATE_FORMAT)} should occur before death of {family_tree.get(fam.husb).name} - {family_tree.get(fam.husb).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)}'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US05', fam.id, warn_msg)
                fam_list_us05.append(fam)

            # elif marr_date and wife_death_date and wife_death_date <= marr_date:
            elif date_greater_than(marr_date, wife_death_date, True):
                warn_msg = f'Marriage date {fam.get_marr_date(TreeUtils.OUTPUT_DATE_FORMAT)} should occur before death of {family_tree.get(fam.wife).name} - {family_tree.get(fam.wife).get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)}'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US05', fam.id, warn_msg)
                fam_list_us05.append(fam)
        return fam_list_us05


    def us15(self, file_path=None):
        """ returns a list of objects if family has more than 15 siblings """
        fam_list = self.get_treedata(file_path).get_sorted_list(UserStoriesDg.FAM_TAG)
        fam_list_us15 = []
        for fam in fam_list:
            if len(fam.chil) >= 15:
                warn_msg = f'Family has more than 15 siblings'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US15', fam.id, warn_msg)
                fam_list_us15.append(fam)
        return fam_list_us15

    
    def us12(self, file_path=None):
        """ returns a list of objects if Parents are too old  """
        family_tree = self.get_treedata(file_path)
        fam_list = family_tree.get_sorted_list(UserStoriesDg.FAM_TAG)
        fam_list_us12 = []
        for fam in fam_list:
            father_age = family_tree.get(fam.husb).get_age()
            mother_age = family_tree.get(fam.wife).get_age()
            for child in fam.chil:
                child_age = family_tree.get(child).get_age()
                father_child_diff = father_age - child_age if father_age and child_age else None
                mother_child_diff = mother_age - child_age if mother_age and child_age else None
                if father_child_diff and father_child_diff >= 80 or mother_child_diff and mother_child_diff >=60 :
                    if father_child_diff and mother_child_diff and father_child_diff >= 80 and  mother_child_diff >=60 :
                        warn_msg = f'Father and Mother should be less than 80 years and 60 years older than their child - {family_tree.get(child).name}'
                    elif father_child_diff and father_child_diff >= 80:
                        warn_msg = f'Father should be less than 80 years than their child - {family_tree.get(child).name}'
                    else:
                        warn_msg = f'Mother should be less than 60 years than their child - {family_tree.get(child).name}'
                    fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US12', child, warn_msg)
                    fam_list_us12.append(family_tree.get(child))
        return fam_list_us12

    def us23(self, file_path=None):
        """ returns a list of individuals with the same name and birth date """
        ind_list = self.get_treedata(file_path).get_sorted_list(UserStoriesDg.INDI_TAG)
        ind_list_us23 = []
        ind_dict = {}
        for ind in ind_list: 
            ind.name = ind.name.replace('/', '')
            if ind.name not in ind_dict:
                ind_dict[ind.name] = ind.get_birth_date()
            else:
                if ind.get_birth_date() == ind_dict[ind.name]:
                    warn_msg = f'More than one individual has same name - {ind.name} and birthdate - {ind.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)}'
                    ind.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US23', ind.id, warn_msg)
                    ind_list_us23.append(ind)
                    continue
                else:
                    ind_dict[ind.name] = ind.get_birth_date()
        return ind_list_us23

    def us25(self, file_path=None):
        """ returns a fam list with the same first name and birth date in a family """
        family_tree = self.get_treedata(file_path)
        fam_list = family_tree.get_sorted_list(UserStoriesDg.FAM_TAG)
        fam_list_us25 = []
        for fam in fam_list: 
            fam_dict = {}
            for child in fam.chil:
                childname = family_tree.get(child).name
                child_birthdate = family_tree.get(child).get_birth_date()
                if childname not in fam_dict:
                    fam_dict[childname] = child_birthdate
                else:
                    if child_birthdate == fam_dict[childname]:
                        warn_msg = f'More than one child has the same first name - {childname} and birthdate - {family_tree.get(child).get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)}'
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US25', fam.id, warn_msg)
                        fam_list_us25.append(fam)
                        continue
                    else:
                        fam_dict[childname] = child_birthdate
        return fam_list_us25

    def get_id_list(self, obj_list):
        """ return the individual or family id's """

        id_list = []
        if obj_list:
            for obj in obj_list:
                id_list.append(obj.id)
        return id_list

    def get_treedata(self, path):
        """ return the tree objects of individual and family """
        file_path = path if path else UserStoriesDg.FILE_PATH1
        processed_tree = TreeLine().process_data(file_path)
        return processed_tree


