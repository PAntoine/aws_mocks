#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : s3_bucket
# Desc  : This is the s3 bucket.
#
# Author: Peter Antoine
# Date  : 29/10/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import os
import json
from datetime import datetime
from typing import Optional, Dict

from .s3_object import S3Object

class S3Bucket:
    def __init__(self, name:str):
        self.name : str = name
        self.count : int = 1
        self.path_name : str = os.path.join("s3_buckets", name)
        
        self.objects : Dict[ str, {} ] = {}

        if os.path.isfile(self.path_name):
            self.load()
            self.exists = True
        else:
            self.exists = self.create()
    
    def create(self) -> bool:
        """ This function will create a new bucket if it does not already exist. """

        result = False

        if not os.path.isfile(self.path_name):
            # Ok, this bucket might not exist so lets create
            result = self.export()

        return result

    def load(self) -> bool:
        """ The loads the bucket """
        result = False

        try:
            infile = open(self.path_name)
            data = infile.read()
            infile.close()

            self.objects = json.loads(data)

            print(self.objects)

            result = True
        except:
            pass

        return result

    def export(self) -> bool:
        """ This exports the bucket list """
        result = False
        data = json.dumps(self.objects)
        outfile = None

        try:
            outfile = open(self.path_name,"w")
            outfile.write(data)
            outfile.close()

            result = True
        except:
            pass

        return result

    def getStatus(self) -> {}:
        """ This function will return the state of the bucket """
        return {'Last-Modified':    'Wed, 12 Oct 2009 17:50:00 GMT',
                'ETag':             "fba9dede5f27731c9771645a39863328"}

    def addObject(self, name:str, data:bytes, replace:bool=True) -> Optional[str]:
        """ This adds or replaces an object """
        result = None

        etag = hex(abs(hash(str(self.count) + ":" + self.name + ":" + name)))[2:]

        if replace or name not in self.objects:
            new_object = {}
            new_object['date'] = datetime.utcnow().strftime("%a, %d %b %Y %I:%M:%S GMT")
            new_object['etag'] = etag
            new_object['size'] = len(data)

            try:
                outfile = open(os.path.join("s3_buckets", etag), "w")
                outfile.write(str(data, "utf-8"))
                outfile.close()

                # TODO: might need to handle versions.
                self.objects[name] = new_object
                
                # write the updated bucket.
                if self.export():
                    result = etag
            except:
                pass

        return result

    def listObjects(self) -> {}:
        """ List all the objects from the bucket. """
        result = []

        for item in self.objects:
            obj = {}
            obj['name'] = item
            obj['etag'] = self.objects[item]['etag']
            obj['date'] = self.objects[item]['date']
            obj['size'] = self.objects[item]['size']

            obj['owner_id'] = "testing"
            obj['display_name'] = "test@example.co.uk"

            result.append(obj)

        return result

    def deleteObject(self, name:str) -> bool:
        """ remove the object from the bucket. """
        result = False

        if name in self.objects:
            del self.objects[name]

            if self.export():
                result = True

        return result

    def getObject(self, name:str) -> Optional[S3Object]:
        """ Get Object """
        result = None

        if name in self.objects:
            etag = self.objects[name]['etag']
            time = self.objects[name]['date']

            try:
                infile = open(os.path.join("s3_buckets", etag))
                data = infile.read()
                infile.close()

                result = S3Object(name, etag, time, data)
            except:
                pass

        return result
