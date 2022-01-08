import os


def write_bytearray_to_file(data, filepath):
    with open(filepath, "wb") as file:
        file.write(data)


def append_bytearray_to_file(data, filepath):
    with open(filepath, "ab") as file:
        file.write(data)


def get_filesize(filepath):
    return os.path.getsize(filepath)
