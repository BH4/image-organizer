class disjoint_sets:
    def __init__(self):
        self.sets = []
        self.size = 0

    def union(self, a, b):  # union by size
        # Returns bool indicating if Union was preformed
        rootA = self.find(a)
        rootB = self.find(b)

        if rootA == rootB:
            return False  # union was not preformed

        # Set size is negative the number of elements of the set
        new_size = self.sets[rootA]+self.sets[rootB]

        # rootA has more elements
        if self.sets[rootA] < self.sets[rootB]:
            self.sets[rootB] = rootA
            self.sets[rootA] = new_size
        else:  # B has more or same
            self.sets[rootA] = rootB
            self.sets[rootB] = new_size

        self.size -= 1

        return True  # union was preformed

    def find(self, a):
        """
        Finds root of element with id 'a'

        Make the parents of this node the root in order to decrease tree height
        """

        parent = self.sets[a]
        if parent < 0:
            return a

        root = self.find(parent)

        self.sets[a] = root

        return root

    def add(self):
        self.sets.append(-1)
        self.size += 1
