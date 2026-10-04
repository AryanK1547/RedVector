from pathlib import Path
import numpy as np

data_dir = Path(__file__).parent.parent
img_file = data_dir / "megt90n000fb.img"


COLUMNS = 11520
ROWS = 5760 
MARS_RADIUS = 3396000.0
CENTRAL_MERIDIAN = 180.0
PIXEL_SIZE = 2 * np.pi * MARS_RADIUS / COLUMNS   # exact, = 1852.2306...
REF_COL = COLUMNS / 2   # 5760.0
REF_ROW = ROWS / 2     # 2880.0


#DEG_PER_PX = 360.0 / COLUMNS        # 0.03125

# Version 1
# def pixel_to_latlon(row, column, pixel_center=False):
#     off = 0.5 if pixel_center else 0.0
#     DEG_PER_PX = 360.0 / 11520          # 0.03125
#     lat = 90.0 - (row + off) * DEG_PER_PX
#     lon = (180.0 + (column + off - 5760) * DEG_PER_PX) % 360.0
#     return lat, lon

#Version 2
def pixel_to_latlon(row, column, pixel_center=True):
    offset = 0.5 if pixel_center else 0.0

    x = (column + offset - REF_COL) * PIXEL_SIZE
    y = (REF_ROW - (row + offset)) * PIXEL_SIZE

    lat = np.degrees(y / MARS_RADIUS)
    lon = CENTRAL_MERIDIAN + np.degrees(x / MARS_RADIUS)

    lat = float(np.clip(lat, -90.0, 90.0))
    lon = round(lon, 9) % 360.0          # round first so -1e-9 becomes 0.0
    return lat, lon


# for row, column in [(2880, 5760), (0, 0), (2880, 0), (2880, 11519)]:
#     lat, lon = pixel_to_latlon(row, column)
#     print(f"row={row}, column={column} -> lat={lat:.4f}°, lon={lon:.4f}°")    


'''The two versions agree exactly. The meter-based one is just the degrees-per-pixel one with an extra round trip through meters, since PIXEL_SIZE / MARS_RADIUS in degrees equals 360/11520. The degrees-per-pixel version is simpler, while this one is useful if you later need to convert to or from projected meters.
pixel_center=True is the right choice for sampling the DEM at a feature's location. Use False only when you need to match the header's corner convention exactly.'''




# for row, column in [(2880, 5760), (0, 0), (2880, 0), (2880, 11519)]:
#     lat, lon = pixel_to_latlon(row, column)
#     print(f"row={row}, column={column} -> lat={lat:.4f}°, lon={lon:.4f}°")    

# Metadata parameters directly from the ENVI header

def latlon_to_pixel(latitude, longitude):
    if latitude < -90 or latitude > +90:
        raise ValueError("Latitude Must be Between -90 to 90")
    
    longitude_diffrence = (longitude - CENTRAL_MERIDIAN + 180) % 360 - 180


    latitude_radians = np.radians(latitude)
    longitude_radians = np.radians(longitude_diffrence)


    x = MARS_RADIUS * longitude_radians
    y = MARS_RADIUS * latitude_radians

    
    column = REF_COL + x / PIXEL_SIZE
    row = REF_ROW - y / PIXEL_SIZE

    row = int(np.floor(round(row, 6)))
    column = int(np.floor(round(column ,6))) 

    row = min(max(row,0),ROWS -1)
    column = min(max(column,0), COLUMNS - 1) #EDGE CASE FOR KEEPING PIXEL INSIDE IMAGE BOUNDS

    return row, column

test_locations = [
    (0, 180),
    (0, 90),
    (0, 270),
    (30, 180),
    (-30, 180),
]

for latitude,longitude in test_locations:
    row, column = latlon_to_pixel(latitude,longitude)
    print(
        f"lat = {latitude}°, lon = {longitude}°"
        f"\n → row={row}, column = {column}"
    )

for r, c in [(0, 0), (2880, 5760), (5759, 11519), (1234, 4321)]:
    lat, lon = pixel_to_latlon(r, c, pixel_center=False)
    assert latlon_to_pixel(lat, lon) == (r, c), (r, c)    

test_pixels = [(0, 0), (2880, 5760), (5759, 11519), (1234, 4321)]

for r, c in test_pixels:
    # 1. Forward transformation: Pixel -> Lat/Lon
    lat, lon = pixel_to_latlon(r, c, pixel_center=False)
    
    # 2. Reverse transformation: Lat/Lon -> Pixel
    r_calc, c_calc = latlon_to_pixel(lat, lon)
    
    # 3. Compare original with round-trip output
    match = (r, c) == (r_calc, c_calc)
    print(f"Original: ({r}, {c}) -> Lat/Lon: ({lat:.4f}°, {lon:.4f}°) -> Reverted: ({r_calc}, {c_calc}) | Match: {match}")    


