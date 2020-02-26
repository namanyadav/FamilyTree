class Tree:

    INPUT_DATE_FORMAT = '%d %b %Y'
    OUTPUT_DATE_FORMAT = '%m/%d/%Y'

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
