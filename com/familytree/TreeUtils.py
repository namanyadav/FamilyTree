import sys

from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable
import logging
import os


class TreeUtils:

    logger = None
    INPUT_DATE_FORMAT = '%d %b %Y'
    OUTPUT_DATE_FORMAT = '%m/%d/%Y'
    INDI = 'INDI'
    FAM = 'FAM'

    @staticmethod
    def form_heading(title, char='*', max_length=100):
        char_len = (max_length - len(title)) // 2
        pre = ''
        for x in range(char_len):
            pre += char

        return f'{pre} {title} {pre}'

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
    def print_report_table(report_name, obj_list):
        heading_list = ["ID", "Type", "Warning"]
        table_printer = TreeUtils.get_table_printer(report_name, heading_list)
        for obj in obj_list:
            table_printer.add_row([obj.id, obj.tag_name, obj.warn_msg])

        TreeUtils.logger.error(f'\n{TreeUtils.form_heading(f"Report - {report_name}")}\n{table_printer}')

    @staticmethod
    def print_report(report_name, obj_list):
        logger = TreeUtils.get_logger()
        logger.error(f'\n{TreeUtils.form_heading(f"Report - {report_name}")}\n')
        # print(f'\n{TreeUtils.form_heading(f"Report - {report_name}")}\n')
        for obj in obj_list:
            if obj.err_list:
                # logger.error(f'{obj.id} error list size [{len(obj.err_list)}]')
                for err in obj.err_list:
                    logger.error(err)
            else:
                logger.error(obj.err)

    @staticmethod
    def get_logger():
        if not TreeUtils.logger:
            TreeUtils.init_logger()
        return TreeUtils.logger

    @staticmethod
    def get_log_file_path():
        return os.path.join(os.path.realpath(__file__+'/../../..'), 'logs', 'familytree.log')

    @staticmethod
    def init_logger():
        logging.basicConfig(filename=TreeUtils.get_log_file_path(), level=logging.ERROR)
        # TreeUtils.logger = logging.getLogger('familytree')
        log_file_path = TreeUtils.get_log_file_path()
        # print(log_file_path)
        hdlr = logging.FileHandler(TreeUtils.get_log_file_path())
        # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name) - %(levelname)s - %(message)s')
        hdlr.setFormatter(formatter)
        hdlr = logging.StreamHandler(sys.stdout)
        TreeUtils.logger = logging.getLogger('familytree')
        TreeUtils.logger.addHandler(hdlr)
        # TreeUtils.logger.setLevel(logging.WARNING)
        # TreeUtils.logger.setLevel(logging.WARNING)

    @staticmethod
    def set_logging_level(level):
        if not TreeUtils.logger:
            TreeUtils.init_logger()
        TreeUtils.logger.setLevel(level)


def date_greater_than(date1, date2, allow_eq=False):
    if not date1 or not date2:
        return False
    if allow_eq:
        return ((date1 - date2).total_seconds() > 0) or date_equal_to(date1, date2)
    return (date1 - date2).total_seconds() > 0


def date_equal_to(date1, date2):
    if not date1 or not date2:
        return False
    return (date1 - date2).total_seconds() == 0


def add_to_date(date1, days=0, months=0, years=0):
    if not date1:
        return None
    return date1 + relativedelta(days=days, months=months, years=years)


def get_data_file_path(file_name):
    return os.path.join(os.path.realpath(__file__ + '/../../..'), 'data', file_name)


def print_list(obj_list, list_name=None):
    # print(f'\n{TreeUtils.form_heading(list_name)}')
    for item in obj_list:
        print(item)


def get_log_file_path():
    return os.path.join(os.path.realpath(__file__+'/../../..'), 'logs', 'familytree.log')


def get_id_list(obj_list):
    id_list = []
    for obj in obj_list:
        id_list.append(obj.id)
    return id_list


def get_pretty_table_printer(table_name, heading_list):
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