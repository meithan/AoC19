import os
import sys
import time

from IntcodeComputer import IntcodeComputer

# =================================================

class Game:

  def __init__(self):
    self.computer = None
    self.score = None
    self.ball_x = None
    self.ball_y = None
    self.paddle_x = None
    self.paddle_y = None
    self.blocks = None

  def initiliaze(self, program):

    temp = {}
    self.computer = IntcodeComputer(program)

    while True:
      x, y, tileid = self.step()
      if self.computer.halted or (x == -1 and y == 0):
        break
      temp[(x,y)] = tileid

    xs = [p[0] for p in temp.keys()]
    ys = [p[1] for p in temp.keys()]
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    self.nx = xmax - xmin + 1
    self.ny = ymax - ymin + 1

    self.tiles = []
    for i in range(self.nx):
      self.tiles.append([0]*self.ny)

    for pos in temp:
      x, y = pos
      tileid = temp[pos]
      self.tiles[x][y] = tileid
      if tileid == 4:
        self.ball_x = x
        self.ball_y = y
      elif tileid == 3:
        self.paddle_x = x
        self.paddle_y = y
      elif tileid == 2:
        if self.blocks is None:
          self.blocks = 1
        else:
          self.blocks += 1

    self.score = 0

  def update(self, x, y, tileid):
    self.tiles[x][y] = tileid
    if tileid == 3:
      self.paddle_x = x
      self.paddle_y = y
    elif tileid == 4:
      self.ball_x = x
      self.ball_y = y
    elif x == -1:
      self.score = tileid

  def autoplay(self):

    self.computer.inputs.put(0)

    while True:
      x, y, tileid = self.step()
      if x is None:
        break
      self.update(x, y, tileid)
      if tileid == 3:
        os.system('clear')
        self.draw()
        # time.sleep(0.0001)
      elif tileid == 4:
        self.computer.inputs.queue.clear()
        if self.paddle_x < self.ball_x:
          self.computer.inputs.put(1)
        elif self.paddle_x > self.ball_x:
          self.computer.inputs.put(-1)
        else:
          self.computer.inputs.put(0)
    os.system('clear')
    self.draw()

  def step(self):
    self.computer.execute(quiet=True, pause_on_output=True)
    self.computer.execute(quiet=True, pause_on_output=True)
    self.computer.execute(quiet=True, pause_on_output=True)
    if len(self.computer.outputs) >= 3:
      x = self.computer.outputs[-3]
      y = self.computer.outputs[-2]
      tileid = self.computer.outputs[-1]
    else:
      return None, None, None
    self.computer.outputs = []
    return x, y, tileid

  def draw(self):
    for y in range(self.ny):
      symbols = []
      for x in range(self.nx):
        if self.tiles[x][y] == 0:
          symbols.append(" ")
        elif self.tiles[x][y] == 1:
          symbols.append("#")
        elif self.tiles[x][y] == 2:
          symbols.append("B")
        elif self.tiles[x][y] == 3:
          symbols.append("=")
        elif self.tiles[x][y] == 4:
          symbols.append("o")
      print("".join(symbols))
    print("Score:", self.score)


# =================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

program[0] = 2
game = Game()
game.initiliaze(program)
game.draw()
input("Press ENTER to start game")

game.autoplay()

print("Part 1:", game.blocks)
print("Part 2:", game.score)
