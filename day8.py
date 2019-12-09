import sys

# Load input
# width = 3; height = 2
# width = 2; height = 2;
width = 25; height = 6
with open(sys.argv[1]) as f:
  digits = f.read().strip()

# Separate layers
layer_len = width * height
assert len(digits) % layer_len == 0
num_layers = len(digits) // layer_len
layers = []
for i in range(num_layers):
  layers.append(digits[i*layer_len:(i+1)*layer_len])

# Part 1

fewest_zeros = None
selected_layer = None
for l in range(num_layers):
  num_zeros = layers[l].count('0')
  if fewest_zeros is None or num_zeros < fewest_zeros:
    fewest_zeros = num_zeros
    selected_layer = layers[l]
answer = selected_layer.count('1') * selected_layer.count('2')
print("Part 1:", answer)

# Part 2

final_image = []
for j in range(height):
  final_image.append(["?"]*width)

for i in range(width):
  for j in range(height):
    for l in range(num_layers):
      idx = j*width + i
      if layers[l][idx] != '2':
        final_image[j][i] = layers[l][idx]
        break

result = ""
for j in range(height):
  s = "".join(final_image[j]).replace("1", "O").replace("0", " ")
  result += s + "\n"

print("Part 2:")
print(result)
