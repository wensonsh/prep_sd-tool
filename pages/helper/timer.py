import datetime

def get_current_time():
    """
    Get the current time in a string format
    :return: current time with hour, minute, second and microsecond
    """
    return datetime.datetime.now().strftime("%H:%M:%S:%f")
