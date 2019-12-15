import sys

from IntcodeComputer import IntcodeComputer

# =================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

# Part 1: run with input = 1
# Part 2: run with input = 2
computer = IntcodeComputer(program)
computer.execute()
