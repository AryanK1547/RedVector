from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

data_folder = Path(__file__).parent.parent / "data"

img_file = data_folder / "megt90n000fb.img"

rows = 5760 
columns = 11520 

terrain = np.fromfile(img_file , dtype=">i2")
terrain = terrain.reshape(rows, columns)

plt.imshow(terrain, cmap="terrain")
plt.title("MOLA Mars Terrain")
plt.xlabel("Column")
plt.ylabel("Row")
plt.show()