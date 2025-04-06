import time
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
from rrt_algorithms.rrt.rrt_star import RRTStar


class MockTree:
    def __init__(self):
        self.V_count = 5
        self.E = {
            (2, 2): (0, 0),
            (3, 3): (2, 2),
            (4, 4): (3, 3)
        }


class MockSearchSpace:
    def __init__(self):
        self.dimensions = 2

    def collision_free(self, point1, point2, resolution):
        return True


def plot_graph(times, title):
    mean_time = np.mean(times)
    min_time = np.min(times)
    max_time = np.max(times)

    plt.figure(figsize=(10, 5))
    plt.plot(times, label='Execution time per iteration')
    plt.axhline(mean_time, color='yellowgreen', linestyle='--', label=f'mean time: {mean_time:.2e}s')
    plt.axhline(min_time, color='darkorange', linestyle='--', label=f'min time: {min_time:.2e}s')
    plt.axhline(max_time, color='royalblue', linestyle='--', label=f'max time: {max_time:.2e}s')
    plt.yscale('log')
    plt.xlabel("Iteration")
    plt.ylabel("Time (seconds, log scale)")
    plt.title(f"Performance Profiling: {title} Over 1000 Iterations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def test_connect_shortest_valid():
    X = MockSearchSpace()
    Q = [1]
    rrt_star = RRTStar(X, Q, (0, 0), (10, 10), 100, 1)
    tree = 0
    x_new = (5, 5)
    L_near = [(1, (2, 2)), (2, (3, 3)), (3, (4, 4))]
    times = []
    for _ in range(1000):
        start = time.perf_counter()
        rrt_star.connect_shortest_valid(tree, x_new, L_near)
        times.append(time.perf_counter() - start)
    plot_graph(times, "connect_shortest_valid()")


def test_current_rewire_count():
    X = MockSearchSpace()
    Q = [1]
    rrt_star = RRTStar(X, Q, (0, 0), (10, 10), 100, 1, rewire_count=20)
    rrt_star.trees = {0: MockTree()}
    times = []
    for _ in range(1000):
        start = time.perf_counter()
        _ = rrt_star.current_rewire_count(0)
        times.append(time.perf_counter() - start)
    plot_graph(times, "current_rewire_count()")


def test_rewire():
    X = MockSearchSpace()
    Q = [1]
    rrt_star = RRTStar(X, Q, (0, 0), (10, 10), 100, 1)
    mock_tree = MockTree()
    rrt_star.trees = {0: mock_tree}
    x_new = (4, 4)
    L_near = [(1.0, (3, 3))]
    times = []
    for _ in range(1000):
        start = time.perf_counter()
        rrt_star.rewire(0, x_new, L_near)
        times.append(time.perf_counter() - start)
    plot_graph(times, "rewire()")


def test_get_nearby_vertices():
    X = MockSearchSpace()
    Q = [1]
    rrt_star = RRTStar(X, Q, (0, 0), (10, 10), 100, 1)
    mock_tree = MockTree()
    rrt_star.trees = {0: mock_tree}
    # Mock the nearby function to return existing keys
    rrt_star.nearby = lambda tree, x_new, count: [(2, 2), (3, 3)]
    x_new = (5, 5)
    times = []
    for _ in range(1000):
        start = time.perf_counter()
        _ = rrt_star.get_nearby_vertices(0, (0, 0), x_new)
        times.append(time.perf_counter() - start)
    plot_graph(times, "get_nearby_vertices()")


def main():
    options = {
        "1": ("connect_shortest_valid()", test_connect_shortest_valid),
        "2": ("current_rewire_count()", test_current_rewire_count),
        "3": ("get_nearby_vertices()", test_get_nearby_vertices),
        "4": ("rewire()", test_rewire),
    }

    print("Choose a method to test and graph:\n")
    for key, (desc, _) in options.items():
        print(f"{key}. {desc}")
    choice = input("\nEnter number: ").strip()

    if choice in options:
        print(f"\nRunning {options[choice][0]}...\n")
        options[choice][1]()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
