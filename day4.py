import sys

#  Going from left to right, the digits never decrease
def check_never_decrease(s):
  for i in range(len(s)-1):
    if s[i] > s[i+1]:
      return False
  return True

# Count lengths of repeated groups (for Part 2)
def count_repeated_runs(s):
  d = s[0]
  run = 0
  repeated_runs = []
  for i in range(len(s)):
    if s[i] == d:
      run += 1
    else:
      repeated_runs.append(run)
      d = s[i]
      run = 1
  repeated_runs.append(run)
  return repeated_runs

def check_pass(s):

  never_decrease = check_never_decrease(s)
  if not never_decrease:
    return False, False

  pass1 = pass2 = False
  for run in count_repeated_runs(s):
    if run >= 2:
      pass1 = True
      if run == 2:
        pass2 = True
  return pass1, pass2

def count_possible_passwords(first, last):

  count1 = 0
  count2 = 0
  n = first
  while n <= last:
    s = str(n)
    pass1, pass2 = check_pass(s)
    if pass1:
      count1 += 1
    if pass2:
      count2 += 1
    n += 1

  return count1, count2

# =======================================

with open(sys.argv[1]) as f:
  tokens = f.readline().strip().split("-")
  first = int(tokens[0])
  last = int(tokens[1])

count1, count2 = count_possible_passwords(first, last)
print(f"Part 1: {count1}")
print(f"Part 2: {count2}")
