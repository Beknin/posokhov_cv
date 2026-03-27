import numpy as np
from scipy import ndimage
from scipy.signal import convolve2d
from matplotlib import pyplot as plt

image = np.load("stars.npy")

plus_kernel = np.array([[0,1,0],
                        [1,1,1],
                        [0,1,0]])
cross_kernel = np.array([[1,0,1],
                         [0,1,0],
                         [1,0,1]])

plus_match = convolve2d(image, plus_kernel, mode='same')
cross_match = convolve2d(image, cross_kernel, mode='same')

plus_centers = plus_match == 5
cross_centers = cross_match == 5

labeled_plus, plus_amount = ndimage.label(plus_centers)
labeled_cross, cross_amount = ndimage.label(cross_centers)

print(f"Всего {plus_amount + cross_amount} звёзд ({plus_amount} плюсиков и {cross_amount} крестиков)")