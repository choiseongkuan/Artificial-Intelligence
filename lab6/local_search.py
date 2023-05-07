import math
import copy
import random
import matplotlib.pyplot as plt
import numpy


class TSP:
    def __init__(self, cities):
        self.cities = cities
        
        self.path = []
        self.total_distance = 0
        self.each_distance = []
        self.cities_num = len(self.cities)
        self.initialize()

    def initialize(self):
        for i in range(0, len(self.cities)):
            self.path.append(i)
            tmp_distance = self.get_distance(i, (i+1)%self.cities_num)
            self.each_distance.append(tmp_distance)
            self.total_distance += tmp_distance

    def get_distance(self, city1, city2):
        x1, y1 = self.cities[city1]
        x2, y2 = self.cities[city2]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def swap_cities(self, index_1, index_2):
        path = copy.deepcopy(self.path)
        path[index_1], path[index_2] = self.path[index_2], self.path[index_1]
        each_distance = copy.deepcopy(self.each_distance)
        each_distance[index_1-1] = self.get_distance(path[index_1-1], path[index_1])
        each_distance[index_1] = self.get_distance(path[index_1], path[(index_1+1)%self.cities_num])
        each_distance[index_2-1] = self.get_distance(path[index_2-1], path[index_2])
        each_distance[index_2] = self.get_distance(path[index_2], path[(index_2+1)%self.cities_num])
        total_distance = self.total_distance - self.each_distance[index_1-1] - self.each_distance[index_1] - self.each_distance[index_2-1] - self.each_distance[index_2] + each_distance[index_1-1] + each_distance[index_1] + each_distance[index_2-1] + each_distance[index_2]
        # aa = 0
        # for i in range(0, len(self.cities)-1):
        #     aa += self.get_distance(path[i], path[i+1])
        # aa += self.get_distance(path[-1], path[0])
        # print(aa)
        return path, each_distance, total_distance

    def reverse_mid_seq(self, index_1, index_2):
        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        path = copy.deepcopy(self.path)
        path = path[:index_1] + path[index_1: index_2+1][::-1] + path[index_2+1:]
        each_distance = copy.deepcopy(self.each_distance)
        old_distance = 0
        new_distance = 0
        for i in range(index_1-1, index_2+1):
            each_distance[i] = self.get_distance(path[i], path[(i+1)%self.cities_num])
            old_distance += self.each_distance[i]
            new_distance += each_distance[i]
        total_distance = self.total_distance - old_distance + new_distance
        # aa = 0
        # for i in range(0, len(self.cities)-1):
        #     aa += self.get_distance(path[i], path[i+1])
        # aa += self.get_distance(path[-1], path[0])
        # print(aa)
        return path, each_distance, total_distance

    def reverse_head_tail_seq(self, index_1, index_2):
        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        path = copy.deepcopy(self.path)
        path = path[:index_1+1][::-1] + path[index_1+1:index_2] + path[index_2:][::-1]
        each_distance = copy.deepcopy(self.each_distance)
        old_distance = 0
        new_distance = 0
        for i in range(0, index_1+1):
            each_distance[i] = self.get_distance(path[i], path[i+1])
            old_distance += self.each_distance[i]
            new_distance += each_distance[i]
        for i in range(index_2-1, self.cities_num):
            each_distance[i] = self.get_distance(path[i], path[(i+1)%self.cities_num])
            old_distance += self.each_distance[i]
            new_distance += each_distance[i]
        total_distance = self.total_distance - old_distance + new_distance
        # aa = 0
        # for i in range(0, len(self.cities)-1):
        #     aa += self.get_distance(path[i], path[i+1])
        # aa += self.get_distance(path[-1], path[0])
        # print(aa)
        return path, each_distance, total_distance

    def reverse_all_seq(self, index_1, index_2):
        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        path = copy.deepcopy(self.path)
        path = path[:index_1][::-1] + path[index_1:index_2][::-1] + path[index_2:][::-1]
        each_distance = copy.deepcopy(self.each_distance)
        total_distance = 0
        for i in range(self.cities_num):
            each_distance[i] = self.get_distance(path[i], path[(i+1)%self.cities_num])
            total_distance += each_distance[i]
        return path, each_distance, total_distance

    def take_seq_to_head(self, index_1, index_2):
        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        path = copy.deepcopy(self.path)
        path = path[index_1:index_2+1] + path[:index_1] + path[index_2+1:]
        each_distance = copy.deepcopy(self.each_distance)
        old_distance = 0
        new_distance = 0
        for i in range(0, index_2+1):
            each_distance[i] = self.get_distance(path[i], path[(i+1)%self.cities_num])
            old_distance += self.each_distance[i]
            new_distance += each_distance[i]
        if index_2 != self.cities_num-1:
            each_distance[self.cities_num-1] = self.get_distance(path[-1], path[0])
            old_distance += self.each_distance[-1]
            new_distance += each_distance[-1]
        total_distance = self.total_distance - old_distance + new_distance
        # aa = 0
        # for i in range(0, len(self.cities)-1):
        #     aa += self.get_distance(path[i], path[i+1])
        # aa += self.get_distance(path[-1], path[0])
        # print(aa)
        return path, each_distance, total_distance

    def generate_solution(self):
        p = random.random()
        index_1 = random.randint(1, self.cities_num-1)
        while True:
            index_2 = random.randint(1, self.cities_num-1)
            if abs(index_1 - index_2) > 1:
                break
        if 0 <= p < 0.25:
            path, each_distance, total_distance = self.swap_cities(index_1, index_2)
        elif 0.25 <= p < 0.5:
            path, each_distance, total_distance = self.reverse_mid_seq(index_1, index_2)
        elif 0.5 <= p < 0.75:
            path, each_distance, total_distance = self.reverse_head_tail_seq(index_1, index_2)
        else:
            path, each_distance, total_distance = self.reverse_all_seq(index_1, index_2)
        # while True:
        #     path, each_distance, total_distance = self.swap_cities(index_1, index_2)
        #     op_path, op_each_distance, op_total_distance = path, each_distance, total_distance
        #     if total_distance < self.total_distance:
        #         break
        #
        #     path, each_distance, total_distance = self.reverse_mid_seq(index_1, index_2)
        #     if total_distance < self.total_distance:
        #         op_path, op_each_distance, op_total_distance = path, each_distance, total_distance
        #         break
        #     if total_distance < op_total_distance:
        #         op_path, op_each_distance, op_total_distance = path, each_distance, total_distance
        #
        #     path, each_distance, total_distance = self.reverse_head_tail_seq(index_1, index_2)
        #     if total_distance < self.total_distance:
        #         op_path, op_each_distance, op_total_distance = path, each_distance, total_distance
        #         break
        #     if total_distance < op_total_distance:
        #         op_path, op_each_distance, op_total_distance = path, each_distance, total_distance
        #
        #     path, each_distance, total_distance = self.reverse_all_seq(index_1, index_2)
        #     if total_distance < self.total_distance:
        #         op_path, op_each_distance, op_total_distance = path, each_distance, total_distance
        #         break
        #     if total_distance < op_total_distance:
        #         op_path, op_each_distance, op_total_distance = path, each_distance, total_distance
        #     break
        return path, each_distance, total_distance


