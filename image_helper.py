import cv2
import numpy as np
import binary_helper

def convert_BGR_to_GRAY(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def replace_value_with_indexing(flat_image, replace_every, replace_with):
  foo2 = flat_image[:]
  foo2[foo2 == replace_every] = replace_with

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