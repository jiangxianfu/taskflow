# -*- coding: utf-8 -*-
"""
demo use test method
"""
from com.utils import ping
import logging


def main(**kwargs):
    """
    获取系统及配置 安装 操作系统 返回 ip port user password
    :param kwargs: is dict type
    :return: <bool> , <message> ,(ip port user password)
    """
    logging.info("start init os config")
    print("kwargs", kwargs)
    print(kwargs["ip"])
    print(kwargs["port"])
    print(kwargs["user"])
    print(kwargs["password"])
    print("ssh server")
    ping()
    print("config data")
    print("install monitor script")
    print("change root password to random")
    logging.info("end init os config")
    return True


def test_main(**kwargs):
    kwargs["ip"] = "127.0.0.1"
    kwargs["port"] = 22
    kwargs["user"] = "root"
    kwargs["password"] = "12345678"

    ########################################
    print("kwargs", kwargs)
    print(kwargs["ip"])
    print(kwargs["port"])
    print(kwargs["user"])
    print(kwargs["password"])
    print("ssh server")
    ping()
    print("config data")
    print("install monitor script")
    print("change root password to random")
    return True
