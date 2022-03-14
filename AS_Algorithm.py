### Import
import pandas as pd
import numpy as np
import random

### Get points
points = [] 
def read_file(file):
    with open(file) as f:
        line = f.readlines()
        list_data = []
        for index, data in enumerate(line):
            list_data.append(data.strip())

    for i in range(len(list_data)):
        points.append((int(list_data[i].split(' ')[1]), int(list_data[i].split(' ')[2])))

read_file('att48.txt')

### Get x & y
x = []
y = []
for i in range(len(points)):
    x.append(points[i][0])
    y.append(points[i][1])

### Get distance
def distance(x_i, x_j, y_i, y_j):
    return ((x_i - x_j)**2 + (y_i - y_j)**2)**(1/2)

cost_matrix = []
for i in range(len(points)):
    row = []
    for j in range(len(points)):
        row.append(distance(x[i], x[j], y[i], y[j]))
    cost_matrix.append(row)

class Get:
    def __init__(self, points, x, y, cost_matrix):
        self.points = points
        self.count_points = len(points)
        self.x = x
        self.y = y
        self.matrix = cost_matrix
        self.n = np.array([[0 if i == j else 1 / cost_matrix[i][j] for i in range(self.count_points)] for j in range(self.count_points)]) # 1/distance
        self.pheromone = np.array([[0 if i==j else 1 for i in range(self.count_points)] for j in range(self.count_points)], dtype=float)

class ACO:
    def __init__(self, gens, ants, alpha, beta, rho):
        self.gens = gens
        self.ants = ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho # rho (p) : Pheromone evaporation

    def probability(self, pheromone, n, count_points):
        ### Denominator
        tsa = [[pheromone[i][j]**self.alpha for i in range(count_points)] for j in range(count_points)] # t square alpha
        nsb = [[n[i][j]**self.beta for i in range(count_points)] for j in range(count_points)] # n square beta
        txn = [[tsa[i][j] * nsb[i][j] for i in range(count_points)] for j in range(count_points)] # tsa * nsb
        denominator = sum(sum(np.array(txn))) # sum(np.array(txn) : Sum of fist row, # sum(sum(np.array(txn)) : Sum of all rows

        # print(f'Allow: {self.allowed}')
        for point in range(count_points-1):
            self.prob = {}
            for i in self.allowed:
                self.prob.update({i: (pheromone[self.paths[-1]][i]**self.alpha) * (n[self.paths[-1]][i]**self.beta) / denominator})
            max_prob = sorted(self.prob.values())[-1]
            selected = list(self.prob.keys())[list(self.prob.values()).index(max_prob)]
            self.paths.append(selected)

            print(f'Point: {point+2}, Select: {selected}')
            # print(f'Paht : {self.paths}')

            ### Check walked path
            walked = 0
            for i in self.aco_matrix[self.paths[-1]]:
                if i == 0:
                    walked += 1
            # print(f'Walked: {walked}')

            if walked != count_points:
                shortest_distance = sorted(self.aco_matrix[self.paths[-1]])[walked]
                best_path = self.aco_matrix[self.paths[-1]].index(shortest_distance)
                print(f'Best path: {best_path}, Shortest distance: {shortest_distance}')
            
            ### Recheck best path
            # for best in enumerate(self.aco_matrix[self.paths[-1]]):
            #     print(best)

            ### Remove the path that has been walked
            self.allowed.remove(selected)
            for i in range(count_points):
                self.aco_matrix[selected][i] = 0
                self.aco_matrix[i][selected] = 0


            # ### Repeat
            # walked = 0
            # for i in cost_matrix[paths[-1]]:
            #     # if i == 0:
            #     #     walked += 1
            #     print(i)

    def aco(self, get: Get):
        self.aco_matrix = get.matrix.copy()
        print(self.aco_matrix)

        list_paths = []
        ### Generation
        for gen in range(self.gens):
            print(f'Generation: {gen+1}')
            
            ### Ant
            self.allowed = [i for i in np.arange(get.count_points)]
            self.paths = []

            random_start = list(range(get.count_points))
            for ant in range(self.ants):
                print(f'Ant: {ant+1}')

                ### Start
                start = random_start.pop(random.randrange(len(random_start))) # Random between 0 to 47
                selected = start
                self.paths.append(selected)

                # print(f'Allowed paht before remove path: {self.allowed}')
                print(f'Point: 1, Select: {start}')
                print(f'Paht : {self.paths}')
                shortest_distance = sorted(self.aco_matrix[self.paths[-1]])[1]
                best_path = self.aco_matrix[self.paths[-1]].index(shortest_distance)
                print(f'Best path: {best_path}, Shortest distance: {shortest_distance}')
                
                ### Remove the path that has been walked
                self.allowed.remove(selected)
                # print(f'Allowed paht after remove path: {self.allowed}')
                for i in range(get.count_points): # Set walked paht to 0
                    self.aco_matrix[selected][i] = 0
                    self.aco_matrix[i][selected] = 0
                
                self.probability(get.pheromone, get.n, get.count_points)

                list_paths.append(self.paths)
                print(list_paths)

                ### Reset values
                # reset()
                # self.allowed = [i for i in np.arange(get.count_points)]

            # ### Total distance
            # total_distance = 0
            # for i in range(len(paths)):
            #     if i != len(paths)-1:
            #         total_distance += (cm[paths[i]][paths[i+1]])
            # print(f'Total Distance : {total_distance}')
            # print(get.matrix)


            
            print()

            # print(f'len {len(self.path)}')

if __name__ == '__main__':
    get = Get(points, x, y, cost_matrix)
    # gens, ants, alpha, beta, rho
    aco = ACO(1, 1, 3, 3, .02)
    aco.aco(get)



    







