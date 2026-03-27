import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage.morphology import opening

images = [f"wire_images/wires{i}.npy" for i in range(1, 7)]
struct = np.ones((3, 1))

for n, i in enumerate(images):
    img = np.load(i)
    cut_wires = opening(ndimage.label(img)[0], struct)
    print(f"Изображение №{n+1}:")
    for j in range(1, ndimage.label(img)[1] + 1):
        cut_wire = cut_wires == j
        part_amt = ndimage.label(cut_wire)[1]
        print(f"Провод №{j} порвался на {part_amt} частей")