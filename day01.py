from math import floor

def compute_fuel(mass):
  return floor(mass/3) - 2

def compute_fuel_part2(mass):
  tot_fuel = compute_fuel(mass)
  mass = tot_fuel
  while True:
    fuel = compute_fuel(mass)
    if fuel <= 0: break
    tot_fuel += fuel
    mass = fuel
  return tot_fuel

# Load input
masses = []
with open("day1.in") as f:
  for line in f:
    masses.append(int(line))

# Part 1
total_fuel_1 = sum([compute_fuel(m) for m in masses])
print(f"Part 1: {total_fuel_1}")

# Part 2
total_fuel_2 = sum([compute_fuel_part2(m) for m in masses])
print(f"Part 2: {total_fuel_2}")
