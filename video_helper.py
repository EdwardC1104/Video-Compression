import cv2


def load_video(path):
    video = cv2.VideoCapture(path)
    return video


def get_next_frame(video):
    return video.read()


def get_frame(video, frameNumber):
    video.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
    success, frame = get_next_frame(video)
    if success:
        return frame
    raise Exception('Failed to return the requested frame.')


def set_frame(video, frameNumber):
    video.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
