from queue import Queue, PriorityQueue
from string import ascii_lowercase, ascii_uppercase
import random
import sys

# =================================================

class bcolors:
  YELLOW = "\033[1;33m"
  KEY = "\033[1;32m"
  DOOR = "\033[1;34m"
  DARKGREY = "\033[1;30m"
  RED = "\033[1;31m"
  BLINK = "\033[5m"
  RESET = "\033[0m"

class Maze:

  def __init__(self, rows):
    self.nx = len(rows[0])
    self.ny = len(rows)
    self.grid = []
    self.keys = {}
    self.doors = {}
    self.entrance = None
    for i in range(self.nx):
      self.grid.append([0]*self.ny)
    for x in range(self.nx):
      for y in range(self.ny):
        self.grid[x][y] = rows[y][x]
        if self.is_key(self.grid[x][y]):
          self.keys[self.grid[x][y]] = (x,y)
        elif self.is_door(self.grid[x][y]):
          self.doors[self.grid[x][y]] = (x,y)
        elif self.grid[x][y] == "@":
          self.entrance = (x,y)

  def is_key(self, c):
    return 97 <= ord(c) <= 122

  def is_door(self, c):
    return 65 <= ord(c) <= 90

  # Pre-compute the paths between all pairs of keys
  def precompute_paths(self):
    self.paths = {}
    # keys = '@' + ascii_lowercase
    keys = ['@'] + sorted(list(self.keys.keys()))
    for i in range(len(keys)):
      for j in range(i+1, len(keys)):
        key1 = keys[i]
        pos1 = self.entrance if key1 == '@' else self.keys[key1]
        key2 = keys[j]
        pos2 = self.keys[key2]
        path = self.find_path(pos1, pos2, ignore_doors=True)
        if path is None:
          continue
        passed_doors = set()
        passed_keys = set()
        for pos in path:
          symbol = self.grid[pos[0]][pos[1]]
          if self.is_door(symbol):
            passed_doors.add(symbol)
          if self.is_key(symbol) and symbol != key1 and symbol != key2:
            passed_keys.add(symbol)
        # print(key1, key2, passed_doors, passed_keys, len(path)-1)
        self.paths[(key1,key2)] = (len(path)-1, passed_doors, passed_keys)

  def valid_neighbors(self, x, y, ignore_doors=False):
    valid = []
    for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
      symbol = self.grid[nx][ny]
      if symbol in ['.', '@'] or self.is_key(symbol) or (ignore_doors and self.is_door(symbol)):
        valid.append((nx,ny))
    return valid

  def find_path(self, start, target, ignore_doors=False):
    visited = set()
    fringe = Queue()
    fringe.put((start,[start]))
    while not fringe.empty():
      pos, path = fringe.get()
      if pos == target:
        return path
      visited.add(pos)
      for npos in self.valid_neighbors(*pos, ignore_doors):
        if npos not in visited:
          fringe.put((npos, path+[npos]))
    return None

  def draw(self, highlight1=None, highlight2=None, blink=None):
    for y in range(self.ny):
      row = []
      for x in range(self.nx):
        effect = bcolors.RESET
        color = bcolors.DARKGREY
        symbol = self.grid[x][y]
        if highlight1 is not None and (x,y) in highlight1:
          color = bcolors.RED
        if highlight2 is not None and (x,y) in highlight2:
          color = bcolors.YELLOW
        if symbol == '#':
          color = bcolors.DARKGREY
          symbol = "▒"
        elif symbol == '@':
          color = bcolors.YELLOW
        elif self.is_key(symbol):
          color = bcolors.KEY
        elif self.is_door(symbol):
          color = bcolors.DOOR
        if blink is not None and (x,y) in blink:
          effect = bcolors.BLINK
        row.append(effect + color + symbol + bcolors.RESET)
      print("".join(row))
    print(bcolors.RESET)

  def is_path_open(self, passed_doors, passed_keys, collected_keys):
    for key in passed_keys:
      if key not in collected_keys:
        return False
    for door in passed_doors:
      if door.lower() not in collected_keys:
        return False
    return True

  def reachable_keys(self, cur_key, collected_keys):

    reachable = []
    for pair in self.paths:
      if pair[0] == cur_key:
        other_key = pair[1]
      elif pair[1] == cur_key:
        other_key = pair[0]
      else:
        continue
      if other_key == '@':
        continue
      if other_key not in collected_keys:
        dist, passed_doors, passed_keys = self.paths[pair]
        if self.is_path_open(passed_doors, passed_keys, collected_keys):
          reachable.append((other_key, dist))
    return reachable

  def find_fastest_route(self):

    collected = set()
    self.cache = {}
    return self.fastest_from('@', collected, [])

  def fastest_from(self, cur_key, collected, route):

    # print(f"\nCall: {cur_key} {collected} {route}")
    if len(collected) == len(self.keys):
      return 0, route

    cache_key = (cur_key, "".join(sorted(list(collected))))
    if cache_key in self.cache:
      return self.cache[cache_key]

    best_dist = None
    best_route = None
    reachable = self.reachable_keys(cur_key, collected)
    for next_key, key_dist in reachable:

      next_collected = collected.copy()
      next_collected.add(next_key)
      next_route = route + [next_key]

      dist, fwd_route = self.fastest_from(next_key, next_collected, next_route)

      cache_key = (next_key, "".join(sorted(list(next_collected))))
      self.cache[cache_key] = (dist, fwd_route)

      tot_dist = key_dist + dist
      if best_dist is None or tot_dist < best_dist:
        best_dist = tot_dist
        best_route = fwd_route

    return best_dist, best_route

class Robot:

  def__init__(self, maze):
    self.maze = None
    self.pos = self.maze.entrance

  def move_to(self, tx, ty):
    

# =================================================

with open(sys.argv[1]) as f:
  rows = f.read().split("\n")[:-1]

maze = Maze(rows)
print("Pre-computing paths ...")
maze.precompute_paths()
print(f"{len(maze.paths)} paths computed")
maze.draw()

# path = maze.find_path(maze.keys['r'], maze.keys['z'], ignore_doors=True)
# maze.draw(highlight2=path, blink=(maze.keys['r'], maze.keys['z']))

#maze.draw(highlight1=squares, highlight2=path, blink=reach_keys.values())
# path = maze.find_path(maze.keys['a'], maze.keys['w'], ignore_doors=True)
# maze.draw(highlight2=path, blink=[maze.keys['a'], maze.keys['w']])

# print(maze.reachable_keys('@', []))

best_dist, best_route = maze.find_fastest_route()
print(best_dist, best_route)
