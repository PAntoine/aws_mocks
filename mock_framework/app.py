#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Name  : app
# Desc  : convert a standard request into a lambda call.
#
# Author: 
# Date  : 19/10/2021
#
#                     Copyright (c) 2021 Peter Antoine
#                            All rights Reserved.
#                    Released Under the Artistic Licence

import json
import requests
from flask import Flask, request, Response, Blueprint
from s3_mock.s3_mock import s3_urls
from werkzeug.datastructures import Headers

app = Flask(__name__)

# register routes from s3
app.register_blueprint(s3_urls)

@app.route("/v1/test_lambda/")
def hello_world():
    req_data = { "httpMethod": "GET" }

    req_data['queryStringParameters'] = request.args

    res = requests.post("http://lambda:8080/2015-03-31/functions/function/invocations", data=json.dumps(req_data))
    
    data = json.loads(res.content)

    app.logger.warning(request.args)

    if res.status_code == 200 and 'body' in data:
        return Response(data['body'], status=data['statusCode'], mimetype='application/json') 
    else:
        return Response(data, status=res.status_code, mimetype='application/json')

@app.route("/v1/put_lambda/<string:item>", methods=['PUT'])
def put_lambda(item:str):
    req_data = { "httpMethod": "PUT" }

    req_data['queryStringParameters'] = request.args
    req_data['body'] = request.data.decode("utf-8")

    res = requests.post("http://lambda:8080/2015-03-31/functions/function/invocations", data=json.dumps(req_data))
    return Response(status=res.status_code)

@app.route("/v1/get_lambda/<string:item>", methods=['GET'])
def get_lambda(item:str):
    req_data = { "httpMethod": "GET" }

    req_data['queryStringParameters'] = request.args
    req_data['body'] = request.data.decode("utf-8")

    res = requests.post("http://lambda:8080/2015-03-31/functions/function/invocations", data=json.dumps(req_data))

    data = json.loads(res.content)

    return Response(data["body"], status=res.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
