import sys

# A node is defined by its name and the name of its parent
class Node:
  def __init__(self, name, parent):
    self.parent = parent

# Walk the three up from the given node up to the root
def walk_up_tree(node):
  visited = []
  count = 0
  while node.parent is not None:
    count += 1
    visited.append((node.parent, count))
    node = orbits[node.parent]
  return visited

# Load orbits
orbits = {"COM": Node("COM", None)}
with open(sys.argv[1]) as f:
  for line in f:
    parent, child = line.strip().split(")")
    orbits[child] = Node(child, parent)

# Part 1
tot_orbits = 0
for node in orbits.values():
  tot_orbits += len(walk_up_tree(node))
print(f"Part 1: {tot_orbits}")

# Part 2
visited_YOU = walk_up_tree(orbits["YOU"])
visited_SAN = walk_up_tree(orbits["SAN"])
visited_SAN_dict = {x[0]: x[1] for x in visited_SAN}

# Find first node that both paths visit when walking up the tree
for node, count1 in visited_YOU:
  if node in visited_SAN_dict:
    count2 = visited_SAN_dict[node]
    steps = count1 + count2 - 2
    print(f"Part 2: {steps}")
    break
