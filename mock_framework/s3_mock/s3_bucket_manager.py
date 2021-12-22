#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : s3_bucket_manager
# Desc  : This function will manage the buckets that have been created.
#         It's not doing anything clever just holding a list of buckets and
#         the files that are in the buckets.
#
# Author:
# Date  : 29/10/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import os
import json
from typing import Optional, Dict
from .s3_bucket import S3Bucket

class S3BucketManager:
    __slots__ = ('buckets')

    def start(self):
        """ start the bucker manager.

            This function will load the bucket list and all the buckets to go with them.
        """
        self.buckets : Dict[str, S3Bucket] = {}
        self.load()

    def addBucket(self, bucket_name:str) -> bool:
        result = False

        if bucket_name not in self.buckets:
            new_bucket = S3Bucket(bucket_name)

            self.buckets[bucket_name] = new_bucket
            self.export()

            result = True

        return result

    def getBucket(self, bucket:str) -> Optional[S3Bucket]:
        """ Return the bucket if it exists. """

        if bucket in self.buckets:
            return self.buckets[bucket]
        else:
            return None

    def load(self) -> bool:
        """ The loads the bucket """
        result = False

        try:
            infile = open(os.path.join("s3_buckets", "bucket_list"))
            data = infile.read()
            infile.close()

            for bucket in json.loads(data):
                self.buckets[bucket] = S3Bucket(bucket)

            result = True
        except:
            pass

        return result

    def export(self) -> bool:
        """ This exports the bucket list """
        result = False
        data = json.dumps(list(self.buckets.keys()))
        outfile = None

        try:
            outfile = open(os.path.join("s3_buckets", "bucket_list") ,"w")
            outfile.write(data)
            outfile.close()

            result = True
        except:
            pass

        return result
