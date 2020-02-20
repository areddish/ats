import os
import datetime

def get_data_folder(app_name):
    # Handle windows, macos, linux
    root_name = "HOME" if "HOME" in os.environ else "USERPROFILE"
    return os.path.join(os.environ[root_name], "."+app_name)

def get_user_file(app_name, file_name):
    return os.path.join(get_data_folder(app_name), file_name)


def is_weekday(dt):
    return dt.weekday() < 5


def is_before_open(dt):
    open_dt = datetime.datetime(
        dt.year, dt.month, dt.day, 9, 30, 0) + datetime.timedelta(seconds=DELTA_OFFSET)
    return dt < open_dt


def previous_end_of_day(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, 16, 0, 0) - datetime.timedelta(days=1) + datetime.timedelta(seconds=DELTA_OFFSET)


def skip_back_to_next_weekday(dt):
    while (not is_weekday(dt)):
        dt = dt - datetime.timedelta(days=1)
    return dt


def to_ib_timestr(dt):
    return dt.strftime("%Y%m%d %H:%M:%S")


def to_duration(dt_start, dt_end):
    return f"{(dt_end - dt_start).seconds} S"