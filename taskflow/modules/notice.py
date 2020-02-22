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
    logging.info("notice start")
    logging.warning("ok")
    logging.info("test")
    instance = kwargs["sys_taskflow_instance"]
    flow_name = instance["title"]
    flow_description = instance["description"]
    creator = instance["creator"]
    # sample module task
    ping()
    logging.info("hi, %s, 你的流程:%s-%s ,已经顺利完成", creator, flow_name, flow_description)
    logging.info("notice end")

# test main
def test_main(**kwargs):
    """
    用于测试的main 函数
    :param kwargs:
    :return:
    """
    instance = kwargs["sys_taskflow_instance"]
    # set demo
    instance["title"] = "hello"
    instance["description"] = "test"
    instance["creator"] = "jiangxf"
    #####################################
    logging.warning("ok")
    logging.info("test")

    flow_name = instance["title"]
    flow_description = instance["description"]
    creator = instance["creator"]
    # sample module task
    ping()
    logging.info("hi, %s, 你的流程:%s-%s ,已经顺利完成", creator, flow_name, flow_description)
