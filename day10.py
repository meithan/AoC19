from math import atan2, pi
import sys

def gcd(a, b):
  if a == 0:
    return 1
  if b == 0:
    return a
  r = a % b
  return gcd(b, r)

def reduce(a, b):
  if a == 0:
    return 0, b // abs(b)
  elif b == 0:
    return a // abs(a), 0
  sa = +1 if a >= 0 else -1
  sb = +1 if b >= 0 else -1
  a = abs(a)
  b = abs(b)
  d = gcd(a, b)
  return sa * a // d, sb * b // d

def visible(asteroids, x0, y0):
  families = {}
  for (xa, ya) in asteroids:
    if (xa, ya) != (x0, y0):
      # print("checking:", xa, ya)
      dx = xa - x0
      dy = ya - y0
      xr, yr = reduce(dx, dy)
      if (xr, yr) not in families:
        families[xr,yr] = []
        # print("Adding ray",xr,yr)
      families[xr,yr].append((xa, ya))
  # print("visible:", num_visible)
  return families

def best_asteroid(asteroids):
  best = None
  max_visible = None
  for xa, ya in asteroids:
    # print("\n> Asteroid", xa, ya)
    families = visible(asteroids, xa, ya)
    num_visible = len(families)
    if best is None or num_visible > max_visible:
      best = (xa, ya)
      max_visible = num_visible
  return best, max_visible

def cw_angle(xp, yp):
  theta = atan2(xp, -yp)
  while theta < 0:
    theta += 2*pi
  return theta * 180 / pi

# ===========================

asteroids = []
nx = None; ny = None
with open(sys.argv[1]) as f:
  y = 0
  for line in f:
    for x in range(len(line.strip())):
      if line[x] == "#":
        asteroids.append((x,y))
    if nx is None: nx = len(line.strip())
    y += 1
ny = y

# Part 1

station_coords, num_visible = best_asteroid(asteroids)
print("Part 1:", num_visible)

# Part 2

x0, y0 = station_coords
print("Station at", x0, y0)

# Within each family, sort asteroids by distance to station
num_roids = 0
families = visible(asteroids, x0, y0)
for key in families.keys():
  families[key].sort(key=lambda coords: (coords[0]-x0)**2+(coords[1]-y0)**2, reverse=True)
  num_roids += len(families[key])

# Destroy asteroids
destroyed_roids = []
while len(destroyed_roids) < num_roids:
  # Pop last element in each family, build in list
  to_destroy = []
  for key in families.keys():
    if len(families[key]) == 0:
      continue
    roid = families[key].pop()
    to_destroy.append(roid)
  # Sort list by CW angle
  to_destroy.sort(key=lambda p: cw_angle(p[0]-x0, p[1]-y0))
  # Destroy roids!
  for roid in to_destroy:
    destroyed_roids.append(roid)

x200, y200 = destroyed_roids[199]
print("Part 2:", 100*x200 + y200)
