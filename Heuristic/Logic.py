import math
from distances import distances

class TSPSolver:
    def __init__(self, coordinates):
        self.coordinates = coordinates
    
    def solve(self, num_salesmen, max_cities_per_salesman):
        paths = [[] for _ in range(num_salesmen)]
        unvisited_cities = set(range(1, len(self.coordinates)))
        
        for salesman in range(num_salesmen):
            path = paths[salesman]
            current_city = 0
            path.append(current_city)
            
            while len(path) < max_cities_per_salesman and unvisited_cities:
                nearest_city = min(unvisited_cities, key=lambda city: self._distance(current_city, city))
                path.append(nearest_city)
                unvisited_cities.remove(nearest_city)
                current_city = nearest_city
            
            path.append(0)
        
        remaining_cities = set(range(1, len(self.coordinates))) - set(city for path in paths for city in path)
        
        for remaining_city in remaining_cities:
            closest_path = min(paths, key=lambda path: self._calculate_insertion_cost(remaining_city, path))
            min_index = min(range(1, len(closest_path)), key=lambda i: self._calculate_insertion_cost_at_position(remaining_city, closest_path, i))
            closest_path.insert(min_index, remaining_city)
        
        return paths 
    
    def _distance(self, city1, city2):
        return math.dist(self.coordinates[city1], self.coordinates[city2])
    
    def _calculate_insertion_cost(self, city, path):
        return min(self._calculate_insertion_cost_at_position(city, path, i) for i in range(1, len(path)))
    
    def _calculate_insertion_cost_at_position(self, city, path, index):
        if index == len(path):
            return self._distance(path[-1], city) + self._distance(city, path[0]) - self._distance(path[-1], path[0])
        else:
            return self._distance(path[index-1], city) + self._distance(city, path[index]) - self._distance(path[index-1], path[index])

num_salesmen = 5
max_cities_per_salesman = 19

selected_matrix = "Matrix9"
coordinates = distances[selected_matrix]

solver = TSPSolver(coordinates)
paths = solver.solve(num_salesmen, max_cities_per_salesman)

for i, path in enumerate(paths):
    print(f"Salesman {i+1}: {path}")

total_distance = round(sum(sum(solver._distance(path[i], path[i+1]) for i in range(len(path) - 1)) for path in paths))
print(f"Total distance traveled: {total_distance}")