def local_search(tsp):
    iteration = []
    distance = []
    i = 0
    while tsp.total_distance > 6721 and i <= 100000:
        path, each_distance, total_distance = tsp.generate_solution()
        if total_distance < tsp.total_distance:
            tsp.total_distance = total_distance
            tsp.each_distance = each_distance
            tsp.path = path
        iteration.append(i)
        distance.append(tsp.total_distance)
        i += 1
    print(f"final optimal distance: {tsp.total_distance}")
    # print_iteration_and_distance(iteration, distance)
    print_map(tsp)


def print_iteration_and_distance(iteration, distance):
    plt.plot(iteration, distance)
    plt.xlabel("iteration")
    plt.ylabel("distance")
    plt.title("TSP local search")
    plt.show()


def print_map(tsp):
    optimal_path = tsp.path
    optimal_path.append(tsp.path[0])
    x = [tsp.cities[city][0] for city in optimal_path]
    y = [tsp.cities[city][1] for city in optimal_path]
    plt.plot(x, y)
    plt.xlabel("lon.")
    plt.ylabel("lat.")
    plt.title("TSP local search")
    plt.show()


def read_tsp_file(file_path):
    items = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines[6:-1]:
            x, y = line.strip().split()[1:]
            items.append((float(x), float(y)))
    return items


if __name__ == "__main__":
    get_cities = read_tsp_file("ch130.tsp")
    get_tsp = TSP(get_cities)
    # get_tsp.take_seq_to_head(5, 9)
    local_search(get_tsp)
