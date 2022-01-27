# Video Compression Project

## Completed:
- Encode algorithm written
  - Split each frame into blocks
  - Compare each block
  - Either writes a flag to tell the decode that the block is identical or it writes the data
- Binary file contains metadata about the image
- Decode partially written
  - Replaces the missing data (visualised as white blocks for demonstration)
  - Rearranges the data back from block based into a 2D array
  - Displays a single frame
- Block size is dynamically determined based on the video resolution
- Metadata does not contain the number of frames so it could be used for streaming?

## Next Steps:
- Write back to a video file
- Run length encode ontop to increase lossless compression even more
- Optimise the decode algorithm
  - It is O(n2) and it doesn’t need to be
- Find a way to put the uint8 values into the numpy array without the expensive byte to decimal conversion

## New Knowledge:
- Use of numpy arrays
- Writing to binary files
- Reading binary byte by byte
- Using OpenCV to work with images and videos
