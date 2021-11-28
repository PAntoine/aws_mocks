#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : s3_utils
# Desc  : Utilities for the s3_mock.
#
# Author: Peter Antoine
# Date  : 31/10/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import base64
import hashlib

def makeLongHash(in_str:str) -> str:
    h = hashlib.sha256()
    h.update(bytes(in_str, "utf-8"))

    return base64.b64encode(bytes(h.hexdigest()[:48], "utf-8"))

def makeShortHash(in_str:str) -> str:
    h = hashlib.sha256()
    h.update(bytes(in_str, "utf-8"))

    return h.hexdigest()[:32]
