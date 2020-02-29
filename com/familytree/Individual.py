from datetime import datetime


class Individual:

    date_format = '%d %b %Y'

    def __init__(self, id):
        self.id = self.get_clean_id(id)
        self.name = None
        self.sex = None
        self.birt = None
        self.deat = None
        self.famc = None
        self.fams = []
        self.tag_name = 'INDI'

    def get_id(self):
        return self.id

    def get_birth_date(self, output_format=None):
        if not self.birt:
            return None
        date = datetime.strptime(self.birt, Individual.date_format)
        if output_format:
            return date.strftime(output_format)
        return date

    def get_death_date(self, output_format=None):
        if not self.deat:
            return None
        date = datetime.strptime(self.deat, Individual.date_format)
        if output_format:
            return date.strftime(output_format)
        return date

    # get a cleaned up version of the id
    def get_clean_id(self, id):
        if '@' in id:
            return id.replace('@', '')
        return id

    def set_name(self, name):
        self.name = name

    def set_sex(self, sex):
        self.sex = sex

    def set_birth_date(self, date):
        self.birt = date

    def set_death_date(self, date):
        self.deat = date

    def set_parent_family(self, family_id):
        self.famc = self.get_clean_id(family_id)

    def set_spouse_family(self, family_id):
        self.fams.append(self.get_clean_id(family_id))

    def get_age(self, target_date=None):
        if target_date:
            ref_date = target_date
            birth_date = datetime.strptime(self.birt, Individual.date_format)
            age = ref_date.year - birth_date.year - (
                        (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day))
            return age
        # If indi does not have a birth date, return -1
        if not self.birt:
            return None
        # if individual is alive, return his current age.
        # If indi dead, return his age at death.
        ref_date = datetime.today() if self.is_alive() else datetime.strptime(self.deat, Individual.date_format)
        birth_date = datetime.strptime(self.birt, Individual.date_format)
        age = ref_date.year - birth_date.year - ((ref_date.month, ref_date.day) < (birth_date.month, birth_date.day))
        return age

    def is_alive(self):
        if self.deat:
            return False
        return True

    def set_attr(self, prop_name, treeline):

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

    def __str__(self):
        return f'{self.tag_name}|{self.id}|{self.name}|{self.sex}|{self.birt}|{self.deat}|{self.famc}|{self.fams}'
