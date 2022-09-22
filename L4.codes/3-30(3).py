from random import randint, random
import sys

N = int(sys.argv[1])
path = sys.argv[2]

num_cities = N 
cities = []

# choose a line
_cities = []
for i in range(num_cities):
    _cities.append(i)

while len(_cities) != 0:
    city = _cities.pop(randint(0, len(_cities) - 1))
    cities.append(city)

# init map
dis = []
for i in range(num_cities):
    dis.append([])
    for j in range(num_cities):
        dis[i].append(0)

max_dis = 100
# generate map
for i in range(num_cities):
    for j in range(i + 1, num_cities):
        dis[i][j] = randint(0, max_dis)
        dis[j][i] = dis[i][j]

# dump map to path
with open(path, "w") as f:
    f.write(str(num_cities) + "\n")
    for i in range(num_cities):
        for j in range(num_cities):
            f.write(str(dis[i][j]) + " ")
        f.write("\n")