class Tree:

    def __init__(self):
        self.treemap = {}

    def put(self, key, val):
        self.treemap[key] = val

    def get(self, key):
        if self.contains(key):
            return self.treemap[key]
        return None

    def contains(self, key):
        if key in self.treemap:
            return True
        return False

    def get_tree_map(self):
        return self.treemap