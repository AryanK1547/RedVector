from pathlib import Path
import numpy as np
COLUMNS = 11520
ROWS = 5760 
MARS_RADIUS = 3396000.0
CENTRAL_MERIDIAN = 180.0
PIXEL_SIZE = 2 * np.pi * MARS_RADIUS / COLUMNS   # exact, = 1852.2306...
REF_COL = COLUMNS / 2   # 5760.0
REF_ROW = ROWS / 2     # 2880.0

data_dir = Path(__file__).parent.parent / "data"
img_file = data_dir / "megt90n000fb.img"

terrain = np.fromfile(img_file, dtype=">i2").reshape(ROWS,COLUMNS)

def latlon_to_pixel(latitude, longitude):
    if latitude < -90 or latitude > +90:
        raise ValueError("Latitude Value out of Bounds")
    
    longitude_difference = (longitude - CENTRAL_MERIDIAN +180) % 360 - 180
    lat_radian = np.radians(latitude)
    long_radian = np.radians(longitude_difference)

    x = long_radian * MARS_RADIUS
    y = lat_radian * MARS_RADIUS

    column = int(np.floor(round(x,6)))
    row = int(np.floor(round(y,6)))

    column = min(max(column,0),COLUMNS-1)
    row = min(max(row,0),ROWS -1)

    return row , column

def get_elevation(latitude, longitude):
    row , column = latlon_to_pixel(latitude,longitude)
    elevation = terrain[row,column]
    return elevation

latitude = 0
longitude = 180

elevation = get_elevation(latitude,longitude)
print("Location:")
print("Latitude:", latitude)
print("Longitude:", longitude)

print("\nRaster cell:")
print("Elevation:", elevation)
