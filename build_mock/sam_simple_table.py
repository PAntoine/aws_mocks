#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : sam_simple_table
# Desc  : The SAM simple table
#
# Author: Peter Antoine
# Date  : 07/11/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import random

class SAMSimpleTable:
    __slots__ = ["key", "table_name", "name", "key_type"]

    def __init__(self, name:str):
        self.name = name        # type : str
        self.key = None         # type : str
        self.key_type = None    # type : str

        # default name is a randomly generated.
        self.table_name = name + "_" + str(hash(random.getrandbits(32)))

    def addPrimaryKey(self, name:str, key_type: str) -> None:
        """ Add the primary key to the table object """
        self.key = name
        self.key_type = key_type

    def addTableName(self, name : str) -> None:
        """ Add the aws simple table name """
        self.table_name = name

    def isValid(self) -> bool:
        return self.table_name is not None and self.key is not None
