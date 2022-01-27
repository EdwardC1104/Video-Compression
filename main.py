
import video_helper
import file_helper
import timer
from encode import encode
from decode import decode


timer.start()

# Load video
video = video_helper.load_video("videos/original.mp4")

encode(video, "./encoded")

timer.end("Encode time:")


print("Encoded video file size from os:",
      file_helper.get_filesize('./encoded'))


timer.start()

decode("./encoded")

timer.end("Decode time:")