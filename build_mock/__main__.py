#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name	: __main__
# Desc	: Main file required.
#
# Author:
# Date	: 21/11/2021
#
#					  Copyright (c) 2021 Peter Antoine
#							 All rights Reserved.
#					 Released Under the Artistic Licence
import os
import sys
import shutil
from .ingest_yaml import IngestSAMYAML

if __name__ == '__main__':
	# This is the main function to import the SAM file
	index = 1
	failed = False
	output = None
	clear = False
	sam_dir = None

	while index < len(sys.argv):
		if sys.argv[index][0:2] == "-o":
			if len(sys.argv[index]) == 2 and index+1 < len(sys.argv):
				output = sys.argv[index + 1]
				index += 1
			else:
				output = sys.argv[index][2:]
		elif sys.argv[index][0:2] == "-s":
			if len(sys.argv[index]) == 2 and index+1 < len(sys.argv):
				sam_dir = sys.argv[index + 1]
				index += 1
			else:
				sam_dir = sys.argv[index][2:]
		elif sys.argv[index][0:2] == "-c":
				clear = True
		else:
			if sys.argv[index][0] == '-':
				if len(sys.argv[index]) == 2:
					print("Invalid Parameter: {}".format(sys.argv[index]))
					index += 1
				else:
					print("Invalid Parameter: {}".format(sys.argv[index][0:2]))
			else:
				print("Invalid Parameter: {}".format(sys.argv[index]))

			failed = True

		index += 1

	if output is not None and sam_dir is not None and not failed:
		if not clear and os.path.exists(output):
			print("Failed: path {} already exists and overwrite is not set..".format(output))
		else:
			if clear and os.path.exists(output):
				if os.path.isfile(output):
					os.remove(output)
				else:
					shutil.rmtree(output)

			sam_file = os.path.join(sam_dir, "template.yaml")
			ingester = IngestSAMYAML(sam_file)

			if ingester.isValid():
				# we have a valid SAM file converted - lets produce the output.
				os.mkdir(output)
				os.mkdir(os.path.join(output, "data"))
				os.mkdir(os.path.join(output, "data", "buckets"))
				os.mkdir(os.path.join(output, "data", "dynamodb"))
				os.mkdir(os.path.join(output, "apps"))
				os.mkdir(os.path.join(output, "apps", "lambdas"))

				# write the docker compose file
				ingester.generateDockerCompose(os.path.join(output))

				# generate functions
				ingester.outputFunctions(os.path.join(output, "apps", "lambdas"))
				ingester.copyFunctions(sam_dir, os.path.join(output, "apps", "lambdas"))

				# copy flask application - that includes the s3 mock.
				shutil.copytree("mock_framework", os.path.join(output, "apps", "mock_framework"))
	else:
		print("Usage: build_mock -o <out_dir> -s <sam_input_file>")

