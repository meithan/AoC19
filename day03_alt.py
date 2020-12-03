import sys

# ===========================================

def Manhattan(x1, y1, x2, y2):
  return abs(x1-x2) + abs(y1-y2)

# ===========================================

with open(sys.argv[1]) as f:
  moves1 = f.readline().strip().split(",")
  moves2 = f.readline().strip().split(",")

# Walk wire1, save visited places and the number of steps
visited = {}
x = y = 0
steps = 0
for move in moves1:
  direc = move[0]
  length = int(move[1:])
  for s in range(length):
    steps += 1
    if direc == "R":
      x += 1
    elif direc == "L":
      x -= 1
    elif direc == "U":
      y += 1
    elif direc == "D":
      y -= 1
    if (x,y) not in visited:
      # we keep the number of steps of the first visit
      visited[(x,y)] = steps

# Now walk wire2, checking whether a place was already visited
# If so, an intersection was found; check if it's "better" under
# the part 1 and part 2 criteria
closest_inter = None
closest_dist = None
fastest_inter = None
fastest_steps = None
x = y = 0
steps2 = 0
for move in moves2:
  direc = move[0]
  length = int(move[1:])
  for s in range(length):
    steps2 += 1
    if direc == "R":
      x += 1
    elif direc == "L":
      x -= 1
    elif direc == "U":
      y += 1
    elif direc == "D":
      y -= 1
    if (x,y) in visited:
      dist = Manhattan(x, y, 0, 0)
      tot_steps = visited[(x,y)] + steps2
      if closest_dist is None or dist < closest_dist:
        closest_dist = dist
        closest_inter = (x,y)
      if fastest_steps is None or tot_steps < fastest_steps:
        fastest_steps = tot_steps
        fastest_inter = (x,y)

print(f"Part 1: {closest_dist}")
print(f"Part 1: {fastest_steps}")

