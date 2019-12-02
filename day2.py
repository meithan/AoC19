import sys

def run_program(program):

  memory = program[:]
  ptr = 0
  opcode = memory[0]

  while opcode != 99:

    ptr_A = memory[ptr+1]
    ptr_B = memory[ptr+2]
    ptr_C = memory[ptr+3]
    val_A = memory[ptr_A]
    val_B = memory[ptr_B]

    if opcode == 1:
      result = val_A + val_B
    elif opcode == 2:
      result = val_A * val_B

    memory[ptr_C] = result

    ptr += 4
    opcode = memory[ptr]

  return memory

# Load input
with open(sys.argv[1]) as f:
  program = [int(x) for x in f.readline().split(",")]

# Part 1

# Set program input to "1202 program alarm"
program[1] = 12
program[2] = 2

final_mem = run_program(program)
result = final_mem[0]
print(f"Part 1: {result}")

# Part 2

for A in range(0,100):
  for B in range(0,100):
  
    program[1] = A
    program[2] = B
    
    final_mem = run_program(program)
    result = final_mem[0]
    
    if result == 19690720:
    

      #print(A, B, result)
      print(f"Part 2: {100*A + B}")

