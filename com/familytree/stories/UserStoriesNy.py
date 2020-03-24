from datetime import datetime
from com.familytree.TreeError import TreeError
from com.familytree.TreeLine import TreeLine
from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils, date_greater_than, date_equal_to, add_to_date, get_data_file_path, \
    get_id_list, print_list


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
        file_path = file_path if file_path else get_data_file_path('us01.ged')
        family_tree = TreeLine().process_data(file_path)
        indi_list, fam_list = family_tree.get_sorted_list(UserStoriesNy.INDI_TAG), \
                              family_tree.get_sorted_list(UserStoriesNy.FAM_TAG)
        today_date = datetime.today()
        indi_list_us01, fam_list_us01 = [], []
        # if there is error in both birth and death criteria, only birth will be listed
        for indi in indi_list:
            if date_greater_than(indi.get_birth_date(), today_date):
                warn_msg = f'Birthday {indi.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)} occurs in future'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US01', indi.id, warn_msg)
                indi_list_us01.append(indi)
            if date_greater_than(indi.get_death_date(), today_date):
                warn_msg = f'Death day {indi.get_death_date(TreeUtils.OUTPUT_DATE_FORMAT)} occurs in future'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US01', indi.id, warn_msg)
                indi_list_us01.append(indi)

        # if there is error in both marriage and divorce criteria, only marriage will be listed
        for fam in fam_list:
            if date_greater_than(fam.get_marr_date(), today_date):
                warn_msg = f'Marriage date {fam.get_marr_date(TreeUtils.OUTPUT_DATE_FORMAT)} occurs in future'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US01', fam.id, warn_msg)
                fam_list_us01.append(fam)
            if date_greater_than(fam.get_div_date(), today_date):
                warn_msg = f'Divorce date {fam.get_div_date(TreeUtils.OUTPUT_DATE_FORMAT)} occurs in future'
                fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_FAM, 'US01', fam.id, warn_msg)
                fam_list_us01.append(fam)

        return indi_list_us01 + fam_list_us01

    def us08(self, file_path=None):
        """ returns a list of individuals whose birth date is before parent's marriage date
        or nine months after parent's divorce date
        """
        # self.logger.error(TreeUtils.form_heading('Starting User Story 8', '#', 70))
        file_path = file_path if file_path else get_data_file_path('us08.ged')
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
                warn_msg = f'Birth date {birth_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)} ' \
                    f'is before or on parent\'s marriage date {parent_marr_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)}'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US08', indi.id, warn_msg)
                indi_list_us08_fail.append(indi)
            if date_greater_than(birth_date, add_to_date(parent_div_date, months=9)):
                warn_msg = f'Birth date {birth_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)} ' \
                    f'is more than 9 months after parent\'s divorce date {parent_div_date.strftime(TreeUtils.OUTPUT_DATE_FORMAT)}'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US08', indi.id, warn_msg)
                indi_list_us08_fail.append(indi)

        return indi_list_us08_fail

    def us13(self, file_path=None):
        """ sibling spacing, should be more than 8 months apart """
        file_path = file_path if file_path else get_data_file_path('us13.ged')
        family_tree = TreeLine().process_data(file_path)
        indi_list = family_tree.get_indi_list()
        us13_fail = []
        for indi in indi_list:
            sibling_list = indi.get_siblings(family_tree)
            for sibling in sibling_list:
                date_diff = indi.get_birth_date() - sibling.get_birth_date()
                if 30.4 * 8 >= abs(date_diff.days) >= 2:
                    # TODO f"{today:%B %d, %Y}"
                    warn_msg = f'{indi.name} and {sibling.name} have birth dates {indi.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)}' \
                        f', {sibling.get_birth_date(TreeUtils.OUTPUT_DATE_FORMAT)} less than 8 months and more than 1 day apart'
                    err_id_1 = indi.id
                    err_id_2 = sibling.id
                    # indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US13', indi.id, warn_msg)
                    indi.add_err(TreeError.TYPE_ERROR, 'US13', warn_msg)
            if indi.err or indi.err_list:
                us13_fail.append(indi)

        return us13_fail

    def us19(self, file_path=None):
        """ cousins should not marry """
        file_path = file_path if file_path else get_data_file_path('us08.ged')
        family_tree = TreeLine().process_data(file_path)
        us19_fail = []
        indi_list = family_tree.get_indi_list()
        for indi in indi_list:
            cousin_list = indi.get_cousins(family_tree)
            spouse_list = indi.get_spouses(family_tree)
            common_indi_list = set(cousin_list) & set(spouse_list)
            if common_indi_list:
                for cousin in common_indi_list:
                    warn_msg = f'{indi.name} married first cousin {cousin.name}'
                    # indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US19', indi.id, warn_msg)
                    indi.add_err(TreeError.TYPE_ERROR, 'US19', warn_msg)
            if indi.err or indi.err_list:
                us19_fail.append(indi)

        return us19_fail

    # US26 Corresponding entries
    def us26(self, file_path=None):
        """ All family roles (spouse, child) specified in an individual record should have corresponding entries in
        the corresponding family records. Likewise, all individual roles (spouse, child) specified in family records
        should have corresponding entries in the corresponding individual's records. I.e. the information in the
        individual and family records should be consistent. """
        file_path = file_path if file_path else get_data_file_path('us26.ged')
        family_tree = Tree().grow(file_path)
        us26_fail = []
        indi_list = family_tree.get_indi_list()
        logger = self.logger
        for indi in indi_list:
            # TODO have to add handling for multiple errors on single indi/fam object
            self.check_family_roles(indi, family_tree, us26_fail)
        for fam in family_tree.get_fam_list():
            self.check_indi_roles(fam, family_tree, us26_fail)

        return us26_fail

    def check_indi_roles(self, fam, family_tree, failures):
        logger = self.logger
        husb_id = fam.husb
        wife_id = fam.wife
        chil_id_list = fam.get_children()
        logger.debug(f'checking indi records for [fam: {fam.id}, husb: {husb_id}, wife: {wife_id}, chil: {chil_id_list}]')
        all_indi_ids = get_id_list(family_tree.get_indi_list())
        if husb_id:
            if husb_id in all_indi_ids:
                husb = family_tree.get(husb_id)
                logger.debug(f'{fam.id} husband definition found in record: {husb.id} = {husb.name}')
            else:
                warn_msg = f'{fam.id} husband {husb_id} definition NOT found in record'
                logger.debug(warn_msg)
                fam.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_FAM, 'US26', fam.id, warn_msg)
                failures.append(fam)
        if wife_id:
            if wife_id in all_indi_ids:
                wife = family_tree.get(wife_id)
                logger.debug(f'{fam.id} wife definition found in record: {wife.id} = {wife.name}')
            else:
                warn_msg = f'{fam.id} wife {wife_id} definition NOT found in record'
                logger.debug(warn_msg)
                fam.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_FAM, 'US26', fam.id, warn_msg)
                failures.append(fam)
        if chil_id_list:
            for child_id in chil_id_list:
                if child_id in all_indi_ids:
                    child = family_tree.get(child_id)
                    logger.debug(f'{fam.id} child definition found in record: {child.id} = {child.name}')
                else:
                    warn_msg = f'{fam.id} child {child_id} definition NOT found in record'
                    logger.debug(warn_msg)
                    fam.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_FAM, 'US26', fam.id, warn_msg)
                    failures.append(fam)

    def check_family_roles(self, indi, family_tree, failures):
        logger = self.logger
        logger.debug(f'checking family records for [person: {indi.id} [{indi.name}], famc: {indi.famc}, fams: {indi.fams}]')
        # use getparent and getspouse methods without passing the familytree object, so that it returns the id
        # strings even if they are invalid i.e. not found in the family tree map
        parent_fam_id = indi.get_parent_family()
        spouse_fam_id_list = indi.get_spouse_families()
        children = indi.get_children(family_tree)
        all_fams_ids = get_id_list(family_tree.get_fam_list())
        if parent_fam_id:
            if parent_fam_id in all_fams_ids:
                parent_fam = family_tree.get(parent_fam_id)
                logger.debug(f'{indi.id} parent family definition found in record: {parent_fam.id} = {parent_fam.husb} : {parent_fam.wife}')
            else:
                warn_msg = f'{indi.name} [{indi.id}] parent family [{indi.famc}] definition NOT found in record'
                logger.debug(warn_msg)
                indi.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_INDI, 'US26', indi.id, warn_msg)
                failures.append(indi)
        else:
            logger.debug(f'{indi.id} parent family id not supplied in indi definition')
        if spouse_fam_id_list:
            for spouse_fam_id in spouse_fam_id_list:
                if spouse_fam_id in all_fams_ids:
                    spouse_fam = family_tree.get(spouse_fam_id)
                    logger.debug(f'{indi.id} spouse family definition found in record: {spouse_fam.id} = {spouse_fam.husb} : {spouse_fam.wife}')
                else:
                    warn_msg = f'{indi.name} [{indi.id}] spouse family [{indi.fams}] definition NOT found in record'
                    logger.debug(warn_msg)
                    indi.err = TreeError(TreeError.TYPE_ANOMALY, TreeError.ON_INDI, 'US26', indi.id, warn_msg)
                    failures.append(indi)
        else:
            logger.debug(f'{indi.id} spouse family id not supplied in indi definition')

    def us22(self, file_path=None):
        """ All individual IDs should be unique and all family IDs should be unique """
        file_path = file_path if file_path else get_data_file_path('us22.ged')
        # file_path = get_data_file_path('us22.ged')
        family_tree = Tree(file_path)
        us22_fail = family_tree.duplicate_items
        for item in us22_fail:
            warn_msg = f'duplicate item [{item.id}], {item}'
            err_on = TreeError.ON_INDI if item.tag_name == TreeUtils.INDI else TreeError.ON_FAM
            item.err = TreeError(TreeError.TYPE_ERROR, err_on, 'US22', item.id, warn_msg)
        return us22_fail
