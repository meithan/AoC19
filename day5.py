import sys

from IntcodeComputer import IntcodeComputer

# =================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

# Run program and give it either input 1 (Part 1) or 5 (Part 2)
computer = IntcodeComputer(program)
computer.execute()
