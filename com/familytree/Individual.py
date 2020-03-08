from datetime import datetime
from com.familytree.Tree import Tree
from com.familytree.TreeError import TreeError


class Individual:

    date_format = '%d %b %Y'

    def __init__(self, id, src_file=None):
        self.id = self.get_clean_id(id)
        self.name = None
        self.sex = None
        self.birt = None
        self.deat = None
        self.famc = None
        self.fams = []
        self.err = None
        self.tag_name = Tree.INDI
        self.src_file = src_file

    def get_id(self):
        return self.id

    def get_birth_date(self, output_format=None):
        """
        returns birth date if present as datetime object if no output_format specified
        returns birth date string if present and output_format given
        """
        if not self.birt:
            return None
        date = datetime.strptime(self.birt, Tree.INPUT_DATE_FORMAT)
        if output_format:
            return date.strftime(output_format)
        return date

    def get_death_date(self, output_format=None):
        """
        returns death date if present as datetime object if no output_format specified
        returns deat date string if present and output_format given
        """
        if not self.deat:
            return None
        date = datetime.strptime(self.deat, Tree.INPUT_DATE_FORMAT)
        if output_format:
            return date.strftime(output_format)
        return date

    def get_parent_marr_date(self, family_tree):
        """ returns marriage date of parents as datetime if present, None otherwise """
        return family_tree.get(self.famc).get_marr_date() if family_tree.get(self.famc) else None

    def get_parent_div_date(self, family_tree):
        """ returns divorce date of parents as datetime if present, None otherwise """
        return family_tree.get(self.famc).get_div_date() if family_tree.get(self.famc) else None

    def get_children(self, family_tree):
        """ returns all children of a person with current and ex partner """
        spouse_fam_list = self.get_spouse_families(family_tree)
        children = []
        for spouse_fam in spouse_fam_list:
            children.extend(spouse_fam.get_children(family_tree))
        return children

    def get_father(self, family_tree):
        """ returns the father of person as Individual object if present, None otherwise """
        parent_fam = self.get_parent_family(family_tree)
        if not parent_fam:
            return None
        if not family_tree:
            return parent_fam
        return family_tree.get(parent_fam.husb)

    def get_mother(self, family_tree):
        """ returns the mother of person as Individual object if present, None otherwise """
        parent_fam = self.get_parent_family(family_tree)
        if not parent_fam:
            return None
        if not family_tree:
            return parent_fam
        return family_tree.get(parent_fam.wife)

    def get_cousins(self, family_tree):
        """ returns a list of Individual objects who are first cousins of person if present, an empty list otherwise """
        # get both parents
        # get all siblings of both parents
        # get all children of all siblings
        father, mother = self.get_father(family_tree), self.get_mother(family_tree)
        father_siblings = father.get_siblings(family_tree) if father else []
        mother_siblings = mother.get_siblings(family_tree) if mother else []
        cousins = []
        for sibling in father_siblings:
            cousins.extend(sibling.get_children(family_tree))
        for sibling in mother_siblings:
            cousins.extend(sibling.get_children(family_tree))

        return cousins

    def get_spouse_families(self, family_tree=None):
        """ returns a list of spouse families if present, an empty list otherwise """
        if not family_tree:
            return self.fams
        families = []
        for fam_id in self.fams:
            families.append(family_tree.get(fam_id))
        return families

    def get_spouses(self, family_tree):
        """ returns a list of all spouses, both current and ex, of a person """
        spouse_families = self.get_spouse_families(family_tree)
        spouses = []
        for family in spouse_families:
            husband = family.get_husb(family_tree)
            wife = family.get_wife(family_tree)
            spouses.append(husband) if husband.id != self.id else spouses.append(wife)

        return spouses

    def get_siblings(self, family_tree):
        """ returns a list of siblings of a person if present, en empty list otherwise """
        # get parent family
        # get each partner (ex and current) of both husband and wife
        # for each partner get a list of fams
        # for each fams element get all chil

        # if parent family None then no siblings can be found
        parent_family = self.get_parent_family(family_tree)
        if not parent_family:
            return []

        husb = parent_family.get_husb(family_tree)
        wife = parent_family.get_wife(family_tree)

        # get all spouse families (current and ex) of husband and wife and add them to a set
        spouse_fam_set = set()
        spouse_fam_set.update(husb.get_spouse_families(family_tree) if husb else [])
        spouse_fam_set.update(wife.get_spouse_families(family_tree) if wife else [])

        # iterate on all collected families and get children in them
        sibling_list = []
        # TODO can use lambda
        for fam in spouse_fam_set:
            sibling_list.extend(fam.get_children(family_tree))

        # remove the individual itself from the list, cannot be his own sibling
        sibling_list.remove(self) if sibling_list else sibling_list

        return sibling_list

    def get_siblings_temp(self, family_tree):
        # get parent family
        # get each partner (ex and current) of both husband and wife
        # for each partner get a list of fams
        # for each fams element get all chil

        sibling_list = self.get_parent_family(family_tree).get_children(family_tree) if self.get_parent_family(family_tree) else []
        sibling_list.remove(self) if sibling_list else sibling_list
        return sibling_list

    def get_parent_family(self, family_tree=None):
        """ returns the parent family of a person """
        if not family_tree:
            return self.famc
        return family_tree.get(self.famc)

    def add_error(self, us_name, err_msg):
        self.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, us_name, self.id, err_msg)

    # get a cleaned up version of the id
    @staticmethod
    def get_clean_id(id):
        """ to clean up id string before saving """
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
        """ returns the date of individual today if alive,
        ff dead, returns the age at death """
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