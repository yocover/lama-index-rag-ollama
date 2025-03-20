import time


def get_timestamp_millis():
    timestamp = time.time()
    timestamp = int(round(timestamp * 1000))
    return timestamp


def get_duration_millis(start_time, end_time):
    timestamp = int(round((end_time - start_time) * 1000))
    return timestamp
