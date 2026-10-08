from pathlib import Path
import numpy as np
ROWS = 5760
COLUMNS = 11520
MARS_RADIUS = 3_396_000.0

PIXEL_PER_DEGREE=32.0
NODATA_VALUE = 0



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

terrain[terrain == NODATA_VALUE] = np.nan #NODATA HANDLING with boolean mask

DEG_PER_PIXEL = 1.0 / PIXEL_PER_DEGREE
RAD_PER_PIXEL = np.radians(DEG_PER_PIXEL)

dy = MARS_RADIUS * RAD_PER_PIXEL

rows = np.arange(ROWS)
latitudes = 90 - (rows + 0.5) * DEG_PER_PIXEL # APPROX latitude of each pixel center
latitudes_radians = np.radians(latitudes)

dx = MARS_RADIUS * np.cos(latitudes_radians) * RAD_PER_PIXEL

print("Terrain Shape: ", terrain.shape)
print("North-South Pixel Distance: ",dy)
print("East-West Pixel Distance at Equator: ",dx[ROWS // 2] )
print("East-West Pixel Distance near North Pole: ",dx[0])

# ============================================================
# Elevation gradients
# ============================================================

dz_dy = np.full_like(terrain, np.nan)
dz_dx = np.full_like(terrain, np.nan)

valid_vertical = (
    ~np.isnan(terrain[:-2, :]) &
    ~np.isnan(terrain[2:, :])
)

dz_dy[1:-1, :][valid_vertical] = (
    terrain[2:, :][valid_vertical]
    - terrain[:-2, :][valid_vertical]
) / (2.0 * dy)

# ============================================================
# East-West gradient
# ============================================================

east = np.roll(terrain, -1,axis=1) #axis=1 means shift along column nd 0 means along row
west = np.roll(terrain, 1,axis=1) #last column ←→ first column

valid_horizontal = (
    ~np.isnan(east) 
    & ~np.isnan(west))


MIN_DX = 1.0
safe_dx = np.maximum(dx, MIN_DX) #PROTECTION AGINAST TINY VALUE OF ROW AT POLES

horizontal_gradient = ( east - west )/ (2 * safe_dx[: ,np.newaxis])



dz_dx[valid_horizontal] = horizontal_gradient[valid_horizontal]

# ============================================================
# Gradient magnitude
# ============================================================

gradient_magnitude = np.sqrt(
    dz_dx**2 + dz_dy**2
)

# ============================================================
# Convert gradient to slope angle
# ============================================================

slope_degrees = np.degrees(
    np.arctan(gradient_magnitude)
)

print("\nSlope statistics")

print(
    "Minimum:",
    np.nanmin(slope_degrees)
)

print(
    "Maximum:",
    np.nanmax(slope_degrees)
)

print(
    "Mean:",
    np.nanmean(slope_degrees)
)

max_index = np.nanargmax(slope_degrees)
max_row, max_column = np.unravel_index(
    max_index, slope_degrees.shape
)

print("\nMaximum slope location:")
print("Row:", max_row)
print("Column:", max_column)
print("Slope:", slope_degrees[max_row, max_column])

print("Latitude:", latitudes[max_row])

r = 2880
c = 5760
center = terrain[r,c]
north = terrain[r-1,c]
south = terrain[r+1,c]
east = terrain[r,c+1]
west = terrain[r,c-1]

print("\nTest pixel:")
print("Center:", center)
print("North:", north)
print("South:", south)
print("West:", west)
print("East:", east)

manual_dz_dy =(south - north) / (2.0* dy)
manual_dz_dx =(west - east) / (2.0*safe_dx[r])
manual_gradient = np.sqrt(manual_dz_dx**2 + manual_dz_dy**2)
manual_slope = np.degrees(np.arctan(manual_gradient))

print("\nManual calculation:")
print("dz/dy:", manual_dz_dy)
print("dz/dx:", manual_dz_dx)
print("gradient:", manual_gradient)
print("slope:", manual_slope)

print("\nVectorized NumPy calculation:")
print("slope:", slope_degrees[r, c])

print("\n Slope Percentiles")
for percentile in [50,90,95,99,99.9]:
    value = np.nanpercentile(slope_degrees, percentile)
    print(f"{percentile}%: {value:.3f}`")