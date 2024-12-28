import csv
import math
from typing import List, Dict, Tuple

# Node class to represent a city in the graph
class Node:
    def __init__(self, value: str):
        self.value = value  # Node's value (e.g., city name)
        self.neighbors: List[Tuple["Node", int]] = []  # List of neighboring nodes and the associated cost

    def add_neighbor(self, neighbor: "Node", cost: int):
        # Add a neighbor node with a cost (e.g., distance between cities)
        self.neighbors.append((neighbor, cost))

    def remove_neighbor(self, neighbor: "Node"):
        # Remove a specific neighbor node from the current node
        self.neighbors = [(n, c) for n, c in self.neighbors if n != neighbor]


# Graph class to represent the entire network of cities
class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def create_node(self, value: str):
        # Create a new node (city) in the graph
        if value not in self.nodes:
            self.nodes[value] = Node(value)

    def insert_edge(self, from_node: str, to_node: str, cost: int):
        # Insert an edge between two nodes with a given cost
        if from_node in self.nodes and to_node in self.nodes:
            self.nodes[from_node].add_neighbor(self.nodes[to_node], cost)

    def delete_edge(self, from_node: str, to_node: str):
        # Delete an edge between two nodes
        if from_node in self.nodes and to_node in self.nodes:
            self.nodes[from_node].remove_neighbor(self.nodes[to_node])

    def delete_node(self, value: str):
        # Delete a node and remove all edges connected to it
        if value in self.nodes:
            del self.nodes[value]
            for node in self.nodes.values():
                node.remove_neighbor(self.nodes.get(value))

    def load_cities(self, csv_file: str):
        # Load cities from a CSV file and create nodes for each
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                city = row[0]
                self.create_node(city)

    def get_coordinates(self, city: str) -> Tuple[float, float]:
        # Get the coordinates (latitude, longitude) for a city from the CSV data
        with open("romania_coordinates.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == city:
                    return float(row[1]), float(row[2])
        return 0.0, 0.0

    def euclidean_distance(self, city1: str, city2: str) -> float:
        # Calculate the Euclidean distance between two cities using their coordinates (latitude, longitude)
        city1_lat, city1_lon = self.get_coordinates(city1)
        city2_lat, city2_lon = self.get_coordinates(city2)
        return math.sqrt((city1_lat - city2_lat) ** 2 + (city1_lon - city2_lon) ** 2)

    def calculate_heuristic(self, goal_city: str) -> Dict[str, float]:
        # Calculate heuristic values (e.g., Euclidean distances to the goal city) for all cities
        heuristic = {}
        for city in self.nodes.keys():
            heuristic[city] = self.euclidean_distance(city, goal_city)
        return heuristic

    def __getitem__(self, city: str) -> Node:
        # Enable access to nodes using dictionary-like syntax
        return self.nodes[city]

    def set_neighbors(self, city_name: str, neighbors: List[Tuple[str, int]]):
        # Set neighbors for a specific city with associated costs
        if city_name in self.nodes:
            for neighbor_name, cost in neighbors:
                if neighbor_name in self.nodes:
                    self.insert_edge(city_name, neighbor_name, cost)
