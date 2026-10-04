import numpy as np
mars_elevation = np.array([
    [120, 135, 141, 130],
    [118, 129, 150, 143],
    [110, 125, 147, 155]
])

heighest = np.max(mars_elevation)
lowest = np.min(mars_elevation)
average = np.mean(mars_elevation)
print("Mars Elevation Grid")
print(mars_elevation)
print("Heighest: ",heighest)
print("Lowest: ",lowest)
print("Average: ",average)
print("Difference: ",heighest - lowest)
