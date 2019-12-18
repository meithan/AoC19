import math
import re
import sys

# ==================================================

class Moon:

  def __init__(self, name, x0, y0, z0):
    self.name = str(name)
    self.x = int(x0)
    self.y = int(y0)
    self.z = int(z0)
    self.vx = 0
    self.vy = 0
    self.vz = 0

  def __repr__(self):
    return f'<"{self.name}" at {self.x},{self.y},{self.z}>'

  def move(self):
    self.x += self.vx
    self.y += self.vy
    self.z += self.vz

  def pot_energy(self):
    return abs(self.x) + abs(self.y) + abs(self.z)

  def kin_energy(self):
    return abs(self.vx) + abs(self.vy) + abs(self.vz)

  def tot_energy(self):
    return self.pot_energy() * self.kin_energy()

def do_step(moons):

  num_moons = len(moons)
  for i in range(num_moons):
    for j in range(i+1, num_moons):
      moon1 = moons[i]
      moon2 = moons[j]
      if moon1.x < moon2.x:
        moon1.vx += 1
        moon2.vx -= 1
      elif moon1.x > moon2.x:
        moon1.vx -= 1
        moon2.vx += 1
      if moon1.y < moon2.y:
        moon1.vy += 1
        moon2.vy -= 1
      elif moon1.y > moon2.y:
        moon1.vy -= 1
        moon2.vy += 1
      if moon1.z < moon2.z:
        moon1.vz += 1
        moon2.vz -= 1
      elif moon1.z > moon2.z:
        moon1.vz -= 1
        moon2.vz += 1

  for moon in moons:
    moon.move()

def system_energy(moons):
  E = 0
  for moon in moons:
    E += moon.tot_energy()
  return E

def lcm(a, b):
  return abs(a*b) // math.gcd(a, b)

# ==================================================

moons = []
with open(sys.argv[1]) as f:
  count = 0
  for line in f:
    pattern = "<[xyz]=([-0-9]*), ?[xyz]=([-0-9]*), ?[xyz]=([-0-9]*)>"
    matches = re.match(pattern, line.strip())
    count += 1
    x0 = matches.group(1)
    y0 = matches.group(2)
    z0 = matches.group(3)
    moons.append(Moon(count, x0, y0, z0))

x_period = None
x_states = set()
y_period = None
y_states = set()
z_period = None
z_states = set()
step = 0
while True:

  do_step(moons)
  step += 1

  if x_period is None:
    x_state = tuple(m.x for m in moons) + tuple(m.vx for m in moons)
    if x_state in x_states:
      x_period = step-1
      print("x-period:", x_period)
    else:
      x_states.add(x_state)

  if y_period is None:
    y_state = tuple(m.y for m in moons) + tuple(m.vy for m in moons)
    if y_state in y_states:
      y_period = step-1
      print("y-period:", y_period)
    else:
      y_states.add(y_state)

  if z_period is None:
    z_state = tuple(m.z for m in moons) + tuple(m.vz for m in moons)
    if z_state in z_states:
      z_period = step-1
      print("z-period:", z_period)
    else:
      z_states.add(z_state)

  if step == 1000:
    print("Part 1:", system_energy(moons))

  if x_period is not None and y_period is not None and z_period is not None and step >= 1000:
    break

global_period = lcm(lcm(x_period, y_period), z_period)
print("Part 2:", global_period)
