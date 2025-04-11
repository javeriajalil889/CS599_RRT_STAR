from scipy.spatial import KDTree

class Tree:
    def __init__(self, X):
        self.X = X
        self.V_list = []     # list of vertices
        self.E = {}          # edges: {vertex: parent}
        self.V_count = 0     # number of vertices
        self.kdtree = None   # KDTree, built when needed

    def add_vertex(self, x):
        self.V_list.append(x)
        self.V_count += 1
        self.kdtree = None   # mark KDTree as outdated

    def build_kdtree(self):
        if self.V_list:
            self.kdtree = KDTree(self.V_list)

    def query(self, x, k):
        if self.kdtree is None:
            self.build_kdtree()
        distances, indexes = self.kdtree.query(x, k=k)
        return distances, indexes

    def get_vertex(self, idx):
        return self.V_list[idx]


