from AS_Algorithm import Get, ACO

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

if __name__ == '__main__':
    get = Get(points, x, y, cost_matrix)
    aco = ACO(1, 48, 3, 3, .02)