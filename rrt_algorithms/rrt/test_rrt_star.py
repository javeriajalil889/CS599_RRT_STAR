from rrt_algorithms.rrt.rrt_star import RRTStar
import time
import matplotlib.pyplot as plt
import numpy as np
import csv


class MockSearchSpace():
    def __init__(self):
        self.dimensions = 2

    def collision_free(self, point1, point2, resolution):
        return True  

def test_connect_shortest_valid():
    X = MockSearchSpace()
    Q = [1]
    x_init = (0, 0)
    x_goal = (10, 10)
    max_samples = 100
    r = 1

    rrt_star = RRTStar(X, Q, x_init, x_goal, max_samples, r)

    tree = 0
    x_new = (5, 5)
    L_near = [(1, (2, 2)), (2, (3, 3)), (3, (4, 4))]

    times = []
    for _ in range(50):
        start_time = time.perf_counter()
        rrt_star.connect_shortest_valid(tree, x_new, L_near)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        times.append(elapsed)
    

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

    plt.title("Performance Profiling: connect_shortest_valid() Timing Over 50 Iterations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# if __name__ == "__main__":
#     test_connect_shortest_valid()
 


def test_current_rewire_count():
    class MockTree:
        def __init__(self, v_count):
            self.V_count = v_count

    class MockSearchSpace:
        def __init__(self):
            self.dimensions = 2
        def collision_free(self, p1, p2, r): return True

    X = MockSearchSpace()
    Q = [1]
    x_init = (0, 0)
    x_goal = (10, 10)
    max_samples = 100
    r = 1

    rrt_star = RRTStar(X, Q, x_init, x_goal, max_samples, r, rewire_count=20)

    tree = 0
    rrt_star.trees = {tree: MockTree(v_count=50)}

    times = []
    for _ in range(50):
        start = time.perf_counter()
        _ = rrt_star.current_rewire_count(tree)
        end = time.perf_counter()
        times.append(end - start)

    # return times


    # # Save to CSV
    # with open("current_rewire_count_times.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Iteration", "ExecutionTime"])
    #     for i, t in enumerate(times):
    #         writer.writerow([i, t])

    # main stats
    mean_time = np.mean(times)
    min_time = np.min(times)
    max_time = np.max(times)

    # graphing
    plt.figure(figsize=(10, 5))
    plt.plot(times, label='Execution time per iteration')
    plt.axhline(mean_time, color='green', linestyle='--', label=f'Mean: {mean_time:.2e}s')
    plt.axhline(min_time, color='orange', linestyle='--', label=f'Min: {min_time:.2e}s')
    plt.axhline(max_time, color='blue', linestyle='--', label=f'Max: {max_time:.2e}s')
    plt.yscale('log')
    plt.xlabel("Iteration")
    plt.ylabel("Time (seconds, log scale)")
    plt.title("Performance Profiling: current_rewire_count() Timing Over 50 Iterations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    times = test_current_rewire_count()