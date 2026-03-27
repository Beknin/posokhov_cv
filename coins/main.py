import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage

image = np.load("coins.npy")
coins = []
sizes = set()
nominals = [1, 2, 5, 10]
total = 0

labeled, amount = ndimage.label(image)
for i in range(1, amount + 1):
    coins.append(labeled == i)
    sizes.add(np.ndarray.sum(coins[-1]))

sizes = {sorted(sizes)[i]: nominals[i] for i in range(len(sizes))}

for coin in coins:
    total += sizes[np.ndarray.sum(coin)]

print(f"Сумма монет: {total}")