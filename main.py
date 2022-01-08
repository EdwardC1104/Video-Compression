import cv2
import numpy as np
from math import gcd
import video_helper
import image_helper
import file_helper
import binary_helper
import timer
from encode import encode


timer.start()

# Load video
video = video_helper.load_video("videos/original.mp4")

encode(video, "./encoded")

timer.end("Encode time:")


print("Encoded video file size from os:",
      file_helper.get_filesize('./encoded'))


timer.start()

# Open file
file = open("encoded", "rb")


# Read metadata from file
frame_width, frame_height = image_helper.read_metadata(file)


# Create numpy array for the frame to fill
new_frame = np.zeros((frame_width * frame_height), dtype=np.uint8)
new_frame_two = np.zeros((frame_width * frame_height), dtype=np.uint8)

byte = file.read(1)
counter = 0
while counter < (frame_width * frame_height * 2) and byte:
    luminosity = binary_helper.bytes_to_int(byte)
    if counter < (frame_width * frame_height):
        new_frame[counter] = luminosity
    else:
        new_frame_two[counter - (frame_width * frame_height)] = luminosity
    counter += 1
    byte = file.read(1)

file.close()

print("Decoded video file size:", image_helper.get_image_size(
    new_frame) + image_helper.get_image_size(new_frame_two))

number_of_blocks = gcd(frame_width, frame_height)
block_size_horizontal = frame_width // number_of_blocks
block_size_vertical = frame_height // number_of_blocks

decoded_frame = np.zeros((frame_width * frame_height), dtype=np.uint8)

pointer = 0
for pixel in new_frame_two:
    if pointer >= (frame_width * frame_height):
        break
    if pixel == 0:
        decoded_frame[pointer:pointer +
                      144] = np.full(144, fill_value=255, dtype=np.uint8)[:]
        pointer += 144
    else:
        decoded_frame[pointer] = pixel
        pointer += 1

decoded_frame = decoded_frame.reshape(
    (decoded_frame.shape[0] // block_size_vertical // block_size_horizontal, block_size_horizontal, block_size_vertical))

decoded_frame = image_helper.combine_blocks_into_image(
    decoded_frame, frame_width, frame_height)

print(image_helper.get_image_size(
    decoded_frame))


timer.end("Decode time:")

image_helper.display_image(decoded_frame)
original_frame = image_helper.convert_BGR_to_GRAY(
    video_helper.get_frame(video, 60))

print(cv2.PSNR(decoded_frame, original_frame))
