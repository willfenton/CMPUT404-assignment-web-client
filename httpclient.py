#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

# regular expression library
import re

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def __init__(self):
        # various regular expressions used to parse URLS and HTTP responses
        self.hostname_re = re.compile(r"(.*):(.*)")
        self.response_status_line_re = re.compile(r"(HTTP\/(\S+))\s([0-9]{3})\s([A-Z]+)")
        self.response_header_re = re.compile(r"(.+):\s(.+)")
        self.response_body_re = re.compile(r"\r\n\r\n([\s\S]*)")

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #----- PARSE URL -----#
        parsed_url = urllib.parse.urlparse(url, scheme="http")

        # extract components of the URL
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        path = parsed_url.path if len(parsed_url.path) > 0 else "/"
        port = parsed_url.port if parsed_url.port != None else 80
        
        # if the netloc is of the format host:port , take only the host
        match = re.match(self.hostname_re, netloc)
        host = match.group(1) if match else netloc

        # make sure it's using http
        if scheme != "http":
            print(f"Invalid scheme \"{parsed_url.scheme}\". Only HTTP is supported.")
            return

        #----- BUILD HTTP REQUEST -----#
        status_line = f"GET {path} HTTP/1.1"
        host_line = f"Host: {host}"
        body = ""

        request = f"{status_line}\r\n{host_line}\r\n\r\n{body}"

        #----- SEND HTTP REQUEST -----#
        self.connect(host, port)                # connect to the host
        self.sendall(request)                   # send the HTTP request
        response = self.recvall(self.socket)    # receive the HTTP response
        self.close()                            # close the connection

        #----- PARSE RESPONSE -----$
        status_line_matches = re.findall(self.response_status_line_re, response)
        header_matches = re.findall(self.response_header_re, response)
        body_matches = re.findall(self.response_body_re, response)

        status_code = int(status_line_matches[0][2])    # response status code
        response_body = body_matches[0]                 # response body

        #----- LOGGING -----#
        # print(f"URL: {url}")
        # print(f"URLPARSE: {parsed_url}")
        # print(f"HOST: {host}")
        # print(f"PATH: {path}")
        # print(f"PORT: {port}")
        # print(f"REQUEST:\n{repr(request)}")
        # print(f"RESPONSE:\n{repr(response)}")
        # print(f"STATUS:\n{status_line_matches}")
        # print(f"HEADERS:\n{header_matches}")
        # print(f"BODY:\n{body_matches}")
        print(body)

        return HTTPResponse(status_code, response_body)

    def POST(self, url, args=None):
        #----- PARSE URL -----#
        parsed_url = urllib.parse.urlparse(url, scheme="http")

        # extract components of the URL
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        path = parsed_url.path if len(parsed_url.path) > 0 else "/"
        port = parsed_url.port if parsed_url.port != None else 80
        
        # if the netloc is of the format host:port , take only the host
        match = re.match(self.hostname_re, netloc)
        host = match.group(1) if match else netloc

        # make sure it's using http
        if scheme != "http":
            print(f"Invalid scheme \"{parsed_url.scheme}\". Only HTTP is supported.")
            return

        #----- BUILD HTTP REQUEST -----#
        body = urllib.parse.urlencode(args) if args else ""

        status_line = f"POST {path} HTTP/1.1"
        host_line = f"Host: {host}"
        content_type_line = "Content-Type: application/x-www-form-urlencoded"
        content_length_line = f"Content-Length: {len(body)}"

        request = f"{status_line}\r\n{host_line}\r\n{content_type_line}\r\n{content_length_line}\r\n\r\n{body}"

        #----- SEND HTTP REQUEST -----#
        self.connect(host, port)                # connect to the host
        self.sendall(request)                   # send the HTTP request
        response = self.recvall(self.socket)    # receive the HTTP response
        self.close()                            # close the connection

        #----- PARSE RESPONSE -----$
        status_line_matches = re.findall(self.response_status_line_re, response)
        header_matches = re.findall(self.response_header_re, response)
        body_matches = re.findall(self.response_body_re, response)

        status_code = int(status_line_matches[0][2])    # response status code
        response_body = body_matches[0]                 # response body

        #----- LOGGING -----#
        # print(f"URL: {url}")
        # print(f"URLPARSE: {parsed_url}")
        # print(f"HOST: {host}")
        # print(f"PATH: {path}")
        # print(f"PORT: {port}")
        # print(f"REQUEST:\n{repr(request)}")
        # print(f"RESPONSE:\n{repr(response)}")
        # print(f"STATUS:\n{status_line_matches}")
        # print(f"HEADERS:\n{header_matches}")
        # print(f"BODY:\n{body_matches}")
        print(body)

        return HTTPResponse(status_code, response_body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)
    
if __name__ == "__main__":
    client = HTTPClient()
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
