class Individual:

    def __init__(self, id):
        self.id = id
        self.name = None
        self.sex = None
        self.birt = None
        self.deat = None
        self.famc = None
        self.fams = None
        self.tag_name = 'INDI'

    def set_name(self, name):
        self.name = name

    def set_sex(self, sex):
        self.sex = sex

    def set_birth_date(self, date):
        self.birt = date

    def set_death_date(self, date):
        self.deat = date

    def set_parent_family(self, family_id):
        self.famc = family_id

    def set_spouse_family(self, family_id):
        self.fams = family_id

    def set_attr(self, prop_name, treeline):
        # print(f'{self.id} setting attribute {prop_name} to {treeline.get_arguments()}')
        # switcher = {
        #     'NAME': self.set_name(treeline.get_arguments()),
        #     'SEX': self.set_sex(treeline.get_arguments()),
        #     'BIRT': self.set_birth_date(treeline.get_arguments()),
        #     'DEAT': self.set_death_date(treeline.get_arguments()),
        #     'FAMC': self.set_parent_family(treeline.get_arguments()),
        #     'FAMS': self.set_spouse_family(treeline.get_arguments())
        # }
        #
        # switcher.get(prop_name)

        if prop_name == 'NAME':
            self.set_name(treeline.get_arguments())
        if prop_name == 'SEX':
            self.set_sex(treeline.get_arguments())
        if prop_name == 'BIRT':
            self.set_birth_date(treeline.get_arguments())
        if prop_name == 'DEAT':
            self.set_death_date(treeline.get_arguments())
        if prop_name == 'FAMC':
            self.set_parent_family(treeline.get_arguments())
        if prop_name == 'FAMS':
            self.set_spouse_family(treeline.get_arguments())

        # print(self)

    def __str__(self):
        return f'{self.tag_name}|{self.id}|{self.name}|{self.sex}|{self.birt}|{self.deat}|{self.famc}|{self.fams}'
