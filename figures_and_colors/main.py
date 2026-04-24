import numpy as np
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2hsv

image = imread("balls_and_rects.png")
hsv = rgb2hsv(image)
h = hsv[:, :, 0]
circs = []
rects = []

for color in np.unique(h):
    if color != 0:
        binary = color == h
        labeled = label(binary)
        props = regionprops(labeled)
        for obj in props:
            if obj.image.size == obj.image.sum():
                rects.append(color)
            else:
                circs.append(color)

delta = 0.05
group_c = [[circs[1]]]
group_r = [[rects[1]]]

for i in range(1, len(circs)):
    if abs(circs[i - 1] - circs[i]) < delta:
        group_c[-1].append(circs[i]) 
    else:
        group_c.append([circs[i]])

for i in range(1, len(rects)):
    if abs(rects[i - 1] - rects[i]) < delta:
        group_r[-1].append(rects[i]) 
    else:
        group_r.append([rects[i]])

print(f"Total shapes: {len(circs) + len(rects)}")

print(f"Circles ({len(circs)}):")
for g in group_c:
    print(np.mean(g), len(g))

print(f"Rectangles ({len(rects)}):")
for g in group_r:
    print(np.mean(g), len(g))