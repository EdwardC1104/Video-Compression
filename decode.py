
import cv2
import numpy as np
from math import gcd
import image_helper
import binary_helper


def decode(filepath):
    # Open file
    file = open(filepath, "rb")

    # Read metadata from file
    frame_width, frame_height = image_helper.read_metadata(file)

    # Create numpy array for the frame to fill
    new_frame = np.zeros((frame_width * frame_height), dtype=np.uint8)

    # Calculate block size
    block_size_horizontal, block_size_vertical = image_helper.calculate_block_size(
        frame_width, frame_height)

    # Reads 1 byte
    byte = file.read(1)

    # Counts decoded frames for debug
    completed_frames = 0

    # Number of luminosity values read - resets on each new frame
    counter = 0

    # Location in new_frame array
    new_frame_pointer = 0

    # Breaks at the end of the file
    while byte:

        # A whole frame has been read - DECODE THIS FRAME
        if new_frame_pointer == (frame_width * frame_height):
            print("Starting decode...")

            # Reset the counter as its a new frame
            counter = 0
            new_frame_pointer = 0

            # Array is populated by the decode frame
            decoded_frame = image_helper.template_image(
                frame_width, frame_height)

            # Either add the pixel to the frame or the block from the previous frame
            pointer = 0
            for pixel in new_frame:
                if pointer >= (frame_width * frame_height):
                    break
                if pixel == 0:
                    decoded_frame[pointer:pointer +
                                  144] = np.full(144, fill_value=255, dtype=np.uint8)[:]
                    pointer += 144
                else:
                    decoded_frame[pointer] = pixel
                    pointer += 1

            # Reshapes a flattened block array into a 3D array of blocks
            decoded_frame = decoded_frame.reshape(
                (decoded_frame.shape[0] // block_size_vertical // block_size_horizontal, block_size_horizontal, block_size_vertical))

            # Combines the 3D array of blocks into a 2D normal frame
            decoded_frame = image_helper.combine_blocks_into_image(
                decoded_frame, frame_width, frame_height)

            # Debug count frames
            completed_frames += 1
            print("Number of frames completed:", completed_frames,
                  "(Exit the opened window to continue decode)")

            # Show image window - DEBUG
            image_helper.display_image(decoded_frame)

        # Convert binary value to decimal and add it to the array
        luminosity = binary_helper.bytes_to_int(byte)
        new_frame[counter] = luminosity

        # Increase by block size
        if luminosity == 0:
            new_frame_pointer += 144
        else:
            new_frame_pointer += 1

        # Read next byte
        counter += 1
        byte = file.read(1)

    file.close()
