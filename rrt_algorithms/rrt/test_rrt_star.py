import time
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
from rrt_algorithms.rrt.rrt_star import RRTStar
from rrt_algorithms.search_space.search_space import SearchSpace
from scipy.spatial import KDTree




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



def test_get_nearby_vertices():
    print("Running get_nearby_vertices()...")

    X_dimensions = np.array([(0, 100), (0, 100)])
    Obstacles = np.array([(20, 20, 40, 40), (20, 60, 40, 80),
                          (60, 20, 80, 40), (60, 60, 80, 80)])
    x_init = (0, 0)
    x_goal = (100, 100)

    q = 8
    r = 1
    max_samples = 1024
    rewire_count = 1024
    prc = 0.1

    X = SearchSpace(X_dimensions, Obstacles)
    rrt_star = RRTStar(X, q, x_init, x_goal, max_samples, r, prc, rewire_count)

    points = [(30, 30), (40, 40), (45, 45)]
    edges = {
        (30, 30): (0, 0),     # parent of (30, 30) is start (0, 0)
        (40, 40): (30, 30),   # parent of (40, 40) is (30, 30)
        (45, 45): (40, 40)    # parent of (45, 45) is (40, 40)
    }
    tree_obj = type('', (), {
    'V': KDTree(points),
    'V_count': len(points),
    'E': edges
    })()

    rrt_star.trees = {0: tree_obj}

    x_new = (50, 50)

    times = []
    for _ in range(1000):
        start = time.perf_counter()
        _ = rrt_star.get_nearby_vertices(0, x_init, x_new)
        times.append(time.perf_counter() - start)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
  

    print(f"get_nearby_vertices() - 1000 runs:")
    print(f"  Mean/Avg Time   : {avg_time:.8f} seconds")
    print(f"  Min Time   : {min_time:.8f} seconds")
    print(f"  Max Time   : {max_time:.8f} seconds")

    plot_graph(times, "get_nearby_vertices() Performance (1000 iterations)")



def test_rewire():
    print("Running rewire()...")

    X_dimensions = np.array([(0, 100), (0, 100)])
    Obstacles = np.array([(20, 20, 40, 40), (20, 60, 40, 80),
                          (60, 20, 80, 40), (60, 60, 80, 80)])
    x_init = (0, 0)
    x_goal = (100, 100)

    q = 8
    r = 1
    max_samples = 1024
    rewire_count = 1024
    prc = 0.1

    X = SearchSpace(X_dimensions, Obstacles)
    rrt_star = RRTStar(X, q, x_init, x_goal, max_samples, r, prc, rewire_count)

    # Setup edges for path_cost to work
    edges = {
        (30, 30): (20, 20),
        (20, 20): (10, 10),
        (10, 10): x_init,
        (40, 40): (30, 30),
        (45, 45): (40, 40)
    }

    tree_obj = type('', (), {'E': edges})()
    rrt_star.trees = {0: tree_obj}

    x_new = (50, 50)
    L_near = [(1, (30, 30)), (2, (40, 40)), (3, (45, 45))]

    times = []
    for _ in range(1000):
        start = time.perf_counter()
        rrt_star.rewire(0, x_new, L_near)
        times.append(time.perf_counter() - start)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"rewire() - 1000 runs:")
    print(f"  Mean/Avg Time   : {avg_time:.8f} seconds")
    print(f"  Min Time   : {min_time:.8f} seconds")
    print(f"  Max Time   : {max_time:.8f} seconds")

    plot_graph(times, "rewire() Performance (1000 iterations)")



def test_connect_shortest_valid():
    print("Running connect_shortest_valid()...")

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

    times = []
    for _ in range(1000):
        start = time.perf_counter()
        rrt_star.connect_shortest_valid(tree, x_new, L_near)
        times.append(time.perf_counter() - start)

    average_time = sum(times) / len(times)
    print(f"Average time per call to connect_shortest_valid(): {average_time:.8f} seconds")
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"connect_shortest_valid() - 1000 runs:")
    print(f" Mean/Avg Time   : {avg_time:.8f} seconds")
    print(f"  Min Time   : {min_time:.8f} seconds")
    print(f"  Max Time   : {max_time:.8f} seconds")


    plot_graph(times, "connect_shortest_valid() Performance (1000 iterations)")



def test_current_rewire_count():
    print("Running current_rewire_count()...")

    X_dimensions = np.array([(0, 100), (0, 100)])
    Obstacles = np.array([(20, 20, 40, 40), (20, 60, 40, 80),
                          (60, 20, 80, 40), (60, 60, 80, 80)])
    x_init = (0, 0)
    x_goal = (100, 100)

    q = 8
    r = 1
    max_samples = 1024
    rewire_count = 1024
    prc = 0.1

    X = SearchSpace(X_dimensions, Obstacles)
    rrt_star = RRTStar(X, q, x_init, x_goal, max_samples, r, prc, rewire_count)

    # Make sure a tree exists at index 0 with .V_count
    rrt_star.trees = {0: type('', (), {'V_count': 5})()}  # 5 vertices for testing

    times = []
    for _ in range(1000):
        start = time.perf_counter()
        _ = rrt_star.current_rewire_count(0)
        times.append(time.perf_counter() - start)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)


    print(f"current_rewire_count() - 1000 runs:")
    print(f" Mean/Avg Time   : {avg_time:.8f} seconds")
    print(f"  Min Time   : {min_time:.8f} seconds")
    print(f"  Max Time   : {max_time:.8f} seconds")

    plot_graph(times, "current_rewire_count() Performance (1000 iterations)")

     
def test_rrt_star():
    print("Starting RRTStar performance test...")
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

    iterations = 1000
    times = []

    for i in range(iterations):
        start_time = time.perf_counter()
        X = SearchSpace(X_dimensions, Obstacles)
        rrt_star = RRTStar(X, q, x_init, x_goal, max_samples, r, prc, rewire_count)

         # force tree init (optional)
        _ = rrt_star.trees[0] if 0 in rrt_star.trees else None

        end_time = time.perf_counter()
        times.append(end_time - start_time)

        if (i + 1) % 100 == 0:
            print(f"Completed {i + 1}/{iterations} iterations")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\nRRTStar - 1000 runs:")
    print(f" Mean/Avg Time   : {avg_time:.8f} seconds")
    print(f"  Min Time   : {min_time:.8f} seconds")
    print(f"  Max Time   : {max_time:.8f} seconds")
    plot_graph(times, "RRTStar Instantiation Performance (1000 iterations)")



def main():
    options = {
        "1": ("test_get_nearby_vertices()", test_get_nearby_vertices),
        "2": ("test_rewire()", test_rewire),
        "3": ("test_connect_shortest_valid()", test_connect_shortest_valid),
        "4": ("test_current_rewire_count()", test_current_rewire_count),
        "5": ("test_rrt_star()", test_rrt_star),

       
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


