from datetime import datetime

from com.familytree.Family import Family
from com.familytree.Individual import Individual
from com.familytree.TreeLine import TreeLine
from com.familytree.TreeUtils import get_pretty_table_printer, TreeUtils


class Tree:

    logger = TreeUtils.get_logger()

    # TODO move gedcom file processing logic here
    def __init__(self, fp=None):
        self.treemap = {}
        self.duplicate_items = []
        self.src_file = fp if fp else None
        self.grow(fp) if fp else None

    def put(self, key, val):
        if key in self.treemap.keys():
            self.logger.info(f'duplicate id found. overwriting previous record: [{key} : {val}]')
            self.duplicate_items.append(self.treemap[key])
        self.treemap[key] = val

    def get(self, key):
        if not key:
            return None
        if self.contains(key.upper()):
            return self.treemap[key.upper()]
        return None

    def contains(self, key):
        if key in self.treemap:
            return True
        return False

    def grow(self, file_path):
        """
        opens the gedcom file, reads each line, creates treeline object for each line
        and returns a list of all treeline objects
        :param file_path: location of gedcom file to be used as input
        :return: list of all treeline objects created from the supplied gedcom file
            """

        self.logger.debug(f'generating tree from ... {file_path}')
        file = open(file_path, 'r')
        self.src_file = file_path
        with file:
            treeline_list = []
            for line_ind, line in enumerate(file):
                self.logger.debug(f'reading line {line_ind+1}: {line.strip()}')
                tl = TreeLine(line, line_ind, line_ind, file_path)
                # tl.print_line(line)
                # tl.print_line_info(line)
                treeline_list.append(tl)
            return self.generate_tree(treeline_list)

    # TODO can add state machine
    def generate_tree(self, treeline_list):
        logger = self.logger
        logger.debug(f'inside generate_tree, treeline_list size: {len(treeline_list)}')
        if treeline_list:
            curr_zero_tag = None
            curr_one_tag = None
            curr_obj_map = {}
            # iterate over all treeline objects
            for treeline in treeline_list:
                logger.debug(f'reading treeline[id:{treeline.id}:] object: {treeline}')
                # if the treeline is not valid, skip to the next treeline
                if not treeline.is_valid:
                    logger.debug(f'treeline[id:{treeline.id}:] not valid, moving to next: {treeline}')
                    continue
                if treeline.get_level() == '0':
                    # if current line level is 0 and if code was already reading something
                    logger.debug(f'treeline[id:{treeline.id}:] level 0 found')
                    if curr_zero_tag in curr_obj_map:
                        processed_obj = curr_obj_map[curr_zero_tag]
                        logger.debug(f'treeline[id:{treeline.id}:] going to save [{curr_zero_tag}] {processed_obj}')
                        self.put(processed_obj.id, processed_obj)
                    curr_zero_tag = treeline.get_tag_name()
                    if curr_zero_tag == 'INDI':
                        curr_indi_object = Individual(treeline.get_arguments(), treeline.src_file)
                        logger.debug(f'treeline[id:{treeline.id}:] initialize new object [{curr_zero_tag}] {curr_indi_object}')
                        curr_obj_map[curr_zero_tag] = curr_indi_object
                    if curr_zero_tag == 'FAM':
                        curr_fam_object = Family(treeline.get_arguments(), treeline.src_file)
                        logger.debug(f'treeline[id:{treeline.id}:] initialize new object [{curr_zero_tag}] {curr_fam_object}')
                        curr_obj_map[curr_zero_tag] = curr_fam_object
                    # else:
                    #     logger.debug(f'treeline[id:{treeline.id}:] tag can be skipped [{treeline.get_tag_name()}] {treeline}')

                if treeline.get_level() == '1':
                    logger.debug(f'treeline[id:{treeline.id}:] level 1 found')
                    if not curr_zero_tag:
                        logger.debug(f'treeline[id:{treeline.id}:] something wrong. '
                                     f'no curr_zero_tag found before trying to read level 1. skipping this line.')
                        continue
                    curr_one_tag = treeline.get_tag_name()
                    logger.debug(f'treeline[id:{treeline.id}:] setting attribute [{treeline.get_tag_name()}, {treeline.get_arguments()}]')
                    curr_obj_map[curr_zero_tag].set_attr(treeline.get_tag_name(), treeline)

                if treeline.get_level() == '2':
                    logger.debug(f'treeline[id:{treeline.id}:] level 2 found')
                    if not curr_one_tag:
                        logger.debug(f'treeline[id:{treeline.id}:] something wrong. '
                                     f'trying to read level 2 without setting curr_one_tag. skipping this line.')
                        continue
                    curr_two_tag = treeline.get_tag_name()
                    logger.debug(f'treeline[id:{treeline.id}:] setting attribute [{curr_one_tag}, {treeline.get_arguments()}]')
                    curr_obj_map[curr_zero_tag].set_attr(curr_one_tag, treeline)

            if curr_zero_tag in ['INDI', 'FAM']:
                if curr_obj_map[curr_zero_tag]:
                    processed_obj = curr_obj_map[curr_zero_tag]
                    logger.debug(f'treeline[id:{treeline.id}:] going to save [{curr_zero_tag}] {processed_obj}')
                    self.put(processed_obj.id, processed_obj)

        return self

    def get_sorted_list(self, list_type):
        obj_list = []
        for key in self.treemap:
            if self.treemap[key].tag_name == list_type:
                obj_list.append(self.treemap[key])
        obj_list.sort(key=lambda x: x.id)
        return obj_list

    def get_indi_list(self):
        return self.get_sorted_list(TreeUtils.INDI)

    def get_fam_list(self):
        return self.get_sorted_list(TreeUtils.FAM)

    def get_parents(self, indi_id):
        if not indi_id:
            return None
        if not self.treemap:
            return None
        indi = self.treemap.get(indi_id)
        # famc = indi.famc
        family = self.treemap.get(indi.famc)
        return family.husb, family.wife

    def get_tree_map(self):
        return self.treemap

    def print_indi_debugging_table(self):
        heading_list = ["#", "ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse", "Source"]
        table_printer = get_pretty_table_printer("INDI", heading_list)
        for num, indi in enumerate(self.get_indi_list()):
            self.prepare_indi_for_display(indi)
            table_printer.add_row(
                [num+1, indi.id, indi.name, indi.sex, indi.birt_disp, indi.age_disp, indi.alive_disp, indi.deat_disp,
                 indi.famc_disp, indi.fams_disp, indi.src_file])
        self.logger.error(f'People [{self.src_file}]\n{table_printer}')
        # print(f'People\n{table_printer}')

    def print_indi_table(self, debug=False):
        if debug:
            self.print_indi_debugging_table()
            return
        heading_list = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        table_printer = get_pretty_table_printer("INDI", heading_list)
        for indi in self.get_indi_list():
            self.prepare_indi_for_display(indi)
            table_printer.add_row(
                [indi.id, indi.name, indi.sex, indi.birt_disp, indi.age_disp, indi.alive_disp, indi.deat_disp,
                 indi.famc_disp, indi.fams_disp])
        self.logger.error(f'People [{self.src_file}]\n{table_printer}')
        # print(f'People\n{table_printer}')

    def prepare_indi_for_display(self, indi):
        """
        helper method to process Individual object for displaying in table
        :param indi: the actual data object to be printed
        :param processed_tree: the Tree object containing the complete family tree
        :return: not required at the moment
        """
        if not self.get(indi.id):
            return indi
        indi = self.get(indi.id)
        indi.age_disp = indi.get_age() if indi.get_age() else 'NA'
        indi.alive_disp = indi.is_alive()
        indi.name_disp = indi.name if indi.name else 'NA'
        indi.sex_disp = indi.sex if indi.sex else 'NA'
        indi.deat_disp = datetime.strptime(indi.deat, TreeUtils.INPUT_DATE_FORMAT).strftime(TreeUtils.OUTPUT_DATE_FORMAT) if indi.deat else 'NA'
        indi.famc_disp = indi.famc if indi.famc else 'NA'
        indi.fams_disp = indi.fams if indi.fams else 'NA'
        indi.birt_disp = datetime.strptime(indi.birt, TreeUtils.INPUT_DATE_FORMAT).strftime(TreeUtils.OUTPUT_DATE_FORMAT) if indi.birt else 'NA'
        return indi

    def print_fam_debugging_table(self):
        heading_list = ["#", "ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children", "Source"]
        table_printer = get_pretty_table_printer("FAM", heading_list)
        for num, fam in enumerate(self.get_fam_list()):
            self.prepare_fam_for_display(fam)
            table_printer.add_row(
                [num+1, fam.id, fam.marr_disp, fam.div_disp, fam.husb_id_disp, fam.husb_name, fam.wife_id_disp, fam.wife_name,
                 fam.chil, fam.src_file])

        self.logger.error(f'Families [{self.src_file}]\n{table_printer}')
        # print(f'Families\n{table_printer}')

    def print_fam_table(self, debug=False):
        if debug:
            self.print_fam_debugging_table()
            return
        heading_list = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
        table_printer = get_pretty_table_printer("FAM", heading_list)
        for fam in self.get_fam_list():
            self.prepare_fam_for_display(fam)
            table_printer.add_row(
                [fam.id, fam.marr_disp, fam.div_disp, fam.husb_id_disp, fam.husb_name, fam.wife_id_disp, fam.wife_name,
                 fam.chil])

        self.logger.error(f'Families [{self.src_file}]\n{table_printer}')
        # print(f'Families\n{table_printer}')

    def prepare_fam_for_display(self, fam):
        """
        helper method to process Family object for displaying in table
        :param fam: the actual data object to be printed
        :param family_tree: the Tree object containing the complete family tree
        :return: not required at the moment
        """
        family = self.get(fam.id)
        fam.husb_id_disp = family.husb if family.husb else 'NA'
        fam.wife_id_disp = family.wife if family.wife else 'NA'
        fam.husb_name = self.get(family.husb).name if self.contains(family.husb) else 'NA'
        fam.wife_name = self.get(family.wife).name if self.contains(family.wife) else 'NA'
        fam.marr_disp = datetime.strptime(fam.marr, TreeUtils.INPUT_DATE_FORMAT).strftime(
            TreeUtils.OUTPUT_DATE_FORMAT) if fam.marr else 'NA'
        fam.div_disp = datetime.strptime(fam.div, TreeUtils.INPUT_DATE_FORMAT).strftime(
            TreeUtils.OUTPUT_DATE_FORMAT) if fam.div else 'NA'
        fam.chil_disp = fam.chil if fam.chil else 'NA'
        return fam

    def pretty_print(self, debug=False):
        self.print_indi_table(debug)
        self.print_fam_table(debug)

    def print(self):
        self.pretty_print()
