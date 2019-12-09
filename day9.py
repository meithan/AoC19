import sys
from queue import Queue
from collections import defaultdict

class IntcodeComputer:

  def __init__(self, program, inputs=[]):
    self.memory = defaultdict(lambda: 0)
    for i in range(len(program)):
      self.memory[i] = program[i]
    self.inputs = Queue()
    for item in inputs:
      self.inputs.put(item)
    self.outputs = []
    self.last_output = None
    self.ptr = 0
    self.relbase = 0
    self.halted = False

  def deref_params(self, params, modes, num):
    for i in range(num):
      if modes[i] == 0:
        params[i] = self.memory[params[i]]
      elif modes[i] == 1:
        pass
      elif modes[i] == 2:
        params[i] = self.memory[self.relbase + params[i]]
    return params

  def execute(self, quiet=False, pause_on_output=False):

    while True:

      instruction = self.memory[self.ptr]
      opcode, nargs, modes = self.decode(instruction)
      # print("ptr=",self.ptr,"instruction=",instruction)

      if opcode == 99:
        self.halted = True
        return

      # Read parameters
      params = [self.memory[self.ptr+i] for i in range(1,nargs+1)]

      # ADD
      if opcode == 1:
        params = self.deref_params(params, modes, 2)
        if modes[2] == 0: addr = params[2]
        elif modes[2] == 2: addr = self.relbase + params[2]
        self.memory[addr] = params[0] + params[1]
        self.ptr += nargs + 1

      # MULT
      elif opcode == 2:
        params = self.deref_params(params, modes, 2)
        if modes[2] == 0: addr = params[2]
        elif modes[2] == 2: addr = self.relbase + params[2]
        self.memory[addr] = params[0] * params[1]
        self.ptr += nargs + 1

      # INPUT
      elif opcode == 3:
        if modes[0] == 0:
          addr = params[0]
        elif modes[0] == 2:
          addr = self.relbase + params[0]
        if not self.inputs.empty():
          next_input = self.inputs.get()
          if not quiet:
            print("input>", next_input)
          self.memory[addr] = next_input
          next_input += 1
        else:
          answer = int(input("input> "))
          self.memory[addr] = int(answer)
        self.ptr += nargs + 1

      # OUTPUT
      elif opcode == 4:
        params = self.deref_params(params, modes, 1)
        if not quiet:
          print(f"output> {params[0]}")
        self.outputs.append(params[0])
        self.last_output = params[0]
        self.ptr += nargs + 1
        if pause_on_output:
          return

      # JUMP_TRUE
      elif opcode == 5:
        params = self.deref_params(params, modes, 2)
        if params[0] != 0:
          self.ptr = params[1]
        else:
          self.ptr += nargs + 1

      # JUMP_FALSE
      elif opcode == 6:
        params = self.deref_params(params, modes, 2)
        if params[0] == 0:
          self.ptr = params[1]
        else:
          self.ptr += nargs + 1

      # LESS_THAN
      elif opcode == 7:
        params = self.deref_params(params, modes, 2)
        if modes[2] == 0: addr = params[2]
        elif modes[2] == 2: addr = self.relbase + params[2]
        self.memory[addr] = 1 if params[0] < params[1] else 0
        self.ptr += nargs + 1

      # EQUAL
      elif opcode == 8:
        params = self.deref_params(params, modes, 2)
        if modes[2] == 0: addr = params[2]
        elif modes[2] == 2: addr = self.relbase + params[2]
        self.memory[addr] = 1 if params[0] == params[1] else 0
        self.ptr += nargs + 1

      # REL_OFFSET
      elif opcode == 9:
        params = self.deref_params(params, modes, 1)
        self.relbase += params[0]
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
    elif opcode == 9: nargs = 1
    elif opcode == 99: nargs = 0

    modes = []
    m = instruction // 100
    for i in range(nargs):
      modes.append(m % 10)
      m = m // 10

    return (opcode, nargs, modes)


# ========================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

# Part 1: run with input = 1
# Part 2: run with input = 2
computer = IntcodeComputer(program)
computer.execute()
