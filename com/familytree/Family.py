class Family:

    def __init__(self, id):
        self.id = self.get_clean_id(id)
        self.marr = None
        self.husb = None
        self.wife = None
        self.chil = []
        self.div = None
        self.tag_name = 'FAM'

    def get_clean_id(self, id):
        if '@' in id:
            return id.replace('@', '')
        return id

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