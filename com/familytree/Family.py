from datetime import datetime
from com.familytree.Tree import Tree


class Family:

    def __init__(self, id, src_file=None):
        self.id = self.get_clean_id(id)
        self.marr = None
        self.husb = None
        self.wife = None
        self.chil = []
        self.div = None
        self.tag_name = Tree.FAM
        self.src_file = src_file

    @staticmethod
    def get_clean_id(id):
        if '@' in id:
            return id.replace('@', '')
        return id

    def get_id(self):
        return id

    def get_marr_date(self, output_format=None):
        if not self.marr:
            return None
        date = datetime.strptime(self.marr, Tree.INPUT_DATE_FORMAT)
        if output_format:
            return date.strftime(output_format)
        return date

    def get_div_date(self, output_format=None):
        if not self.div:
            return None
        date = datetime.strptime(self.div, Tree.INPUT_DATE_FORMAT)
        if output_format:
            return date.strftime(output_format)
        return date

    def get_husb(self, family_tree=None):
        return family_tree.get(self.husb) if family_tree else self.husb

    def get_wife(self, family_tree=None):
        return family_tree.get(self.wife) if family_tree else self.wife

    def get_husb_death_date(self, family_tree):
        return family_tree.get(self.husb).get_death_date() if family_tree.get(self.husb) else None

    def get_wife_death_date(self, family_tree):
        return family_tree.get(self.wife).get_death_date() if family_tree.get(self.wife) else None

    def get_children(self, family_tree=None):
        # TODO can use lambda :D
        if not family_tree:
            return self.chil
        children = []
        for indi_id in self.chil:
            children.append(family_tree.get(indi_id))
        return children

    def set_marr(self, date):
        self.marr = date

    def set_husb(self, husb_id):
        self.husb = self.get_clean_id(husb_id)

    def set_wife(self, wife_id):
        self.wife = self.get_clean_id(wife_id)

    def set_chil(self, chil_id):
        self.chil.append(self.get_clean_id(chil_id))

    def set_div(self, date):
        self.div = date

    def set_attr(self, prop_name, treeline):
        if prop_name == 'MARR':
            self.set_marr(treeline.get_arguments())
        if prop_name == 'HUSB':
            self.set_husb(treeline.get_arguments())
        if prop_name == 'WIFE':
            self.set_wife(treeline.get_arguments())
        if prop_name == 'CHIL':
            self.set_chil(treeline.get_arguments())
        if prop_name == 'DIV':
            self.set_div(treeline.get_arguments())

    def __str__(self):
        return f'{self.tag_name}|{self.id}|{self.marr}|{self.husb}|{self.wife}|{self.chil}|{self.div}'