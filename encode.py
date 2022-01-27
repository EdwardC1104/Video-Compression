import numpy as np
import video_helper
import image_helper
import file_helper
import binary_helper


def encode(video, filepath):

    # Read black and white frame
    video_helper.set_frame(video, 59.5*60)
    success, frame = video_helper.get_next_frame(video)
    frame = image_helper.convert_BGR_to_GRAY(frame)

    # Generate and write metadata
    metadata = image_helper.create_metadata_array(frame)
    metadata_bytes = binary_helper.numpy_to_bytearray(metadata)
    file_helper.write_bytearray_to_file(metadata_bytes, "./encoded")

    uncompressed_frame_size = image_helper.get_image_size(frame)
    print("Single uncompressed frame size:", uncompressed_frame_size)

    # Replace every 0 with a 1 so that it can be used to indicate 'no change in luminosity'
    frame = image_helper.replace_value(frame, 0, 1)

    # Split the image into blocks that can be compared
    frame_in_blocks = image_helper.split_into_blocks(frame)

    # Converts numpy array to python bytes and write it to a file
    frame_bytes = binary_helper.numpy_to_bytearray(
        frame_in_blocks.flatten())
    file_helper.append_bytearray_to_file(frame_bytes, "./encoded")

    ###############################################

    # Get frame dimensions
    width, height = image_helper.get_dimensions(frame)

    # Calculate block size
    size_horizontal, size_vertical = image_helper.calculate_block_size(width, height)
    block_size = size_horizontal * size_vertical

    # Debug count frames
    completed_frames = 0

    # Load next frame
    success, frame = video_helper.get_next_frame(video)
    while success:

        # Set the current frame as the previous frame
        last_frame_in_blocks = frame_in_blocks

        # success, frame = video_helper.get_next_frame(video)
        frame = image_helper.convert_BGR_to_GRAY(frame)

        # Replace every 0 with a 1 so that it can be used to indicate 'no change in luminosity'
        frame = image_helper.replace_value(frame, 0, 1)

        # Split the image into blocks that can be compared
        frame_in_blocks = image_helper.split_into_blocks(
            frame)

        # Array will be populated with the encoded data
        encoded_frame = image_helper.template_image(width, height)

        # Cheeck if each block is different in the previous frame
        # A 00000000 byte indicates an identical block
        pointer = 0
        for i in range(len(frame_in_blocks)):
            if np.array_equal(last_frame_in_blocks[i], frame_in_blocks[i]):
                pointer += 1
            else:
                end = pointer + block_size
                encoded_frame[pointer:end] = frame_in_blocks[i].flat[:]
                pointer += block_size

        # Trim the encoded array to the correct length
        encoded_frame = encoded_frame[:pointer]

        # Converts numpy array to python bytes and write it to a file
        frame_bytes = binary_helper.numpy_to_bytearray(encoded_frame)
        file_helper.append_bytearray_to_file(frame_bytes, filepath)

        # Load next frame
        success, frame = video_helper.get_next_frame(video)

        # Debug
        completed_frames += 1

    print("Number of frames encoded:", completed_frames)
    print("Theoretical uncompressed video file size:", completed_frames * uncompressed_frame_size)
