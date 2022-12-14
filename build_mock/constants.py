#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name    : constants
# Desc    : This file holds constants for the generators.
#
# Author: Peter Antoine
# Date    : 18/11/2021
#
#                      Copyright (c) 2021 Peter Antoine
#                             All rights Reserved.
#                     Released Under the Artistic Licence

DOCKER_COMPOSE_HEADER = [
		"version: '3.3'\n",
		"services:\n",
		"    dynamodb-local:\n",
		"        image: \"amazon/dynamodb-local:latest\"\n",
		"        command: \"-jar DynamoDBLocal.jar -sharedDb -dbPath /home/dynamodblocal/data/\"\n",
		"        container_name: dynamodb-local\n",
		"        ports:\n",
		"          - \"8000:8000\"\n",
		"        networks:\n",
		"          - comp_connect\n",
		"        volumes:\n",
		"          - ./data/dynamodb:/home/dynamodblocal/data:rw\n",
		"\n",
		"    mock_framework:\n",
		"        build:\n",
		"            context: apps/mock_framework\n",
		"        networks:\n",
		"            - my-network\n",
		"            - comp_connect\n",
		"        ports:\n",
		"            - \"6000:8080\"\n",
		"        volumes:\n",
		"            - ./data/buckets:/app/s3_buckets:rw\n\n" ]

DOCKER_COMPOSE_FOOTER = [
		"networks:\n",
		"    comp_connect:\n",
		"        driver: bridge\n",
		"        internal: true\n",
		"    my-network:\n",
		"        driver: bridge\n" ]

FLASK_FUNCTION_HEADER = [
		"#!/usr/bin/env python3\n",
		"#\n",
		"# Name  : flash app for mocking AWS API Ingress\n",
		"# Desc  : convert a standard request into a lambda call.\n",
		"#\n",
		"# Author: <aws_mock - auto-generated>\n",
		"\n",
		"import json\n",
		"import requests\n",
		"from flask import Flask, request, Response\n",
		"from s3_mock.s3_mock import s3_urls\n",
		"\n",
		"app = Flask(__name__)\n",
		"\n",
		"# register routes from s3\n",
		"app.register_blueprint(s3_urls)\n",
		"\n",
		"\n" ]

FLASK_FUNCTION_FOOTER = [
		"\n",
		"\n",
		"if __name__ == '__main__':\n",
		"    app.run(host='0.0.0.0', port=8080)\n",
		"\n" ]
