# -*- coding: utf-8 -*-
"""
demo use test method
"""
from modules.libs.config import connect_short
import logging


def main(**kwargs):
    """
    run test method
    :param kwargs: is dict type
    :return: <bool> , <message>
    """
    logging.info("demo start")
    logging.warning("ok")
    logging.info("test")
    print("**kwargs")
    print(kwargs["id"])
    print("test module is running...")
    print(connect_short("good"))
    logging.info("demo end")
    return True, "ok"


def test_main(**kwargs):
    """
    仅仅用于测试的方式运行
    :param kwargs:
    :return:
    """
    kwargs["id"] = 8
    print("kwargs data:", kwargs)
    logging.warning("ok")
    logging.info("test")
    print("**kwargs")
    print(kwargs["id"])
    print("test module is running...")
    print(connect_short("good"))
    return True, "ok"
