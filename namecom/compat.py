#!/usr/bin/env python
# coding: utf-8
"""
    compat.py
    ~~~~~~~~~~

"""
import sys


_ver = sys.version_info
is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)


if is_py2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin
