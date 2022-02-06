# -*- coding: utf-8 -*-
"""
action: 允许使用4种返回值：

情况一：没有返回

情况二：bool类型

情况三：tuple类型 bool,message

情况四：tuple类型 bool,message,data 注:data必须是字典类型

"""


def main(**kwargs):
    data = {}
    return True, "ok", data
