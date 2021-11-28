#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : inject_yaml
# Desc  : This function will ingest a SAM yaml file
#
# Author: Peter Antoine
# Date  : 06/11/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import os
import yaml
from .constants import *
from typing import Dict
from .sam_function import SAMFunction
from .sam_bucket import SAMBucket
from .sam_simple_table import SAMSimpleTable
from .YAMLConstructor import Sub

class IngestSAMYAML:
    __slots__ = ["functions", "buckets", "tables", "valid"]

    def __init__(self, sam_template_file:str):
        """ This function will ingest a sam YAML file and
            build a structure that holds the structure of the
            SAM instance that is to be built. """

        self.buckets:Dict[SamBuckets] = {}
        self.functions:Dict[SamFunction] = {}
        self.tables:Dict[SamSimpleTables] = {}

        yaml.SafeLoader.add_constructor('!Sub', Sub.from_yaml)
        yaml.SafeLoader.add_constructor('!GetAtt', Sub.from_yaml)


        failed = False

        with open('deploy.yaml', 'r') as file:
            configuration = yaml.safe_load(file)

        for item in configuration['Resources']:
            if configuration['Resources'][item]['Type'] == 'AWS::Serverless::Function':
                if not self.decodeFunction(item, configuration['Resources'][item]):
                    failed = True

            if configuration['Resources'][item]['Type'] == 'AWS::S3::Bucket':
                if not self.decodeBucket(item, configuration['Resources'][item]):
                    failed = True

            if configuration['Resources'][item]['Type'] == 'AWS::Serverless::SimpleTable':
                if not self.decodeSimpleTable(item, configuration['Resources'][item]):
                    failed = True

        # The SAM setup is valid if none of the required mocking fields fail.
        # This won't verify if the SAM YAML is valid for AWS - you can use the
        # normal tools for that, this is just so we can set up a mock to test the
        # lambda functions.
        self.valid = not failed

    def isValid(self):
        return self.valid

    def decodeFunction(self, name:str, function:Dict) -> bool:
        """ TODO: handle this -> Resource: 'arn:aws:s3:::<bucket_name>/*' """
        result = False
        new_function = SAMFunction(name)

        for prop in function['Properties']:
            if prop == 'CodeUri':
                new_function.addDirectory(function['Properties'][prop])

            if prop == 'Handler':
                new_function.addEntryPoint(function['Properties'][prop])

            if prop == 'Runtime':
                new_function.addRuntime(function['Properties'][prop])

            if prop == 'Policies':
                pass

            if prop == 'Events':
                pass

            if prop == 'Environment':
                self.decodeEnvironmentVariables(new_function, function['Properties'][prop])

        if new_function.isValid():
            self.functions[name] = new_function
            result = True
        else:
            printf("function failed")

        return result

    def decodeBucket(self, name:str, bucket:Dict) -> bool:
        result = False
        new_bucket = SAMBucket(name)

        for prop in bucket['Properties']:
            if prop == 'BucketName':
                new_bucket.addBucketName(bucket['Properties'][prop])

        if new_bucket.isValid():
            self.buckets[name] = new_bucket
            result = True

        return result

    def decodeSimpleTable(self, name:str, table:Dict) -> bool:
        result = False
        new_table = SAMSimpleTable(name)

        for prop in table['Properties']:
            if prop == 'TableName':
                new_table.addTableName(table['Properties'][prop])

            if prop == 'PrimaryKey':
                new_table.addPrimaryKey(table['Properties'][prop]['Name'], table['Properties'][prop]['Type'])

        #  Ignoring: Tags, ProvisionedThroughput and SSESpecification

        if new_table.isValid():
            self.tables[name] = new_table
            result = True

        return result

    def decodeEnvironmentVariables(self, function:object, env_var:Dict) -> bool:
        if 'Variables' in env_var:
            for item in env_var['Variables']:
                function.addEnvironmentVariable(item, env_var['Variables'][item])

    def generateDockerCompose(self, path:str) -> str:
        result = DOCKER_COMPOSE_HEADER

        for item in self.functions:
            result += self.functions[item].generateComposeService()

        result += DOCKER_COMPOSE_FOOTER

        with open(os.path.join(path, 'docker-compose.yml'), "w") as out_file:
            out_file.writelines(result)

    def outputFunctions(self, path:str):
        for item in self.functions:
            os.mkdir(os.path.join(path, self.functions[item].name))
            self.functions[item].generateDockerfile(os.path.join(path, self.functions[item].name, "Dockerfile"))
