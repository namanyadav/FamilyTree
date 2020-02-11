from datetime import datetime

from prettytable import PrettyTable

from com.familytree.Individual import Individual
from com.familytree.Family import Family
from com.familytree.Tree import Tree


class TreeLine:

    zero_tags = ["FAM", "INDI", "HEAD", "TRLR", "NOTE"]
    one_tags = ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"]
    two_tags = ['DATE']
    allowed_tags_on_level = {
        '0': zero_tags,
        '1': one_tags,
        '2': two_tags
    }
    all_tags = zero_tags + one_tags + two_tags
    date_print_format = '%Y-%m-%d'

    def __init__(self, input_line=None):
        if input_line:
            split_text = input_line.strip().split(' ', maxsplit=2)
            self.level = split_text[0]
            self.tag_name = self.extract_tag_name(input_line)
            self.arguments = self.extract_arguments(input_line)
            self.is_valid = self.is_valid(input_line)

    def __str__(self):
        return f'<-- {self.level}|{self.tag_name}|{"Y" if self.is_valid else "N"}|{self.arguments}'

    def is_valid(self, input_line):
        if not input_line:
            return False
        if len(input_line.strip()) == 0:
            return False
        split_text = self.split_to_list(input_line)
        if len(split_text) < 2:
            return False
        tag_name = self.get_tag_name()
        level = self.get_level()
        return True if tag_name in self.allowed_tags_on_level.get(level, 'False') else False

    def extract_arguments(self, input_line):
        if not input_line:
            return ''
        if len(input_line) == 0:
            return ''
        split_text = self.split_to_list(input_line)
        tag_name = self.get_tag_name()
        if len(split_text) < 3:
            return ''
        if tag_name in ['FAM', 'INDI']:
            return split_text[1]
        return split_text[2]

    def get_level(self):
        return self.level

    def get_tag_name(self):
        return self.tag_name

    def get_arguments(self):
        return self.arguments

    def split_to_list(self, input_line):
        if not input_line:
            return
        return input_line.strip().split(' ', maxsplit=2)

    def extract_tag_name(self, input_line):
        if not input_line.strip():
            return ''
        split_text = self.split_to_list(input_line)
        # print(split_text)
        if self.get_level() == '0':
            if len(split_text) > 2:
                if split_text[2] in ['FAM', 'INDI']:
                    return split_text[2]

        return split_text[1] if split_text[1] in ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'] else ''

    def print_line(self, input_line):
        if not input_line:
            return
        if len(input_line.strip()) == 0:
            return
        print(f'--> {input_line.strip()}')

    def print_line_info(self, input_line):
        if not input_line:
            return
        if len(input_line.strip()) == 0:
            return
        print(self)

    def generate_info_string(self, input_line):
        if not input_line:
            return ''
        if len(input_line.strip()) == 0:
            return ''
        return f'<-- {self.level}|{self.tag_name}|{self.is_valid}|{self.arguments}'

    def get_tags_of_type(self, tag_name):
        if tag_name and treeline_list:
            tag_list = []
            for treeline in treeline_list:
                if treeline.get_tag_name() == tag_name:
                    tag_list.append(treeline)
            return tag_list
        return

    def print_indi(self):
        for treeline in treeline_list:
            if treeline.get_tag_name() == 'INDI':
                print('start to create Individual object')

    def process_data(self, file_path):
        file = open(file_path, 'r')
        for line in file:
            tl = TreeLine(line)
            # tl.print_line(line)
            # tl.print_line_info(line)
            treeline_list.append(tl)
        return self.generate_indi_objects()

    def generate_indi_objects(self):
        if treeline_list:
            curr_zero_tag = None
            curr_one_tag = None
            curr_obj_map = {}
            processed_tree = Tree()
            for treeline in treeline_list:
                # if the treeline is not valid, skip to the next treeline
                if not treeline.is_valid:
                    # print('treeline not valid, moving to next')
                    continue
                if treeline.get_level() == '0':
                    if curr_zero_tag in curr_obj_map:
                        processed_obj = curr_obj_map[curr_zero_tag]
                        processed_tree.put(processed_obj.id, processed_obj)
                    curr_zero_tag = treeline.get_tag_name()
                    if curr_zero_tag == 'INDI':
                        curr_indi_object = Individual(treeline.get_arguments())
                        curr_obj_map[curr_zero_tag] = curr_indi_object
                    if curr_zero_tag == 'FAM':
                        curr_fam_object = Family(treeline.get_arguments())
                        curr_obj_map[curr_zero_tag] = curr_fam_object

                if treeline.get_level() == '1':
                    if not curr_zero_tag:
                        continue
                    curr_one_tag = treeline.get_tag_name()
                    curr_obj_map[curr_zero_tag].set_attr(treeline.get_tag_name(), treeline)

                if treeline.get_level() == '2':
                    if not curr_one_tag:
                        continue
                    curr_two_tag = treeline.get_tag_name()
                    curr_obj_map[curr_zero_tag].set_attr(curr_one_tag, treeline)

            if curr_zero_tag in ['INDI', 'FAM']:
                if curr_obj_map[curr_zero_tag]:
                    processed_obj = curr_obj_map[curr_zero_tag]
                    processed_tree.put(processed_obj.id, processed_obj)

        return processed_tree

    def get_table_printer(self, table_name, heading_list):
        x = PrettyTable(heading_list)
        x.align[0] = "1"
        x.padding_width = 1
        x.table_name = table_name
        return x

    def process_for_pretty_table(self, type, type_obj, processed_tree):
        if type == 'FAM':
            return self.process_fam_for_table(type_obj, processed_tree)
        if type == 'INDI':
            return self.process_indi_for_table(type_obj, processed_tree)

    def process_fam_for_table(self, type_obj, processed_tree):
        family = processed_tree.get(type_obj.id)
        type_obj.husb_name = processed_tree.get(family.husb).name if processed_tree.contains(family.husb) else 'NA'
        type_obj.wife_name = processed_tree.get(family.wife).name if processed_tree.contains(family.wife) else 'NA'
        type_obj.marr_disp = datetime.strptime(type_obj.marr, Individual.date_format).strftime(TreeLine.date_print_format) if type_obj.marr else 'NA'
        type_obj.div_disp = datetime.strptime(type_obj.div, Individual.date_format).strftime(TreeLine.date_print_format) if type_obj.div else 'NA'
        type_obj.chil_disp = type_obj.chil if type_obj.chil else 'NA'
        type_obj.marr = type_obj.marr if type_obj.marr else 'NA'
        type_obj.div = type_obj.div if type_obj.div else 'NA'
        return type_obj

    def process_indi_for_table(self, type_obj, processed_tree):
        if not processed_tree.get(type_obj.id):
            return type_obj
        indi = processed_tree.get(type_obj.id)
        type_obj.age_disp = indi.get_age() if indi.get_age() else 'NA'
        type_obj.alive_disp = indi.is_alive()
        type_obj.name_disp = type_obj.name if type_obj.name else 'NA'
        type_obj.sex_disp = type_obj.sex if type_obj.sex else 'NA'
        type_obj.deat_disp = datetime.strptime(type_obj.deat, Individual.date_format).strftime(TreeLine.date_print_format) if type_obj.deat else 'NA'
        type_obj.famc_disp = type_obj.famc if type_obj.famc else 'NA'
        type_obj.fams_disp = type_obj.fams if type_obj.fams else 'NA'
        type_obj.birt_disp = datetime.strptime(type_obj.birt, Individual.date_format).strftime(TreeLine.date_print_format) if type_obj.birt else 'NA'
        return type_obj

    def print_fam_table(self, fam_list, processed_tree):
        heading_list = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
        table_printer = self.get_table_printer("FAM", heading_list)
        for fam in fam_list:
            self.process_for_pretty_table('FAM', fam, processed_tree)
            table_printer.add_row([fam.id, fam.marr_disp, fam.div_disp, fam.husb, fam.husb_name, fam.wife, fam.wife_name, fam.chil])

        print(f'Families\n{table_printer}')

    def print_indi_table(self, indi_list, processed_map):
        heading_list = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        table_printer = self.get_table_printer("INDI", heading_list)
        for indi in indi_list:
            self.process_for_pretty_table('INDI', indi, processed_map)
            table_printer.add_row([indi.id, indi.name, indi.sex, indi.birt_disp, indi.age_disp, indi.alive_disp, indi.deat_disp, indi.famc_disp, indi.fams_disp])
        print(f'Individuals\n{table_printer}')

    def pretty_print_table(self, table_name, data_list, processed_tree):
        if table_name == 'INDI':
            self.print_indi_table(data_list, processed_tree)
        if table_name == 'FAM':
            self.print_fam_table(data_list, processed_tree)

    def get_sep_obj_list(self, processed_tree):
        indi_list = []
        fam_list = []
        processed_map = processed_tree.get_tree_map()
        for key in processed_map:
            if processed_map[key].tag_name == 'INDI':
                indi_list.append(processed_map[key])
            else:
                fam_list.append(processed_map[key])

        return [indi_list, fam_list]

    def process_and_print(self, obj_type, processed_tree):
        self.pretty_print_table(obj_type, processed_tree.get_obj_list(obj_type), processed_tree)

    def tabulate(self, processed_tree):
        self.process_and_print('INDI', processed_tree)
        self.process_and_print('FAM', processed_tree)


treeline_list = []
if __name__ == '__main__':
    tree_line = TreeLine()
    processed_tree = tree_line.process_data('./data/Familytree_test_file.ged')
    tree_line.tabulate(processed_tree)

