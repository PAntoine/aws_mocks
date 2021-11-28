#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name	: sam_function
# Desc	: The structure to hold SAM functions.
#
# Author: Peter Antoine
# Date	: 06/11/2021
#
#					  Copyright (c) 2021 Peter Antoine
#							 All rights Reserved.
#					 Released Under the Artistic Licence

class SAMFunction:
	__slots__ = ["name", "directory", "entry_point", "runtime", "environment" ]

	def __init__(self, name:str):
		self.name = name
		self.directory = None	# type:str
		self.entry_point = None # type:str
		self.runtime = None		# type:str
		self.environment = {}	# type Dict[str, str]

	def addDirectory(self, name:str):
		# TODO - check that this is valid first.
		self.directory = name

	def addEntryPoint(self, name:str):
		if name is not None and '.' in name:
			self.entry_point = name
		else:
			print("Error: name needs to have a '.' in it, to separate the module (file) from the function.")

	def addRuntime(self, name:str):
		if name[0:6] == 'python':
			self.runtime = 'python:' + name[6:]
		else:
			self.runtime = name

	def addEnvironmentVariable(self, name:str, value:str):
		self.environment[name] = value

	def isValid(self) -> bool:
		return self.name is not None and \
				self.directory is not None and \
				self.entry_point is not None and \
				self.runtime is not None

	def generateComposeService(self):
		result = []
		result.append("    " + self.name + ":\n")
		result.append("		   build:\n")
		result.append("			   context: apps/lambdas/" + self.name + "\n")
		result.append("		   ports:\n")
		result.append("			   - \"7000:8080\"\n")
		result.append("		   networks:\n")
		result.append("			   - comp_connect\n")

		if len(self.environment) > 0:
			result.append("		   environment:\n")

			for item in self.environment:
				result.append("			   - " + item + "=\"" + self.environment[item] + "\"\n")

		return result

	def generateDockerfile(self, path:str):
		result = ""

		DOCKER_TEMPLATE =	"FROM public.ecr.aws/lambda/{0}\n" \
							"COPY {1}.py ${{LAMBDA_TASK_ROOT}}\n" \
							"ENV AWS_DEFAULT_REGION=\"eu-west-2\"\n" \
							"ENV AWS_ACCESS_KEY_ID=\"fdfd\"\n" \
							"ENV AWS_SECRET_ACCESS_KEY=\"fdfddf\"\n" \
							"ENV AWS_SESSION_TOKEN=\"dfdfdfdfdfdfdfd\"\n"

		pos = self.entry_point.find(".")

		if pos != -1 and pos != 0:
			root = self.entry_point[0:pos]
			result = DOCKER_TEMPLATE.format(self.runtime, root)

			for item in self.environment:
				result += "ENV " + item + "=\"" + self.environment[item] + "\"\n"

			result += "ENV S3_TEST_ENDPOINT=\"http://flask:8080\"\n"
			result += "ENV DB_TEST_ENDPOINT=\"http://dynamodb-local:8000\"\n"
			result += "CMD [ \"" + self.entry_point + "\" ]\n"

		outfile = open(path, "w")
		outfile.write(result)
		outfile.close()

		return result

