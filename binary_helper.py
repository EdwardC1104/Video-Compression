def numpy_to_bytearray(array):
    return array.tobytes()


def bytes_to_int(bytes_to_convert):
    return int.from_bytes(bytes_to_convert, "little", signed=False)
