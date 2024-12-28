from collections import deque
from queue import PriorityQueue
import random
import math
from typing import Dict, List, Tuple
from graph import Graph, Node  # Assuming these classes are defined

# Breadth-First Traversal with Cost Calculation
def bfs_with_cost(graph: Graph, start: Node, goal: Node) -> Tuple[List[Node], float]:
    """
    Perform Breadth-First Search to find the shortest path from start to goal and calculate its cost.
    """
    queue = deque([(start, 0, [start])])  # Queue containing (current_node, current_cost, path)
    visited = set()  # Set to track visited nodes

    while queue:
        current, current_cost, path = queue.popleft()

        # Check if we've reached the goal node
        if current == goal:
            return path, current_cost  # Return the path and total cost

        if current not in visited:
            visited.add(current)  # Mark the node as visited

            # Iterate through neighbors
            for neighbor, cost in current.neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, current_cost + cost, path + [neighbor]))

    return None, float('inf')  # Return None if no path is found


# Depth-First Traversal with Cost Calculation
def dfs_with_cost(graph: Graph, start: Node, goal: Node) -> Tuple[List[Node], float]:
    """
    Perform Depth-First Search to find a path from start to goal and calculate the path cost.
    """
    visited = set()  # Set to track visited nodes
    stack = [(start, 0, [start])]  # Stack containing (current_node, current_cost, path)

    while stack:
        current, current_cost, path = stack.pop()

        # Check if the goal node is reached
        if current == goal:
            return path, current_cost

        if current not in visited:
            visited.add(current)  # Mark the current node as visited

            # Iterate through neighbors with their associated costs
            for neighbor, cost in current.neighbors:
                if neighbor not in visited:
                    # Append neighbor with updated cost and path
                    stack.append((neighbor, current_cost + cost, path + [neighbor]))

    return None, float('inf')  # Return None if no path is found

# Uniform Cost Search (UCS)
def ucs(graph: Graph, start: Node, goal: Node) -> Tuple[List[Node], float]:
    """
    Perform Uniform Cost Search to find the least-cost path from start to goal.
    """
    pq = PriorityQueue()
    came_from = {}
    cost_so_far = {start: 0}

    pq.put((0, start))

    while not pq.empty():
        current_cost, current = pq.get()

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, current_cost

        # Iterate through neighbors
        for neighbor, cost in current.neighbors:
            new_cost = current_cost + cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                pq.put((new_cost, neighbor))
                came_from[neighbor] = current

    return None, float('inf')  # Return None if no path is found


# A* Search Algorithm
def a_star(graph: Graph, start: Node, goal: Node, heuristic: Dict[str, float]) -> Tuple[List[Node], float]:
    """
    Perform A* Search to find the shortest path from start to goal using a heuristic.
    """
    pq = PriorityQueue()
    came_from = {}
    g_costs = {start: 0}

    f_costs = {start: heuristic[start.value]}
    pq.put((f_costs[start], start))

    while not pq.empty():
        _, current = pq.get()

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_costs[goal]

        for neighbor, cost in current.neighbors:
            new_g_cost = g_costs[current] + cost
            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic[neighbor.value]
                f_costs[neighbor] = f_cost
                pq.put((f_cost, neighbor))
                came_from[neighbor] = current

    return None, float('inf')  # Return None if no path is found


# Simulated Annealing Algorithm
def simulated_annealing(graph: Graph, start: Node, goal: Node, heuristic: Dict[str, float]) -> Tuple[List[Node], float]:
    """
    Perform Simulated Annealing to find an approximate solution from start to goal.
    """
    current_state = start
    current_path = [start]  # Track the path from start to current state
    visited_nodes = set([start])  # Track visited nodes to avoid loops
    current_cost = 0
    temperature = 1000.0
    cooling_rate = 0.95

    # Run for a fixed number of iterations
    for _ in range(1000):
        neighbors_with_costs = [(neighbor, cost) for neighbor, cost in current_state.neighbors if neighbor not in visited_nodes]

        if not neighbors_with_costs:
            return None, float('inf')  # No neighbors, return failure

        # Randomly pick a neighbor and calculate the new path cost
        next_state, cost_to_next_state = random.choice(neighbors_with_costs)
        new_cost = current_cost + cost_to_next_state  # Update the total cost correctly
        delta_e = new_cost - current_cost

        # Accept the new state if it's better or with a certain probability
        if delta_e < 0 or random.random() < math.exp(-delta_e / temperature):
            current_state = next_state
            current_cost = new_cost  # Update the current cost
            current_path.append(current_state)  # Add the state to the path
            visited_nodes.add(current_state)  # Mark this node as visited

            # If we've reached the goal node, return the path and cost
            if current_state == goal:
                return current_path, current_cost

        # Cooling process
        temperature *= cooling_rate

    return None, float('inf')  # Return None if no solution is found
