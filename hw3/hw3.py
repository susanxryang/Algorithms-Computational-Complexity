import time
import sys

# Reading Input File
start_input = time.time()
input_file = sys.argv[1]
f = open(input_file).read()
output_filename = input_file.replace(".txt", "") + "_results.txt"
results = open(output_filename, 'w')

input_data = f.split()
N = int(input_data[0])

dfs_nums = [-1]*N
lows = [N+1]*N
dfscounter = 1
edgeList = []
biconnected_components = []
articulation_points = set([])
# try:
#     start_vertex = int(sys.argv[2])
# except:
#     start_vertex = 0

# Make Adjacency List

start_adj = time.time()
graph = list(zip(input_data[1::2], input_data[2::2]))
adjacency_list = {v: [] for v in range(N)}

for edge in graph:
    u = int(edge[0])
    v = int(edge[1])
    adjacency_list[u].append(v)
    adjacency_list[v].append(u)

visited = []

def DFS_biconnect(v, parent):

    global dfscounter, dfs_nums, edgeList, biconnected_components
    global visited, adjacency_list, articulation_points

    dfs_nums[v] = dfscounter
    dfscounter += 1
    lows[v] = dfs_nums[v]

    for x in adjacency_list[v]:

        if dfs_nums[x] == -1:
            # node unvisited; move towards it next
            edgeList.append((v, x))
            DFS_biconnect(x, v)
            lows[v] = min(lows[v], lows[x])

            if lows[x] >= dfs_nums[v]:
                articulation_points.add(v)

                next_edge = (-1, -1)
                next_bi_comp = []

                while next_edge[0] != v:
                    next_edge = edgeList.pop()
                    next_bi_comp.append(next_edge)

                biconnected_components.append(next_bi_comp)

        # edge going to non-parent ancestor in tree
        elif x != parent and dfs_nums[x] < dfs_nums[v]:
            lows[v] = min(lows[v], dfs_nums[x])
            edgeList.append((v, x))

start_alg = time.time()

DFS_biconnect(0, 0)
count = 0
articulation_points.remove(0)

# check separately whether start vertex is articulation point
for bc in biconnected_components:
    for edge in bc:
        if 0 in edge:
            count += 1
            break

if count > 1:
    articulation_points.add(0)

alg_runtime = time.time() - start_alg

# Outputting Results 

# for more detailed outputs
results.write("number nodes: " + str(N) + "\n")
print("number nodes: " + str(N) + "\n")
results.write("number graph: " + str(len(list(graph))) + "\n")
print("number graph: " + str(len(list(graph))) + "\n")
results.write("number biconnected components: " +
              str(len(biconnected_components)) + "\n")
print("number biconnected components: " +
      str(len(biconnected_components)) + "\n")
results.write("number of articulation points: " +
              str(len(articulation_points)) + "\n")
print("number of articulation points: " + str(len(articulation_points)) + "\n")
results.write("articulation points: " + str(articulation_points) + "\n")
print("articulation points: " + str(articulation_points) + "\n")

for i, bc in enumerate(biconnected_components):
    results.write("biconnected component " + str(i+1) +
                  ": " + str(biconnected_components[i]) + "\n")
    print("biconnected component " + str(i+1) +
          ": " + str(biconnected_components[i]) + "\n")

results.write("biconnected algorithm ran in: " + str(alg_runtime) + "\n")
print("algorithm ran in ", alg_runtime)