# -*- coding: utf-8 -*-

def connect_short(key):
    if key == "good":
        return "this is connect short by good"
    else:
        raise ValueError("the key is not exists")
