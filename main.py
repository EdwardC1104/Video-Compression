import numpy as np
import video_helper
import image_helper
import file_helper
import binary_helper


# Load video
my_video = video_helper.load_video("videos/bbb_sunflower_short.mp4")


# Read black and white frame
video_helper.set_frame(my_video, 1000)
success, my_frame = video_helper.get_next_frame(my_video)
my_frame = image_helper.convert_BGR_to_GRAY(my_frame)


# Generate and write metadata
metadata = image_helper.create_metadata_array(my_frame)
metadata_bytes = binary_helper.numpy_to_bytearray(metadata)
file_helper.write_bytearray_to_file(metadata_bytes, "./encoded")


# Flatten array
my_frame_flat = my_frame.flatten()
print("Uncompressed image size:", image_helper.get_image_size(my_frame))


# Replace every 0 with a 1 so that it can be used to indicate 'no change in luminosity'
image_helper.replace_value_with_indexing(my_frame_flat, 0, 1)


# Converts numpy array to python bytes and write it to a file
my_frame_bytes = binary_helper.numpy_to_bytearray(my_frame_flat)
file_helper.append_bytearray_to_file(my_frame_bytes, "./encoded")
print("Encoded image file size from os:", file_helper.get_filesize('./encoded'))


# Open file
file = open("encoded", "rb")


# Read metadata from file
frame_width, frame_height = image_helper.read_metadata(file)


# Create numpy array for the frame to fill
new_frame = np.zeros((frame_width * frame_height), dtype=np.uint8)

byte = file.read(1)
counter = 0
while byte:
    luminosity = binary_helper.bytes_to_int(byte)
    new_frame[counter] = luminosity
    counter += 1
    byte = file.read(1)

print("Decoded image file size:", image_helper.get_image_size(new_frame))

file.close()