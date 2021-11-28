#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : setup.py
# Desc  : flask build
#
# Author: 
# Date  : 19/10/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import os
#import version as version
from setuptools import setup, find_packages

__author__      = "Peter Antoine"
__copyright__   = "Copyright 2021, Peter Antoine"
__credits__     = ["Peter Antoine"]
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Peter Antoine"
__email__       = "github@peterantoine.me.uk"
__url__         = "https://github.com/PAntoine/BeornLib"
__status__      = "Development"

setup(name='AWSLambdaInterface',
      version=__version__,
      description='AWS Lambda Interface',
      author=__author__,
      author_email=__email__,
      url=__url__,
      packages=find_packages(),
      install_requires=['flask']
     )
