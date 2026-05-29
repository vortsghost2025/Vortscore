import hdc_engine
import numpy as np

# Create two dummy vectors of size 10 (bipolar: -1 or 1)
vec1 = np.array([1, -1, 1, -1, 1, -1, 1, -1, 1, -1], dtype=np.int8)
vec2 = np.array([1, 1, -1, -1, 1, 1, -1, -1, 1, 1], dtype=np.int8)

# Perform the bind operation
result = hdc_engine.bind(vec1, vec2)

print(f"Vector A: {vec1}")
print(f"Vector B: {vec2}")
print(f"Result  : {result}")
