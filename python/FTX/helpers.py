from time import time as _time

def get_current_timestamp():
    return int(round(_time() * 1000))