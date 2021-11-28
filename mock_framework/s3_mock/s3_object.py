#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : S3Object
# Desc  : The pseudo S3 Object.
#
# Author: Peter Antoine
# Date  : 29/10/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

class S3Object:
    __slots__ = ("name", "etag", "date", "data")

    def __init__(self, name:str , etag:str , date:str , data:bytes):
        self.name = name
        self.etag = etag
        self.date = date
        self.data = data
