# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
import numpy as np

from rrt_algorithms.rrt.rrt_star import RRTStar
from rrt_algorithms.search_space.search_space import SearchSpace
from rrt_algorithms.utilities.plotting import Plot

X_dimensions = np.array([(0, 100), (0, 100)])  # dimensions of Search Space
# obstacles
Obstacles = np.array([(20, 20, 40, 40), (20, 60, 40, 80),
                     (60, 20, 80, 40), (60, 60, 80, 80)])
x_init = (0, 0)  # starting location
x_goal = (100, 100)  # goal location

q = 8  # length of tree edges
r = 1  # length of smallest edge to check for intersection with obstacles
max_samples = 1024  # max number of samples to take before timing out
rewire_count = 32  # optional, number of nearby branches to rewire
prc = 0.1  # probability of checking for a connection to goal

# create Search Space
X = SearchSpace(X_dimensions, Obstacles)

# create rrt_search
rrt = RRTStar(X, q, x_init, x_goal, max_samples, r, prc, rewire_count)
path = rrt.rrt_star()

# plot
plot = Plot("rrt_star_2d")
plot.plot_tree(X, rrt.trees)
if path is not None:
    plot.plot_path(X, path)
plot.plot_obstacles(X, Obstacles)
plot.plot_start(X, x_init)
plot.plot_goal(X, x_goal)
plot.draw(auto_open=True)




# connect_shortest_valid(self, tree, x_new, L_near):
        """
        Connect to nearest vertex that has an unobstructed path
        :param tree: int, tree being added to
        :param x_new: tuple, vertex being added
        :param L_near: list of nearby vertices
        """

def test_connect_shortest_valid():
    X_dimensions = np.array([(0, 100), (0, 100)])  
    Obstacles = np.array([(20, 20, 40, 40), (20, 60, 40, 80),
                     (60, 20, 80, 40), (60, 60, 80, 80)])
    x_init = (0, 0)  
    x_goal = (100, 100) 

    q = 8  
    r = 1  
    max_samples = 1024  
    rewire_count = 32  
    prc = 0.1  

    X = SearchSpace(X_dimensions, Obstacles)
    rrt_star = RRTStar(X, q, x_init, x_goal, max_samples, r, prc, rewire_count)

    tree=0
    x_new=(50,50)
    L_near=[(1, (30,30)), (2, (40,40)), (3, (45,45))] 

    times=[]
    for _ in range(1000):
        start=time.perf_counter()
        rrt_star.connect_shortest_valid(tree,x_new, L_near)
        times.append(time.perf_counter()-start)
    plot_graph(times, "connect_shortest_valid()")
