from com.familytree.Individual import Individual
from com.familytree.Family import Family


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

    def __init__(self, input_line):
        split_text = input_line.strip().split(' ', maxsplit=2)
        # print(split_text)
        self.level = split_text[0]
        self.tag_name = self.extract_tag_name(input_line)
        self.arguments = self.extract_arguments(input_line)
        self.is_valid = 'Y' if self.is_valid(input_line) else 'N'

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

        # new_all_tags = map(lambda x: x if x not in ['FAM', 'INDI'] else False, TreeLine.all_tags)
        # for key in new_all_tags:
        #     print(key)
        # print(f'{input_line}')
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
        info_string = self.generate_info_string(input_line)
        print(info_string)

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

    @staticmethod
    def process_data(file_path):
        file = open(file_path, 'r')
        for line in file:
            tl = TreeLine(line)
            # tl.print_line(line)
            # tl.print_line_info(line)
            treeline_list.append(tl)


    def save_indi_data(self, treeline):

        return

    @staticmethod
    def generate_indi_objects():
        indi_object_list = []
        if treeline_list:
            reading_level_zero = False
            reading_level_one = False
            reading_level_two = False
            reading_indi_data = False
            curr_indi_object = None
            curr_fam_object = None
            date_type_to_set = None
            curr_obj_type = None
            curr_zero_tag = None
            curr_one_tag = None
            curr_two_tag = None
            curr_obj_map = {}
            processed_obj_map = {}
            for treeline in treeline_list:
                print(f'reading treeline: {treeline.get_tag_name()}|{treeline.get_arguments()}|{treeline.is_valid}')
                # if the treeline is not valid, skip to the next treeline
                if treeline.is_valid == 'N':
                    print('treeline not valid, moving to next')
                    continue

                if treeline.get_level() == '0':
                    if curr_zero_tag in curr_obj_map:
                        # indi_object_list.append(curr_obj_map[curr_zero_tag])
                        processed_obj = curr_obj_map[curr_zero_tag]
                        processed_obj_map[processed_obj.id] = processed_obj
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
                    # if treeline.get_tag_name() not in ['BIRT', 'DEAT', 'MARR']:
                    curr_obj_map[curr_zero_tag].set_attr(treeline.get_tag_name(), treeline)

                if treeline.get_level() == '2':
                    if not curr_one_tag:
                        continue
                    curr_two_tag = treeline.get_tag_name()
                    curr_obj_map[curr_zero_tag].set_attr(curr_one_tag, treeline)

            if curr_zero_tag in ['INDI', 'FAM']:
                if curr_obj_map[curr_zero_tag]:
                    # indi_object_list.append(curr_obj_map[curr_zero_tag])
                    processed_obj = curr_obj_map[curr_zero_tag]
                    processed_obj_map[processed_obj.id] = processed_obj



            #     # set of actions if the current level is 0
            #     if treeline.get_level() == '0':
            #         # if current reading level is 0 and reading level one is true, that means the on-going description is over.
            #         # Reset read level one flag to false and store the current object in indi list
            #         if reading_level_one:
            #             reading_level_one = False
            #             if curr_indi_object:
            #                 indi_object_list.append(curr_indi_object)
            #                 curr_indi_object = None
            #         reading_level_zero = True
            #
            #         # if level 0 instantiate a new INDI or FAM object
            #         if treeline.get_tag_name() == 'INDI':
            #             curr_indi_object = Individual(treeline.get_arguments())
            #         if treeline.get_tag_name() == 'FAM':
            #             curr_fam_object = Family(treeline.get_arguments())
            #
            #     # set of actions if the current level is 1
            #     if treeline.get_level() == '1':
            #         if reading_level_zero:
            #             reading_level_one = True
            #             if curr_indi_object:
            #                 if not (treeline.get_tag_name() == 'BIRT' or treeline.get_tag_name() == 'DEAT'):
            #                     curr_indi_object.set_attr(treeline.get_tag_name(), treeline)
            #                 else:
            #                     date_type_to_set = treeline.get_tag_name()
            #         else:
            #             continue
            #     if treeline.get_level() == '2':
            #         if reading_level_one:
            #             reading_level_two = True
            #             print(f'reading level 2, date type should be set {date_type_to_set}')
            #             if curr_indi_object:
            #                 if date_type_to_set:
            #                     curr_indi_object.set_attr(date_type_to_set, treeline)
            #         else:
            #             continue
            #
            # if reading_level_zero:
            #     print('reading indi flag was true but reached end of file, so setting reading indi flag to False')
            #     if curr_indi_object:
            #         indi_object_list.append(curr_indi_object)
            #     reading_indi_data = False
            #     curr_indi_object = None
            #     # print(len(indi_object_list))

        return processed_obj_map

    @staticmethod
    def generate_indi_objects_workds():
        indi_object_list = []
        if treeline_list:
            reading_level_zero = False
            reading_level_one = False
            reading_level_two = False
            reading_indi_data = False
            curr_indi_object = None
            curr_fam_object = None
            date_type_to_set = None
            for treeline in treeline_list:
                print(f'reading treeline: {treeline.get_tag_name()}|{treeline.get_arguments()}')
                # if the treeline is not valid, skip to the next treeline
                if treeline.is_valid == 'N':
                    print('treeline not valid, moving to next')
                    continue

                # set of actions if the current level is 0
                if treeline.get_level() == '0':
                    # if current reading level is 0 and reading level one is true, that means the on-going description is over.
                    # Reset read level one flag to false and store the current object in indi list
                    if reading_level_one:
                        reading_level_one = False
                        if curr_indi_object:
                            indi_object_list.append(curr_indi_object)
                            curr_indi_object = None
                    reading_level_zero = True

                    # if level 0 instantiate a new INDI or FAM object
                    if treeline.get_tag_name() == 'INDI':
                        curr_indi_object = Individual(treeline.get_arguments())
                    if treeline.get_tag_name() == 'FAM':
                        curr_fam_object = Family(treeline.get_arguments())

                # set of actions if the current level is 1
                if treeline.get_level() == '1':
                    if reading_level_zero:
                        reading_level_one = True
                        if curr_indi_object:
                            if not (treeline.get_tag_name() == 'BIRT' or treeline.get_tag_name() == 'DEAT'):
                                curr_indi_object.set_attr(treeline.get_tag_name(), treeline)
                            else:
                                date_type_to_set = treeline.get_tag_name()
                    else:
                        continue
                if treeline.get_level() == '2':
                    if reading_level_one:
                        reading_level_two = True
                        print(f'reading level 2, date type should be set {date_type_to_set}')
                        if curr_indi_object:
                            if date_type_to_set:
                                curr_indi_object.set_attr(date_type_to_set, treeline)
                    else:
                        continue

            if reading_level_zero:
                print('reading indi flag was true but reached end of file, so setting reading indi flag to False')
                if curr_indi_object:
                    indi_object_list.append(curr_indi_object)
                reading_indi_data = False
                curr_indi_object = None
                # print(len(indi_object_list))

        return indi_object_list


    def splitandprint(self, line):
        print(line)


# TreeLine.process_data = staticmethod(TreeLine.process_data)
# TreeLine.generate_indi_objects = staticmethod(TreeLine.generate_indi_objects)
treeline_list = []
# print("hello1")
# print(__name__)
if __name__ == '__main__':
    # print("hello")
    # input_line = '1 NAME Terry /Bull/ its a beautiful day'
    TreeLine.process_data('./data/Familytree_test_file.ged')
    processed_map = TreeLine.generate_indi_objects()
    for key in processed_map:
        print(processed_map[key])
    # for indi in indi_list:
    #     print(indi)
    # print(indi_list.pop())

    # tl = TreeLine(input_line)
    # tl.print_line(input_line)
    # tl.print_line_info(input_line)
