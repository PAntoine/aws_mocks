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

class SAMPathDetails:
	__slots__ = ["event", "parameters", "methods"]

	def __init__(self, event:str, parameters:str, method:str):
		self.event = event
		self.parameters = parameters		# type List[str]
		self.methods = [method.upper()]	# type List[str]

	def addMethod(self, method:str):
		self.methods.append(method.upper())

	def getEvent(self) -> str:
		return self.event

	def getMethods(self) -> str:
		result = ''

		for method in self.methods:
			result += f"'{method}',"

		return result[:-1]

	def getParameters(self) -> str:
		result = ''

		for parameter in self.parameters:
			result += f"{parameter}, "

		return result[:-2]

	def getParameterPairs(self) -> str:
		result = ''

		for parameter in self.parameters:
			result += f"'{parameter}': {parameter}, "

		return result[:-2]


class SAMFunction:
	__slots__ = ["name", "directory", "entry_point", "runtime", "environment", "paths" ]

	def __init__(self, name:str):
		self.name = name
		self.directory = None	# type:str
		self.entry_point = None # type:str
		self.runtime = None		# type:str
		self.environment = {}	# type Dict[str, str]
		self.paths = {}			# type Dict[str, str]

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

	def addEvents(self, event:object):
		for item in event:
			print(item)
			if event[item]['Type'] in ['Api', 'HttpApi']:
				prop = event[item]['Properties']

				if 'Path' in prop:
					path_params = []

					amended = [x for x in prop['Path']]

					for i, c in enumerate(prop['Path']):
						if c == '{':
							start = i+1
							amended[i] = '<'
						elif c == '}':
							path_params.append(prop['Path'][start:i])
							amended[i] = '>'

					ap = ''.join(amended)

					if ap not in self.paths:
						self.paths[ap] = SAMPathDetails(item, path_params, prop['Method'])
					else:
						self.paths[ap].addMethod(prop['Method'])

	def isValid(self) -> bool:
		return self.name is not None and \
				self.directory is not None and \
				self.entry_point is not None and \
				self.runtime is not None

	def generateComposeService(self):
		result = []
		result.append("    " + self.name + ":\n")
		result.append("           build:\n")
		result.append("               context: apps/lambdas/" + self.name + "\n")
		result.append("           ports:\n")
		result.append("               - \"7000:8080\"\n")
		result.append("           networks:\n")
		result.append("               - comp_connect\n")

		if len(self.environment) > 0:
			result.append("           environment:\n")

			for item in self.environment:
				result.append("			   - " + item + "=\"" + self.environment[item] + "\"\n")

		return result

	def generatePathFunctions(self) -> list:
		result = []
		print(self.name)

		for path in self.paths:
			result.append(f"@app.route('{path}', methods=[{self.paths[path].getMethods()}])\n")
			result.append(f"def {self.paths[path].getEvent()}({self.paths[path].getParameters()}):\n")

			result.append("\treq_data = {\"httpMethod\": request.method}\n")
			result.append("\treq_data['queryStringParameters'] = request.args\n")
			result.append("\treq_data['body'] = request.data.decode('utf-8')\n")

			result.append(f"\treq_data['pathParameters'] = {{{self.paths[path].getParameterPairs()}}}\n")

			result.append(f"\tres = requests.post('http://{self.name}:8080/2015-03-31/functions/function/invocations', data=json.dumps(req_data))\n")
			result.append("\treturn Response(res.content, status=res.status_code)\n")
			result.append("\n")

		return result

	def generateDockerfile(self, path:str):
		result = ""

		self.generatePathFunctions()

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

			result += "ENV S3_TEST_ENDPOINT=\"http://flask:8080/buckets\"\n"
			result += "ENV DB_TEST_ENDPOINT=\"http://dynamodb-local:8000\"\n"
			result += "CMD [ \"" + self.entry_point + "\" ]\n"

		outfile = open(path, "w")
		outfile.write(result)
		outfile.close()

		return result

