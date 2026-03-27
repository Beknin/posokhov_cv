import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage

images = [f"out/h_{i}.npy" for i in range(100)]
trajectories = {}
id = 0

def find_centers(image):
    labeled, objects = ndimage.label(image)
    mass_centers = []
    for i in range(1, objects + 1):
        obj = labeled == i
        center = ndimage.center_of_mass(obj)
        mass_centers.append(center)
    return mass_centers

img0 = np.load(images[0])

for center in find_centers(img0):
    trajectories[id] = [center]
    id += 1

for img in images[1:]:
    used = set()
    image = np.load(img)
    for y, x in find_centers(image):
        min_dist = 10**10
        min_dist_id = None
        for id, trajectory in trajectories.items():
            if id in used:
                continue
            prev_y, prev_x = trajectory[-1]
            dist = ((y - prev_y)**2 + (x - prev_x)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                min_dist_id = id
        trajectories[min_dist_id].append((y, x))
        used.add(min_dist_id)

plt.figure()
for id, coords in trajectories.items():
    x_coords = [i[1] for i in coords]
    y_coords = [i[0] for i in coords]
    plt.plot(x_coords, y_coords, marker='o', linewidth=2, markersize=4)
plt.axis('equal')
plt.show()