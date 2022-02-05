import datetime
import time


def ping():
    """
    test ping
    :return: None
    """
    for i in range(3):
        print(i, "ok", datetime.datetime.now())
        time.sleep(1)
