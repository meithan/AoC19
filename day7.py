import sys
from queue import Queue

class IntcodeComputer:

  def __init__(self, program, inputs=[]):
    self.memory = program
    self.inputs = Queue()
    for item in inputs:
      self.inputs.put(item)
    self.outputs = []
    self.last_output = None
    self.ptr = 0
    self.halted = False

  def execute(self, quiet=False, pause_on_output=False):

    while True:

      instruction = self.memory[self.ptr]
      opcode, nargs, modes = self.decode(instruction)
      # print("ptr=",self.ptr,"instruction=",instruction)

      if opcode == 99:
        self.halted = True
        return

      params = []
      for i in range(1,nargs+1):
        params.append(self.memory[self.ptr+i])

      # ADD
      if opcode == 1:
        A = self.memory[params[0]] if modes[0] == 0 else params[0]
        B = self.memory[params[1]] if modes[1] == 0 else params[1]
        self.memory[params[2]] = A + B
        self.ptr += nargs + 1

      # MULT
      elif opcode == 2:
        A = self.memory[params[0]] if modes[0] == 0 else params[0]
        B = self.memory[params[1]] if modes[1] == 0 else params[1]
        self.memory[params[2]] = A * B
        self.ptr += nargs + 1

      # INPUT
      elif opcode == 3:
        if not self.inputs.empty():
          next_input = self.inputs.get()
          if not quiet:
            print("input>", next_input)
          self.memory[params[0]] = next_input
          next_input += 1
        else:
          answer = int(input("input> "))
          self.memory[params[0]] = answer
        self.ptr += nargs + 1

      # OUTPUT
      elif opcode == 4:
        A = self.memory[params[0]] if modes[0] == 0 else params[0]
        if not quiet:
          print(f"output> {A}")
        self.outputs.append(A)
        self.last_output = A
        self.ptr += nargs + 1
        if pause_on_output:
          return

      # JUMP_TRUE
      elif opcode == 5:
        A = self.memory[params[0]] if modes[0] == 0 else params[0]
        B = self.memory[params[1]] if modes[1] == 0 else params[1]
        if A != 0:
          self.ptr = B
        else:
          self.ptr += nargs + 1

      # JUMP_FALSE
      elif opcode == 6:
        A = self.memory[params[0]] if modes[0] == 0 else params[0]
        B = self.memory[params[1]] if modes[1] == 0 else params[1]
        if A == 0:
          self.ptr = B
        else:
          self.ptr += nargs + 1

      # LESS_THAN
      elif opcode == 7:
        A = self.memory[params[0]] if modes[0] == 0 else params[0]
        B = self.memory[params[1]] if modes[1] == 0 else params[1]
        self.memory[params[2]] = 1 if A < B else 0
        self.ptr += nargs + 1

      # EQUAL
      elif opcode == 8:
        A = self.memory[params[0]] if modes[0] == 0 else params[0]
        B = self.memory[params[1]] if modes[1] == 0 else params[1]
        self.memory[params[2]] = 1 if A == B else 0
        self.ptr += nargs + 1

  def decode(self, instruction):

    opcode = instruction % 100

    if opcode == 1: nargs = 3
    elif opcode == 2: nargs = 3
    elif opcode == 3: nargs = 1
    elif opcode == 4: nargs = 1
    elif opcode == 5: nargs = 2
    elif opcode == 6: nargs = 2
    elif opcode == 7: nargs = 3
    elif opcode == 8: nargs = 3
    elif opcode == 99: nargs = 0

    modes = []
    m = instruction // 100
    for i in range(nargs):
      modes.append(m % 10)
      m = m // 10

    return (opcode, nargs, modes)

# -----------------------------------------------

def try_sequence_part1(phase_settings, program):

  last_output = 0
  for phase in phase_settings:
    computer = IntcodeComputer(program, inputs=(phase, last_output))
    computer.execute(quiet=True)
    last_output = computer.last_output

  thruster_signal = last_output
  return thruster_signal

# -----------------------------------------------

def try_sequence_part2(phase_settings, program):

  computers = {}
  for i,name in enumerate(["A", "B", "C", "D", "E"]):
    computers[name] = IntcodeComputer(program, inputs=[phase_settings[i]])

  last_output = 0
  finished = False
  while not finished:
    for name in ["A", "B", "C", "D", "E"]:
      computer = computers[name]
      computer.inputs.put(last_output)
      computer.execute(pause_on_output=True, quiet=True)
      last_output = computer.last_output
      if name == "E" and computer.halted:
        finished = True

  thruster_signal = last_output
  return thruster_signal

# -----------------------------------------------

# Yields all permutations of elems sequentially
def permutations(elems):
  if len(elems) <= 1:
    yield elems
  else:
    for perm in permutations(elems[1:]):
      for i in range(len(perm)+1):
        yield perm[:i] + elems[0:1] + perm[i:]

# ========================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

# Part 1

# sequence = (4,3,2,1,0)  # test1
# sequence = (0,1,2,3,4)  # test2
# sequence = (1,0,4,3,2)  # test3
# try_sequence(sequence, program)
highest_signal = None
for phase_settings in permutations((0,1,2,3,4)):
  thruster_signal = try_sequence_part1(phase_settings, program)
  if highest_signal is None or thruster_signal > highest_signal:
    highest_signal = thruster_signal
  # print(phase_settings, thruster_signal)
print("Part 1:", highest_signal)

# Part 2

highest_signal = None
for phase_settings in permutations((5,6,7,8,9)):
  thruster_signal = try_sequence_part2(phase_settings, program)
  if highest_signal is None or thruster_signal > highest_signal:
    highest_signal = thruster_signal
  # print(phase_settings, thruster_signal)
print("Part 2:", highest_signal)
