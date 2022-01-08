import time


start_time = 0


def start():
    global start_time
    start_time = time.time()


def end(text=""):
    global start_time
    end_time = time.time()
    print(text, round(end_time - start_time, 4), "s")
