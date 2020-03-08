from datetime import datetime
from com.familytree.TreeUtils import get_pretty_table_printer


class Tree:

    INPUT_DATE_FORMAT = '%d %b %Y'
    OUTPUT_DATE_FORMAT = '%m/%d/%Y'
    INDI = 'INDI'
    FAM = 'FAM'

    # TODO move gedcom file processing logic here
    def __init__(self):
        self.treemap = {}

    def put(self, key, val):
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

    def get_sorted_list(self, list_type):
        obj_list = []
        for key in self.treemap:
            if self.treemap[key].tag_name == list_type:
                obj_list.append(self.treemap[key])
        obj_list.sort(key=lambda x: x.id)
        return obj_list

    def get_indi_list(self):
        return self.get_sorted_list(Tree.INDI)

    def get_fam_list(self):
        return self.get_sorted_list(Tree.FAM)

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
        heading_list = ["#", "ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        table_printer = get_pretty_table_printer("INDI", heading_list)
        for num, indi in enumerate(self.get_indi_list()):
            self.prepare_indi_for_display(indi)
            table_printer.add_row(
                [num+1, indi.id, indi.name, indi.sex, indi.birt_disp, indi.age_disp, indi.alive_disp, indi.deat_disp,
                 indi.famc_disp, indi.fams_disp])
        # self.logger.error(f'People\n{table_printer}')
        print(f'People\n{table_printer}')

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
        # self.logger.error(f'People\n{table_printer}')
        print(f'People\n{table_printer}')

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
        indi.deat_disp = datetime.strptime(indi.deat, self.INPUT_DATE_FORMAT).strftime(self.OUTPUT_DATE_FORMAT) if indi.deat else 'NA'
        indi.famc_disp = indi.famc if indi.famc else 'NA'
        indi.fams_disp = indi.fams if indi.fams else 'NA'
        indi.birt_disp = datetime.strptime(indi.birt, self.INPUT_DATE_FORMAT).strftime(self.OUTPUT_DATE_FORMAT) if indi.birt else 'NA'
        return indi

    def print_fam_debugging_table(self):
        heading_list = ["#", "ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
        table_printer = get_pretty_table_printer("FAM", heading_list)
        for num, fam in enumerate(self.get_fam_list()):
            self.prepare_fam_for_display(fam)
            table_printer.add_row(
                [num+1, fam.id, fam.marr_disp, fam.div_disp, fam.husb_id_disp, fam.husb_name, fam.wife_id_disp, fam.wife_name,
                 fam.chil])

        # self.logger.error(f'Families\n{table_printer}')
        print(f'Families\n{table_printer}')

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

        # self.logger.error(f'Families\n{table_printer}')
        print(f'Families\n{table_printer}')

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
        fam.marr_disp = datetime.strptime(fam.marr, self.INPUT_DATE_FORMAT).strftime(
            Tree.OUTPUT_DATE_FORMAT) if fam.marr else 'NA'
        fam.div_disp = datetime.strptime(fam.div, self.INPUT_DATE_FORMAT).strftime(
            Tree.OUTPUT_DATE_FORMAT) if fam.div else 'NA'
        fam.chil_disp = fam.chil if fam.chil else 'NA'
        return fam

    def pretty_print(self, debug=False):
        self.print_indi_table(debug)
        self.print_fam_table(debug)
