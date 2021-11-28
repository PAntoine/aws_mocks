#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : sam_bucket
# Desc  : The sam bucket structure.
#
# Author: Peter Antoine
# Date  : 06/11/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

class SAMBucket:
	__slots__ = ["name", "bucket_name"]

	def __init__(self, name:str):
		self.name = name		# type : str
		self.bucket_name = None	# type : str

	def addBucketName(self, name:str) -> bool:
		self.bucket_name = name

		return True

	def isValid(self) -> bool:
		result = self.bucket_name is not None

		return result
