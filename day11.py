import sys
from collections import defaultdict
from IntcodeComputer import IntcodeComputer

# =================================================

class Robot:

  def __init__(self, program):
    self.program0 = program
    self.reset()

  def reset(self):
    self.computer = IntcodeComputer(program)
    self.panels = defaultdict(lambda: 0)

  def run(self, part):
    self.its = 0
    self.x = self.y = 0
    self.direction = "up"
    if part == 2:
      self.panels[(0,0)] = 1
    while True:
      over_color = self.panels[(self.x, self.y)]
      # print(self.its, self.x, self.y, over_color, self.direction)
      self.computer.inputs.put(over_color)
      self.computer.execute(pause_on_output=True, quiet=True)
      self.computer.execute(pause_on_output=True, quiet=True)
      to_paint = self.computer.outputs[-2]
      turn_to = self.computer.outputs[-1]
      # print("paint:", to_paint)
      self.panels[(self.x,self.y)] = to_paint
      self.turn(turn_to)
      self.advance()
      # print("turn to:", turn_to)
      self.its += 1
      if self.computer.halted:
        if part == 1:
          print("Part 1:", len(self.panels))
          break
        elif part == 2:
          print("Part 2:")
          xs = [x[0] for x in self.panels.keys() if self.panels[x] == 1]
          ys = [x[1] for x in self.panels.keys() if self.panels[x] == 1]
          xmin, xmax = min(xs), max(xs)
          ymin, ymax = min(ys), max(ys)
          for y in range(ymax, ymin-1, -1):
            for x in range(xmin, xmax+1):
              if (x,y) in self.panels and self.panels[(x,y)] == 1:
                print("#", end="")
              else:
                print(" ", end="")
              print(" ", end="")
            print()
          break

  def turn(self, turn_to):
    if turn_to == 0:
      if self.direction == "up": self.direction = "left"
      elif self.direction == "left": self.direction = "down"
      elif self.direction == "down": self.direction = "right"
      elif self.direction == "right": self.direction = "up"
    elif turn_to == 1:
      if self.direction == "up": self.direction = "right"
      elif self.direction == "right": self.direction = "down"
      elif self.direction == "down": self.direction = "left"
      elif self.direction == "left": self.direction = "up"

  def advance(self):
    if self.direction == "up": self.y += 1
    elif self.direction == "right": self.x += 1
    elif self.direction == "left": self.x -= 1
    elif self.direction == "down": self.y -= 1

# =================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

robot = Robot(program)

# Part 1
robot.run(part=1)

# Part 2
robot.reset()
robot.run(part=2)
