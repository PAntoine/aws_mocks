#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : YAMLConstructor
# Desc  : This is a custom constructor for SAM YAML imports.
#
# Author: Peter Antoine
# Date  : 07/11/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import yaml

class Sub(yaml.YAMLObject):
    yaml_tag = u'!Sub'

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "%s(name=%r)" % (self.__class__.__name__, self.name)

    @classmethod
    def from_yaml(cls, loader, node):
        return Sub(node.value)
