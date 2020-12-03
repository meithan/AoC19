import sys

# =================================================

def get_mult(k, i, base_pattern=(0, 1, 0, -1)):
  j = (i+1) // (k+1)
  return base_pattern[j % len(base_pattern)]

def do_phases_full(input_signal, num_phases, base_pattern=(0, 1, 0, -1)):
  import numpy as np
  N = len(input_signal)
  F = []
  for k in range(N):
    row = [get_mult(k, i, base_pattern=base_pattern) for i in range(N)]
    F.append(row)
  F = np.array(F)
  x = np.array(input_signal)
  for phase in range(num_phases):
    x = np.abs(np.dot(F, x)) % 10
    print(phase)
  return x

def solve_part2(input_signal, num_phases, repeats, offset_len, output_len, base_pattern):

  offset = int(join_digits(input_signal[:offset_len]))
  # signal = []
  # for k in range(offset, len(input_signal)*repeats):
  #   signal.append(input_signal[k % len(input_signal)])
  signal = (input_signal*repeats)[offset:]

  print(f"len(input_signal)= {len(input_signal)}")
  print(f"len(tot_input_signal)= {len(input_signal)*repeats}")
  print(f"offset= {offset}")
  print(f"len(signal)=", len(signal))

  # output = input_signal[offset:offset+output_len]
  # for k in range(offset, offset+output_len):
  #   i1 = k
  #   i2 = signal_len-1
  #   s = 0
  #   for i in range(i1, i2+1):
  #     if get_mult(k, i) == 1:
  #       s +=




def join_digits(digits):
  return "".join([str(x) for x in digits])

# =================================================

with open(sys.argv[1]) as f:
  input_signal = [int(x) for x in f.read().strip()]

# Part 1

# output_signal = do_phases_full(input_signal, 100, (0, 1, 0, -1))
# print("Part 1:", join_digits(output_signal)[:8])


# Part 2

input_signal = [int(x) for x in "03036732577212944063491565474664"]

output_signal = solve_part2(input_signal, num_phases=100, repeats=10000, offset_len=7, output_len=8, base_pattern=(0, 1, 0, -1))




# offset = "".join(input_signal[:7])
