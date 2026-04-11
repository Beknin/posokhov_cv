import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def count_lines(region):
    shape = region.image.shape
    image = region.image
    vlines = (np.sum(image, 0) / shape[0] == 1).sum()
    hlines = (np.sum(image, 1) / shape[1] == 1).sum()
    return vlines, hlines

def symmetry(region, Transpose = False):
    if Transpose:
        image = region.image.T
    else:
        image = region.image
    shape = image.shape
    top = image[:shape[0] // 2]
    if shape[0] % 2 != 0:
        bottom = image[shape[0] // 2 + 1:]
    else:
        bottom = image[shape[0] // 2:]
    bottom = bottom[::-1]
    result = bottom == top
    return result.sum() / result.size

def classificator(region):
    holes = count_holes(region)
    if holes == 2: #B, 8
        v, _ = count_lines(region)
        v /= region.image.shape[1]
        if v > 0.2 and symmetry(region, Transpose=True) < 0.8:
            return 'B'
        else:
            return '8'
    elif holes == 1: #A, 0
        if symmetry(region) > 0.6:
            return '0'
        else:
            return 'A'
    elif holes == 0: #1, W, X, *, -, /
        v, _ = count_lines(region)
        v /= region.image.shape[1]
        aspect = region.image.shape[0] / region.image.shape[1]
        if aspect > 1 :
            aspect = 1 / aspect

        if region.image.sum() == region.image.size:
            return '-'
        if symmetry(region) > 0.7 and v > 0.2:
            return '1'
        if symmetry(region, Transpose=True) > 0.8 and symmetry(region) < 0.5:
            return 'W'
        if symmetry(region, Transpose=True) > 0.8 and symmetry(region) > 0.8:
            return 'X'
        if aspect > 0.8:
            return '*'
        return '/'
    return '?'

image = imread('./alphabet.png')[:,:,:-1]
binary_alphabet = image.mean(2) > 0
labeled_alphabet = label(binary_alphabet)
aprops = regionprops(labeled_alphabet)
result = {}
save_path = Path(__file__).parent
image_path = save_path / "out_tree"
image_path.mkdir(exist_ok = True)
plt.ion()
plt.figure(figsize = (5, 7))
for region in aprops:
    symbol = classificator(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f"Class - '{symbol}'")
    plt.imshow(region.image)
    plt.savefig(image_path / f"image_{region.label}.png")
print(result)
plt.imshow(binary_alphabet)
plt.show()