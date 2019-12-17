from collections import defaultdict
from queue import Queue
import os
import sys
import time

from IntcodeComputer import IntcodeComputer

# =================================================

class Crawler:

  def __init__(self, computer):
    self.computer = computer
    self.map = defaultdict(lambda: None)

  def build_map(self):

    self.pos = (0,0)
    map = self.map
    map[(0,0)] = 1
    to_try = {(0,0): ['e', 'w', 's', 'n']}
    dists = {(0,0): 0}
    num_to_try = 4
    moves = []
    found_oxy = False
    oxy_coords = None
    oxy_dist = None
    max_dist = None

    while num_to_try > 0:

      os.system('clear')
      print("\nPosition: ({},{})".format(self.pos[0], self.pos[1]))

      if len(to_try[self.pos]) != 0:
        move = to_try[self.pos].pop()
        num_to_try -= 1
        cmd, dx, dy = self.get_cmd_dx_dy(move)
        self.computer.inputs.put(cmd)
        self.computer.execute(pause_on_output=True, quiet=True)
        result = self.computer.last_output
        if result == 0:
          print("Hit wall {} at ({},{})".format(move, self.pos[0]+dx, self.pos[1]+dy))
          map[(self.pos[0]+dx, self.pos[1]+dy)] = 0
        elif result in (1, 2):
          moves.append(move)
          cur_dist = dists[self.pos]
          self.pos = self.pos[0] + dx, self.pos[1] + dy
          map[self.pos] = result
          if self.pos not in to_try:
            direcs = [d for d in ['e', 'w', 's', 'n'] if d != self.get_opp(move)]
            to_try[self.pos] = direcs
            num_to_try += 4
          if self.pos not in dists or cur_dist+1 < dists[self.pos]:
            dists[self.pos] = cur_dist + 1
          print("Moved {} to ({},{})".format(move, self.pos[0], self.pos[1]))
          if result == 2:
            oxy_dist = dists[self.pos]
            self.oxy_coords = self.pos
            # input("FOUND OXYGEN at ({},{}), dist: {}".format(x,y,oxy_dist))
      else:
        if len(moves) == 0:
          break
        last_move = moves.pop()
        move = self.get_opp(last_move)
        cmd, dx, dy = self.get_cmd_dx_dy(move)
        self.computer.inputs.put(cmd)
        self.computer.execute(pause_on_output=True, quiet=True)
        result = self.computer.last_output
        if result == 0:
          print("ERROR")
          sys.exit()
        self.pos = self.pos[0] + dx, self.pos[1] + dy
        print("Backtracked {} to ({},{})".format(move, self.pos[0], self.pos[1]))

      self.draw_map()
      # time.sleep(0.2)
      # input()

    print("Part 1: {}".format(oxy_dist))

  def propagate_oxygen(self):

    map = self.map

    # Do BFS on completed map
    x, y = self.oxy_coords
    max_dist = None
    fringe = Queue()
    visited = set()
    fringe.put((x, y, 0))
    while not fringe.empty():
      x, y, dist = fringe.get()
      print(x, y, dist)
      visited.add((x,y))
      map[(x,y)] = 2
      if max_dist is None or dist > max_dist:
        max_dist = dist
      moves = self.get_valid_moves(map, x, y)
      for move in moves:
        _, dx, dy = self.get_cmd_dx_dy(move)
        if (x+dx, y+dy) not in visited:
          fringe.put((x+dx, y+dy, dist+1))
      self.draw_map(show_pos=False)
      # input()
      os.system('clear')
    print("Part 2: {}".format(max_dist))

  def draw_map(self, show_pos=True):
    map = self.map
    xs = [p[0] for p in map.keys()]
    ys = [p[1] for p in map.keys()]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    for y in range(ymax, ymin-1, -1):
      for x in range(xmin, xmax+1):
        if show_pos and (x,y) == self.pos:
          print("D", end="")
        elif (x,y) == (0,0):
          print("S", end="")
        elif map[(x,y)] is None:
          print(" ", end="")
        elif map[(x,y)] == 0:
          print("#", end="")
          # print("░", end="")
          # print("█", end="")
        elif map[(x,y)] == 1:
          print(".", end="")
        elif map[(x,y)] == 2:
          print("O", end="")
        print(" ", end="")
      print()

  def get_cmd_dx_dy(self, move):
    if move == "n":
      cmd = 1; dx = 0; dy = +1
    elif move == "s":
      cmd = 2; dx = 0; dy = -1
    elif move == "w":
      cmd = 3; dx = -1; dy = 0
    elif move == "e":
      cmd = 4; dx = +1; dy = 0
    return cmd, dx, dy

  def get_opp(self, move):
    if move == "n": return "s"
    elif move == "s": return "n"
    elif move == "w": return "e"
    elif move == "e": return "w"

  def get_valid_moves(self, map, x, y):
    moves = []
    for move in ["n", "s", "e", "w"]:
      _, dx, dy = self.get_cmd_dx_dy(move)
      if map[(x+dx,y+dy)] != 0:
        moves.append(move)
    return moves

# =================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

crawler = Crawler(IntcodeComputer(program))
crawler.build_map()
input()
crawler.propagate_oxygen()
