from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
data_folder = Path(__file__).parent.parent / "data"
img_file = data_folder / "megt90n000fb.img"

rows = 5760
columns = 11520

terrain = np.fromfile(
    img_file, 
    dtype=">i2")

print("Number of values: ",terrain.size)
print("Expected values: ",rows * columns)

terrain = terrain.reshape(rows,columns)

print("Shape:",terrain.shape)
print("Data Type",terrain.dtype)

print("minimum:",terrain.min())
print("maximum:",terrain.max())


print("\n Sample Terrain Values:")
print("Top-Left:",terrain[0,0])
print("Center", terrain[rows // 2, columns // 2])
print("Bottom-Right:", terrain[-1,-1])
