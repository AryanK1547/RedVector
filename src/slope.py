from pathlib import Path
import numpy as np
ROWS = 5760
COLUMNS = 11520

PIXEL_SIZE = 1852.2306687


data_folder = Path(__file__).parent.parent / "data"

img_file = data_folder / "megt90n000fb.img"


# -----------------------------
# Read the MOLA raster
# -----------------------------

terrain = np.fromfile(
    img_file,
    dtype=">i2"
).reshape(ROWS, COLUMNS)

terrain = terrain.astype(np.float64)
dz_dy,dz_dx = np.gradient(terrain,PIXEL_SIZE,PIXEL_SIZE)

slope = np.sqrt(dz_dx**2 + dz_dy**2)
slope_degrees = np.degrees(
    np.arctan(slope)
)

print("Terrain shape:", terrain.shape)

print("Slope shape:", slope_degrees.shape)

print("Minimum slope:", np.min(slope_degrees))

print("Maximum slope:", np.max(slope_degrees))

print("Average slope:", np.mean(slope_degrees))