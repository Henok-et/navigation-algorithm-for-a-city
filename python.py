import time
from random import random
from math import exp, inf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from graph import Graph
from search_algorithms import (
     bfs_with_cost,
    dfs_with_cost,
    ucs,
    a_star,
    simulated_annealing,
)

# Initialize the graph and load city data
romania_map = Graph()
romania_map.load_cities("romania_coordinates.csv")  # Load cities and coordinates from CSV

# Define city connections with their respective costs
romania_map.set_neighbors('Arad', [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)])
romania_map.set_neighbors('Sibiu', [('Arad', 140), ('Fagaras', 99), ('Oradea', 151), ('Rimnicu Vilcea', 80)])
romania_map.set_neighbors('Zerind', [('Arad', 75), ('Oradea', 71)])
romania_map.set_neighbors('Fagaras', [('Sibiu', 99), ('Bucharest', 211)])
romania_map.set_neighbors('Oradea', [('Zerind', 71), ('Sibiu', 151)])
romania_map.set_neighbors('Rimnicu Vilcea', [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)])
romania_map.set_neighbors('Pitesti', [('Rimnicu Vilcea', 97), ('Bucharest', 101)])
romania_map.set_neighbors('Timisoara', [('Arad', 118), ('Lugoj', 111)])
romania_map.set_neighbors('Lugoj', [('Timisoara', 111), ('Mehadia', 70)])
romania_map.set_neighbors('Mehadia', [('Lugoj', 70), ('Drobeta', 75)])
romania_map.set_neighbors('Drobeta', [('Mehadia', 75), ('Craiova', 120)])
romania_map.set_neighbors('Craiova', [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)])
romania_map.set_neighbors('Bucharest', [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90)])

# Specify the starting and destination cities
origin_city = "Arad"
destination_city = "Bucharest"

# Fetch nodes for the start and destination
origin_node = romania_map[origin_city]
destination_node = romania_map[destination_city]

# Calculate heuristic values for A* and Simulated Annealing
heuristic_values = romania_map.calculate_heuristic(destination_city)

# Define algorithms to evaluate
search_methods = {
    "bfs_with_cost": lambda: bfs_with_cost(romania_map, origin_node, destination_node),
    "dfs_with_cost": lambda: dfs_with_cost(romania_map, origin_node, destination_node),
    "ucs": lambda: ucs(romania_map, origin_node, destination_node),
    "a_star": lambda: a_star(romania_map, origin_node, destination_node, heuristic_values),
    "simulated_annealing": lambda: simulated_annealing(romania_map, origin_node, destination_node, heuristic_values),
}

# Helper function for displaying paths
def format_path(nodes):
    return " -> ".join(node.value for node in nodes) if nodes else "No path found"

# Benchmark algorithms and collect results
results_summary = {}
for name, method in search_methods.items():
    exec_times = []
    paths = []
    total_costs = []

    for _ in range(10):  # Test each algorithm multiple times
        start = time.perf_counter()  # Use perf_counter for higher precision
        path, cost = method()
        end = time.perf_counter()
        exec_times.append(end - start)
        paths.append(path)
        total_costs.append(cost)

    avg_execution_time = sum(exec_times) / len(exec_times)
    avg_cost = sum(total_costs) / len(total_costs)
    example_path = paths[0]  # Take the first path as representative

    if name == "Simulated Annealing" and (not example_path or len(example_path) == 0):
        results_summary[name] = {
            "path": "No solution found",
            "cost": "N/A",
            "time": f"{avg_execution_time:.10f}",
        }
    else:
        results_summary[name] = {
            "path": format_path(example_path),
            "cost": avg_cost if example_path else float('inf'),
            "time": f"{avg_execution_time:.10f}",
        }

# Prepare data for plotting
algorithms = list(results_summary.keys())
execution_times = [float(data['time']) for data in results_summary.values()]
costs = [float(data['cost']) if isinstance(data['cost'], (int, float)) else float('inf') for data in results_summary.values()]

# Create first plot for execution times
plt.figure(figsize=(12, 6))
bar_colors = sns.color_palette("Blues", len(results_summary))
plt.bar(algorithms, execution_times, color=bar_colors)
plt.xlabel('Search Algorithms')
plt.ylabel('Execution Time (seconds)')
plt.title("Execution Time Comparison of Search Algorithms")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the first plot
plt.savefig("execution_time_comparison.png")
plt.close()

# Create second plot for costs
plt.figure(figsize=(12, 6))
plt.bar(algorithms, costs, color="lightcoral")
plt.xlabel('Search Algorithms')
plt.ylabel('Cost')
plt.title("Cost Comparison of Search Algorithms")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the second plot
plt.savefig("cost_comparison.png")
plt.close()

print("Execution time and cost comparison images saved as 'execution_time_comparison.png' and 'cost_comparison.png'")
