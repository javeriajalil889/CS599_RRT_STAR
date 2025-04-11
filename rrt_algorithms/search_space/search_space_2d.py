# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import numpy as np
from rtree import index

from rrt_algorithms.utilities.geometry import es_points_along_line
from rrt_algorithms.utilities.obstacle_generation import obstacle_generator


class SearchSpace(object):
    def __init__(self, dimension_lengths, O=None):
        """
        Initialize Search Space
        :param dimension_lengths: list of (min, max) tuples for each dimension
        :param O: list of obstacles (optional)
        """
        if len(dimension_lengths) < 2:
            raise Exception("Must have at least 2 dimensions")
        if any(len(i) != 2 for i in dimension_lengths):
            raise Exception("Dimensions can only have a start and end")
        if any(i[0] >= i[1] for i in dimension_lengths):
            raise Exception("Dimension start must be less than dimension end")

        self.dimensions = len(dimension_lengths)
        self.dimension_lengths = np.array(dimension_lengths)  # ✅ Fix: convert to NumPy array

        p = index.Property()
        p.dimension = self.dimensions

        if O is None:
            self.obs = index.Index(interleaved=True, properties=p)
        else:
            if any(len(o) / 2 != self.dimensions for o in O):
                raise Exception("Obstacle has incorrect dimension definition")
            if any(o[i] >= o[int(i + len(o) / 2)] for o in O for i in range(int(len(o) / 2))):
                raise Exception("Obstacle start must be less than obstacle end")
            self.obs = index.Index(obstacle_generator(O), interleaved=True, properties=p)

    def sample(self):
        """
        Return a random location within X (not necessarily obstacle-free)
        :return: tuple of random coordinates
        """
        x = np.random.uniform(self.dimension_lengths[:, 0], self.dimension_lengths[:, 1])
        return tuple(x)

    def sample_free(self):
        """
        Sample a location within X_free (outside obstacles)
        :return: valid sample location
        """
        while True:
            x = self.sample()
            if self.obstacle_free(x):
                return x

    def obstacle_free(self, x):
        """
        Check if a location resides inside of an obstacle
        :param x: location to check (tuple)
        :return: True if not inside an obstacle, False otherwise
        """
        return self.obs.count(x) == 0

    def collision_free(self, start, end, r):
        """
        Check if a line segment intersects any obstacle
        :param start: starting point of line (tuple)
        :param end: ending point of line (tuple)
        :param r: resolution of sampling along the edge
        :return: True if no collision, False otherwise
        """
        points = es_points_along_line(start, end, r)
        return all(map(self.obstacle_free, points))

