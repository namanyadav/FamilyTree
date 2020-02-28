from prettytable import PrettyTable
import logging


class TreeUtils:

    logger = None

    @staticmethod
    def form_heading(title, char='*', max_length=100):
        char_len = (max_length - len(title)) // 2
        pre = ''
        for x in range(char_len):
            pre += char

        return f'{pre} {title} {pre}'

    @staticmethod
    def print_list(list_name, obj_list):
        print(f'\n{TreeUtils.form_heading(list_name)}')
        for item in obj_list:
            print(item)

    @staticmethod
    def get_file_path(user_story):
        return f'../data/{user_story}.ged'

    @staticmethod
    def get_table_printer(table_name, heading_list):
        """
        method to generate a PrettyTable object which can be used to print data in tabulated form
        :param table_name: used as the name of the table to be generated
        :param heading_list: list containing the headers of the table
        :return: preconfigured PrettyTable object
        """
        x = PrettyTable(heading_list)
        x.align[0] = "1"
        x.padding_width = 1
        x.table_name = table_name
        return x

    @staticmethod
    def print_report(report_name, obj_list):
        heading_list = ["ID", "Type", "Warning"]
        table_printer = TreeUtils.get_table_printer(report_name, heading_list)
        for obj in obj_list:
            table_printer.add_row([obj.id, obj.tag_name, obj.warn_msg])

        TreeUtils.logger.error(f'\n{TreeUtils.form_heading(f"Report - {report_name}")}\n{table_printer}')

    @staticmethod
    def get_logger():
        if not TreeUtils.logger:
            TreeUtils.init_logger()
        return TreeUtils.logger

    @staticmethod
    def init_logger():
        TreeUtils.logger = logging.getLogger('familytree')
        hdlr = logging.FileHandler('../logs/familytree.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        TreeUtils.logger.addHandler(hdlr)
        TreeUtils.logger.setLevel(logging.WARNING)

    @staticmethod
    def set_logging_level(level):
        if not TreeUtils.logger:
            TreeUtils.init_logger()
        TreeUtils.logger.setLevel(level)
