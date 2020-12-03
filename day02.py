import sys

from IntcodeComputer import IntcodeComputer

# Load input
with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

# Part 1

# Set program input to "1202 program alarm"
program[1] = 12
program[2] = 2

computer = IntcodeComputer(program)
computer.execute()

print(f"Part 1: {computer.memory[0]}")

# Part 2

for A in range(0,100):
  for B in range(0,100):

    program[1] = A
    program[2] = B

    computer = IntcodeComputer(program)
    computer.execute()
    result = computer.memory[0]

    if result == 19690720:
      print(f"Part 2: {100*A + B}")
