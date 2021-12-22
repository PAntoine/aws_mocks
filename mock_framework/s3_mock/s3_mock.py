#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name  : s3_mock
# Desc  : This function mock AWS S3 for local testing.
#
# Author: Peter Antoine
# Date  : 29/10/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import json
import hashlib
import datetime
import s3_mock.s3_utils
from flask import Flask, request, Response, Blueprint, current_app
from werkzeug.datastructures import Headers
from .s3_bucket_manager import S3BucketManager

s3_urls = Blueprint('s3_urls', __name__,)

# Load and start the bucket manager.
bucket_manager = S3BucketManager()
bucket_manager.start()

# request number
request_id : int = 0

list_bucket_header = """<ListBucketResult xmlns=\"http://s3.amazonaws.com/doc/2006-03-01/\">
    <Name>{name}</Name>
    <Prefix/>
    <Marker/>
    <MaxKeys>1000</MaxKeys>
    <IsTruncated>false</IsTruncated>"""

list_bucket_item = """
    <Contents>
       <Key>{name}</Key>
         <LastModified>{date}</LastModified>
         <ETag>\"{etag}\"</ETag>
         <Size>{size}</Size>
         <StorageClass>STANDARD_IA</StorageClass>
         <Owner>
            <ID>{owner_id}</ID>
            <DisplayName>{display_name}</DisplayName>
        </Owner>
    </Contents>"""

def makeHeaders(headers_dict: {} ) -> Headers:

    result = Headers()

    for item in headers_dict:
        result.add(item, headers_dict[item])

    return result

@s3_urls.route("/buckets/<string:bucket_name>")
def bucket_commands(bucket_name:str):
    global request_id

    current_app.logger.warning("COM: " + bucket_name)

    resp_data = ''
    status_value = 200

    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %I:%M:%S GMT")

    bucket = bucket_manager.getBucket(bucket_name)

    if bucket is not None:
        request_id += 1

        headers = makeHeaders(bucket.getStatus())

        headers.add('Date',             now)
        headers.add('x-amz-id-2',       s3_mock.s3_utils.makeLongHash("hash:" + str(request_id)))
        headers.add('x-amz-request-id', s3_mock.s3_utils.makeShortHash("hash:" + str(request_id)))

        resp_data = list_bucket_header.format(name=bucket_name)

        for item in bucket.listObjects():
            current_app.logger.warning(item)
            resp_data += list_bucket_item.format(**item)

        resp_data += "</ListBucketResult>"
    else:
        status_value = 404

    return Response(resp_data, status=status_value, headers=headers, mimetype='application/json')

@s3_urls.route("/buckets/<string:bucket_name>/<string:item>", methods=['GET'])
def item_fetch(bucket_name:str, item:str):
    global request_id

    current_app.logger.warning("PUT: " + bucket_name + " " + item)

    headers = None
    resp_data = ''
    status_value = 503

    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %I:%M:%S GMT")

    bucket = bucket_manager.getBucket(bucket_name)

    if bucket is not None:
        request_id += 1

        headers = Headers()
        headers.add('Date',             now)
        headers.add('x-amz-id-2',       s3_mock.s3_utils.makeLongHash("hash:" + str(request_id)))
        headers.add('x-amz-request-id', s3_mock.s3_utils.makeShortHash("hash:" + str(request_id)))

        s3_obj = bucket.getObject(item)

        headers.add('Last-Modified',    s3_obj.date)
        headers.add('ETag',             s3_obj.etag)
        headers.add('Content-Length',   50) #len(s3_obj.data))

        resp_data = s3_obj.data
        status_value = 200
    else:
        status_value = 404
        headers = Headers()

    return Response(resp_data, status=status_value, headers=headers, mimetype='application/json')

@s3_urls.route("/buckets/<string:bucket_name>/<string:item>", methods=['PUT'])
def item_put(bucket_name:str, item:str):
    global request_id

    headers = None
    resp_data = ''
    status_value = 503

    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %I:%M:%S GMT")

    bucket = bucket_manager.getBucket(bucket_name)

    if bucket is not None:
        request_id += 1

        headers = makeHeaders(bucket.getStatus())
        headers.add('Date',             now)
        headers.add('x-amz-id-2',       s3_mock.s3_utils.makeLongHash("hash:" + str(request_id)))
        headers.add('x-amz-request-id', s3_mock.s3_utils.makeShortHash("hash:" + str(request_id)))
        headers.add('Content-Length',   0)
        headers.add('Connnection',      'close')

        current_app.logger.warning(item)
        current_app.logger.warning(request.data)

        etag = bucket.addObject(item, data=request.data)

        if etag is not None:
            headers.add('ETag', etag)
            status_value = 200
    else:
        status_value = 404
        headers = Headers()

    return Response(resp_data, status=status_value, headers=headers, mimetype='application/json')
