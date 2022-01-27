import cv2
import numpy as np
from math import gcd
import binary_helper
import os
os.environ['MPLCONFIGDIR'] = os.getcwd() + '/configs/'
import matplotlib.pyplot as plt


def convert_BGR_to_GRAY(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def replace_value_with_indexing(array, replace_every, replace_with):
    foo2 = array[:]
    foo2[foo2 == replace_every] = replace_with


def replace_value(array, replace_every, replace_with):
    new_array = array.flatten()
    foo2 = new_array[:]
    foo2[foo2 == replace_every] = replace_with
    return new_array.reshape(array.shape)


def write_to_file(image, filename):
    cv2.imwrite(filename, image)


def create_metadata_array(image):
    return np.array([image.shape[0], image.shape[1]], dtype=np.uint16)


def read_metadata(file):
    byte = file.read(2)
    width = binary_helper.bytes_to_int(byte)
    byte = file.read(2)
    height = binary_helper.bytes_to_int(byte)
    return width, height


def get_image_size(image):
    return image.nbytes


def split_into_blocks(arr):
    h, w = arr.shape
    nrows, ncols = calculate_block_size(h, w)
    assert h % nrows == 0, f"{h} rows is not evenly divisible by {nrows}"
    assert w % ncols == 0, f"{w} cols is not evenly divisible by {ncols}"
    return (arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1, 2).reshape(-1, nrows, ncols))


def combine_blocks_into_image(arr, h, w):
    n, nrows, ncols = arr.shape
    return (arr.reshape(h//nrows, -1, nrows, ncols).swapaxes(1, 2).reshape(h, w))


def display_image(image):
    plt.axis("off")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def get_dimensions(image):
    return image.shape


def calculate_block_size(width, height):
    # width, height = get_dimensions(image)
    number_of_blocks = gcd(width, height)
    block_size_horizontal = width // number_of_blocks
    block_size_vertical = height // number_of_blocks
    return block_size_horizontal, block_size_vertical


def template_image(width, height):
    return np.zeros((width * height), dtype=np.uint8)
