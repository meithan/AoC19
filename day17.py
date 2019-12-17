import sys

from IntcodeComputer import IntcodeComputer

# =================================================

class Scaffolding:

  def __init__(self, computer_outputs):

    # Parse computer output into grid
    self.grid = []
    row = []
    for c in computer.outputs:
      if c == 10 and len(row) > 0:
        self.grid.append(row)
        row = []
      else:
        row.append(chr(c))
    self.nrows = len(self.grid)
    self.ncols = len(self.grid[0])

    # Initial robot position and direction
    for i in range(self.nrows):
      for j in range(self.ncols):
        if self.grid[i][j] in ['<', '>', 'v', '^']:
          self.x, self.y = i, j
          self.direc = self.grid[i][j]
          self.grid[i][j] = "#"
          break

  def get_dxdy(self, direc):
    # Note: x is the row, so the vertical coord,
    # while y is the column, so horizontal coord
    if direc == '^':
      dx = -1; dy = 0
    elif direc == '>':
      dx = 0; dy = +1
    elif direc == 'v':
      dx = +1; dy = 0
    elif direc == '<':
      dx = 0; dy = -1
    return dx, dy

  def get_new_direc(self, cur_direc, turn):
    direcs = ['^', '>', 'v', '<']
    idx = direcs.index(cur_direc)
    if turn == "L":
      idx -= 1
    elif turn == "R":
      idx += 1
    return direcs[idx % 4]

  def grid_at(self, x, y):
    if x < 0 or x > self.nrows-1 or y < 0 or y > self.ncols-1:
      return None
    else:
      return self.grid[x][y]

  def walk_robot(self, debug=False):
    route = []
    fwd = 0
    while True:
      if debug:
        self.draw()
      if debug:
        print("pos={},{}  direc={}".format(self.x, self.y, self.direc))
      dx, dy = self.get_dxdy(self.direc)
      if self.grid_at(self.x+dx, self.y+dy) == "#":
        fwd += 1
        self.x += dx; self.y += dy
        if debug:
          print("Moved forward")
          print("Fwd:", fwd)
      else:
        if debug:
          print("Can't move forward, trying turn")
        found = False
        for turn in ["L", "R"]:
          new_direc = self.get_new_direc(self.direc, turn)
          new_dx, new_dy = self.get_dxdy(new_direc)
          if self.grid_at(self.x+new_dx, self.y+new_dy) == "#":
            found = True
            if fwd > 0:
              route.append(fwd)
            if debug:
              print("Turned", turn)
            route.append(turn)
            self.direc = new_direc
            fwd = 0
            break
        if not found:
          if fwd > 0:
            route.append(fwd)
          if debug:
            print("Reached end")
          break
      if debug:
        input("ENTER TO CONTINUE")

    return route

  def draw(self):
    for i in range(self.nrows):
      _row = self.grid[i][:]
      if i == self.x:
        _row[self.y] = self.direc
      print("".join(_row))

# =================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

computer = IntcodeComputer(program)
computer.execute(quiet=True)
scaff = Scaffolding(computer.outputs)

# Part 1

# Find intersections
grid = scaff.grid
inters = []
for i in range(1,scaff.nrows-1):
  for j in range(1,scaff.ncols-1):
    if grid[i][j] == "#" and grid[i-1][j] == "#" and grid[i+1][j] == "#" and grid[i][j-1] == "#" and grid[i][j+1] == "#":
      inters.append((i,j))

result = sum([p[0]*p[1] for p in inters])
print("Part 1:", result)

# Part 2

# First automatically find route along scaffolding
route = scaff.walk_robot()
route_str = ",".join([str(x) for x in route])
print(route_str)

# Then manually group instructions, and define them here:
definitions = {
"A": "L,12,L,8,R,12",
"B": "L,10,L,8,L,12,R,12",
"C": "R,12,L,8,L,10"
}

comp_route = route_str
for func in ["A", "B", "C"]:
  comp_route = comp_route.replace(definitions[func], func)

# Check the compressed route is good
print(f"Compressed: {comp_route} ({len(comp_route)})", )
for func in ["A", "B", "C"]:
  print(f"Function {func}: {definitions[func]} ({len(definitions[func])})")

# Now feed the program the definitions (ASCII-translated) and execute it
program[0] = 2
computer = IntcodeComputer(program)
seq = [ord(x) for x in comp_route] + [10]
print(seq)
for item in seq:
  computer.inputs.put(item)
for func in ["A", "B", "C"]:
  seq = [ord(x) for x in definitions[func]] + [10]
  print(seq)
  for item in seq:
    computer.inputs.put(item)
computer.inputs.put(ord("n"))
computer.inputs.put(10)
computer.execute(quiet=True)

# The last output is the answer
print("Part 2:", computer.last_output)
