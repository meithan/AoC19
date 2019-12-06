import sys

class IntcodeComputer:

  def run_program(self, program):

    memory = program[:]
    ptr = 0
    while True:

      instruction = memory[ptr]
      opcode, nargs, modes = self.decode(instruction)
      # print("ptr=",ptr,"instruction=",instruction)

      if opcode == 99:
        break

      params = []
      for i in range(1,nargs+1):
        params.append(memory[ptr+i])

      if opcode == 1:
        A = memory[params[0]] if modes[0] == 0 else params[0]
        B = memory[params[1]] if modes[1] == 0 else params[1]
        memory[params[2]] = A + B
        ptr += nargs + 1

      elif opcode == 2:
        A = memory[params[0]] if modes[0] == 0 else params[0]
        B = memory[params[1]] if modes[1] == 0 else params[1]
        memory[params[2]] = A * B
        ptr += nargs + 1

      elif opcode == 3:
        answer = int(input("input> "))
        memory[params[0]] = answer
        ptr += nargs + 1

      elif opcode == 4:
        A = memory[params[0]] if modes[0] == 0 else params[0]
        print(f"output> {A}")
        ptr += nargs + 1

      elif opcode == 5:
        A = memory[params[0]] if modes[0] == 0 else params[0]
        B = memory[params[1]] if modes[1] == 0 else params[1]
        if A != 0:
          ptr = B
        else:
          ptr += nargs + 1

      elif opcode == 6:
        A = memory[params[0]] if modes[0] == 0 else params[0]
        B = memory[params[1]] if modes[1] == 0 else params[1]
        if A == 0:
          ptr = B
        else:
          ptr += nargs + 1

      elif opcode == 7:
        A = memory[params[0]] if modes[0] == 0 else params[0]
        B = memory[params[1]] if modes[1] == 0 else params[1]
        memory[params[2]] = 1 if A < B else 0
        ptr += nargs + 1

      elif opcode == 8:
        A = memory[params[0]] if modes[0] == 0 else params[0]
        B = memory[params[1]] if modes[1] == 0 else params[1]
        memory[params[2]] = 1 if A == B else 0
        ptr += nargs + 1

    return memory

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


# =================================================

with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

# Run program and give it either input 1 (Part 1) or 5 (Part 2)
computer = IntcodeComputer()
memory = computer.run_program(program)
