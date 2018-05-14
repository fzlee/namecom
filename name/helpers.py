#!/usr/bin/env python
# coding: utf-8
"""
    helpers.py
    ~~~~~~~~~~

"""
import time
import functools

from requests.exceptions import Timeout, ChunkedEncodingError


def request_error_retry(repeat=3, sleep=0):

    def wrapper(old_func):
        @functools.wraps(old_func)
        def new_func(*args, **kwargs):
            # 尝试多次， 最后一次抛出异常
            for i in range(repeat):
                try:
                    return old_func(*args, **kwargs)
                except (ChunkedEncodingError, Timeout) as e:
                    if i == repeat - 1:
                        raise e
                    else:
                        if sleep > 0:
                            time.sleep(sleep)
                        continue
        return new_func
    return wrapper
