# -*- coding: utf-8 -*-
"""
demo use test method
"""
from com.utils import ping
import logging


def main(**kwargs):
    """
    run test method
    :param kwargs: is dict type
    :return: <bool> , <message>
    """
    logging.warning("ok")
    logging.info("test")
    print("**kwargs")
    print(kwargs["id"])
    print("test module is running...")
    print(ping())
    return True, "ok"


if __name__ == '__main__':
    params = {"id": 8, "name": 10}
    main(**params)
