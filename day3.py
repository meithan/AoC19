import sys

# ===========================================

class Segment:
  def __init__(self, orient, x1, y1, x2, y2, prev_steps):
    self.orient = orient
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.prev_steps = prev_steps

def gen_segments(wire_moves):
  segments = []
  x = y = 0
  steps = 0
  for move in wire_moves:
    direc = move[0]
    length = int(move[1:])
    if direc in ["R", "L"]:
      orient = "h"
      dx = (-1 if direc == "L" else 1) * length
      dy = 0
    elif direc in ["U", "D"]:
      orient = "v"
      dx = 0
      dy = (-1 if direc == "D" else 1) * length
    nx = x + dx
    ny = y + dy
    segments.append(Segment(orient, x, y, nx, ny, steps))
    x = nx
    y = ny
    steps += length
  return segments

def Manhattan(x1, y1, x2, y2):
  return abs(x1-x2) + abs(y1-y2)

def intersect(segment1, segment2):
  if segment1.orient == "h" and segment2.orient == "v":
    xlo = min(segment1.x1, segment1.x2)
    xhi = max(segment1.x1, segment1.x2)
    ylo = min(segment2.y1, segment2.y2)
    yhi = max(segment2.y1, segment2.y2)
    if xlo <= segment2.x1 <= xhi and ylo <= segment1.y1 <= yhi:
      return (segment2.x1, segment1.y1)
  elif segment1.orient == "v" and segment2.orient == "h":
    xlo = min(segment2.x1, segment2.x2)
    xhi = max(segment2.x1, segment2.x2)
    ylo = min(segment1.y1, segment1.y2)
    yhi = max(segment1.y1, segment1.y2)
    if xlo <= segment1.x1 <= xhi and ylo <= segment2.y1 <= yhi:
      return (segment1.x1, segment2.y1)
  return None

# ===========================================

wires = []
with open(sys.argv[1]) as f:
  for line in f:
    wires.append(line.strip().split(","))

segments1 = gen_segments(wires[0])
segments2 = gen_segments(wires[1])

import matplotlib.pyplot as plt

xs = [seg.x1 for seg in segments1] + [segments1[-1].x2]
ys = [seg.y1 for seg in segments1] + [segments1[-1].y2]
plt.plot(xs, ys)
xs = [seg.x1 for seg in segments2] + [segments2[-1].x2]
ys = [seg.y1 for seg in segments2] + [segments2[-1].y2]
plt.plot(xs, ys)
plt.gca().set_aspect("equal")

closest_inter = None
closest_dist = None
fastest_inter = None
fastest_steps = None
for seg1 in segments1:
  for seg2 in segments2:

    inter = intersect(seg1, seg2)
    if inter is not None and inter != (0,0):
      xi, yi = inter

      dist = Manhattan(0, 0, xi, yi)
      if closest_dist is None or dist < closest_dist:
        closest_dist = dist
        closest_inter = inter

      steps1 = seg1.prev_steps + Manhattan(seg1.x1, seg1.y1, xi, yi)
      steps2 = seg2.prev_steps + Manhattan(seg2.x1, seg2.y1, xi, yi)
      tot_steps = steps1 + steps2
      if fastest_steps is None or tot_steps < fastest_steps:
        fastest_steps = tot_steps
        fastest_inter = inter

      plt.scatter([inter[0]], [inter[1]], marker="o", color="k", fc="none", zorder=10)
      print(inter, dist, tot_steps)
    # print(seg1, seg2)

plt.scatter([closest_inter[0]], [closest_inter[1]], s=200, marker="x", color="r", zorder=-10)
plt.scatter([fastest_inter[0]], [fastest_inter[1]], s=200, marker="x", color="g", zorder=-10)

print(f"Part 1: {closest_dist}")
print(f"Part 1: {fastest_steps}")

plt.plot([0], [0], "ko")
plt.tight_layout()
plt.show()
