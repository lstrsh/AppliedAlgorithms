class Set:
    def __init__(self):
        self.lst = []

    def insert(self, x):
        if not self.search(x):
            self.lst.append(x)

    def delete(self, x):
        if self.search(x):
            self.lst.remove(x)

    def search(self, x):
        return 1 if x in self.lst else 0

    def clear(self):
        self.lst.clear()

    def union(self, other):
        new_set = Set()
        for x in self.lst:
            new_set.insert(x)
        for x in other.lst:
            new_set.insert(x)
        return new_set

    def intersection(self, other):
        new_set = Set()
        for x in self.lst:
            if x in other.lst:
                new_set.insert(x)
        return new_set

    def set_difference(self, other):
        new_set = Set()
        for x in self.lst:
            if x not in other.lst:
                new_set.insert(x)
        return new_set

    def sym_difference(self, other):
        new_set = Set()
        for x in self.lst:
            if x not in other.lst:
                new_set.insert(x)
        for x in other.lst:
            if x not in self.lst:
                new_set.insert(x)
        return new_set

    def is_subset(self, other):
        for x in self.lst:
            if x not in other.lst:
                return False
        return True

    def __str__(self):
        return str(self.lst)
