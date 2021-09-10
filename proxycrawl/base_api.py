import json
import gzip
import ssl
import sys
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, HTTPError, Request
except ImportError:
    # Fall back to Python 2's
    from urllib2 import urlopen, HTTPError, Request
try:
    # For Python 3.0 and later
    from urllib.parse import urlencode, quote_plus
except ImportError:
    # Fall back to Python 2's
    from urllib import urlencode, quote_plus
try:
    # For Python 3.0 and later
    from io import BytesIO
except ImportError:
    # Fall back to Python 2's
    from BytesIO import BytesIO

#
# A Python class that acts as base for ProxyCrawl APIs.
#
# This is not meant to be use directly, please use the other classes.
#
# Copyright ProxyCrawl
# Licensed under the Apache License 2.0
#
PROXYCRAWL_API_URL = 'https://api.proxycrawl.com/'

class BaseAPI(object):
    timeout = 120
    headers = { 'Accept-Encoding': 'gzip' }
    base_path = ''

    def __init__(self, options):
        if options['token'] is None or options['token'] == '':
            raise Exception('You need to specify the token')
        if 'timeout' in options:
            self.timeout = options['timeout']
        self.options = options

    def request(self, options = {}, data = None):
        self.response = {}
        self.response['headers'] = {}
        http_method = options.pop('HTTP_METHOD') if options.has_key('HTTP_METHOD') else None
        url = self.buildURL(options)
        req = Request(url, headers=self.headers)
        if not http_method is None:
            req.get_method = lambda: http_method
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

        try:
            handler = urlopen(req, data, self.timeout, context=ssl_context)
        except HTTPError as error:
            self.response['body'] = ''
            self.response['status_code'] = error.code
            return self.response

        self.response['status_code'] = handler.getcode()
        response_headers = dict(handler.info())
        if ('Content-Encoding' in response_headers and response_headers['Content-Encoding'] == 'gzip') or ('content-encoding' in response_headers and response_headers['content-encoding'] == 'gzip'):
            self.response['body'] = self.decompressBody(handler)
        else:
            self.response['body'] = handler.read()

        if (handler.headers.get('Content-Type') == 'application/json; charset=utf-8' or
          (options and not options.get('callback') and options.get('format') == 'json')):
            self.parseJsonResponse()
        else:
            self.parseRegularResponse(handler)

        return self.response

    def buildURL(self, options):
        options = urlencode(options or {})
        url = PROXYCRAWL_API_URL + self.base_path + '?token=' + self.options['token'] + '&' + options

        return url

    def decompressBody(self, handler):
        body_stream = BytesIO(handler.read())
        body_gzip = gzip.GzipFile(fileobj=body_stream)

        return body_gzip.read()

    def parseJsonResponse(self):
        parsed_json = json.loads(self.response['body'])
        if 'original_status' in parsed_json:
            self.response['headers']['original_status'] = str(parsed_json['original_status'])
            self.response['headers']['pc_status'] = str(parsed_json['pc_status'])
            self.response['headers']['url'] = str(parsed_json['url'])

        if 'body' in parsed_json:
            compare_str = str if sys.version_info[0] > 2 else basestring
            if isinstance(parsed_json['body'], compare_str):
                try:
                    self.response['json'] = json.loads(parsed_json['body'])
                except ValueError:
                    self.response['json'] = parsed_json['body']
            else:
                self.response['json'] = parsed_json['body']
        else:
            self.response['json'] = parsed_json

    def parseRegularResponse(self, handler):
        headers = handler.headers
        self.response['headers']['original_status'] = str(headers.get('original_status'))
        self.response['headers']['pc_status'] = str(headers.get('pc_status'))
        self.response['headers']['url'] = str(headers.get('url'))
