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
    logging.info("start install os")
    logging.warning("ok")
    logging.info("test")
    print("**kwargs")
    print("test module is running...")
    print(ping())
    print("kwargs", kwargs)
    print(kwargs["os"])
    print(kwargs["cpu_num"])
    print(kwargs["mem_gb"])
    print(kwargs["disk_gb"])
    ping()
    # get install os result
    ip = "127.0.0.1"
    port = 22
    user = "op"
    passwd = "test"
    ret_dict_data = {"ip": ip, "port": port, "user": user, "passwd": passwd}
    logging.info("end install os")
    return True, "ok", ret_dict_data


def test_main(**kwargs):
    kwargs["os"] = "centos 8.0"
    kwargs["cpu_num"] = 8
    kwargs["mem_gb"] = 24
    kwargs["disk_gb"] = 100
    print("kwargs", kwargs)
    print(kwargs["os"])
    print(kwargs["cpu_num"])
    print(kwargs["mem_gb"])
    print(kwargs["disk_gb"])
    ping()
    # get install os result
    ip = "127.0.0.1"
    port = 22
    user = "op"
    passwd = "test"
    ret_dict_data = {"ip": ip, "port": port, "user": user, "passwd": passwd}
    return True, "ok", ret_dict_data
