import json
import gzip
import ssl
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
# A Python class that acts as wrapper for ProxyCrawl API.
#
# Read ProxyCrawl API documentation https://proxycrawl.com/dashboard/docs
#
# Copyright ProxyCrawl
# Licensed under the Apache License 2.0
#
PROXYCRAWL_API_URL = 'https://api.proxycrawl.com/'

class ProxyCrawlAPI:
    timeout = 30000
    headers = { 'Accept-Encoding': 'gzip' }

    def __init__(self, options):
        if options['token'] is None or options['token'] == '':
            raise Exception('You need to specify the token')
        self.options = options
        self.endPointUrl = PROXYCRAWL_API_URL + '?token=' + options['token']

    def get(self, url, options = None):
        return self.request(url, None, options)

    def post(self, url, data, options = None):
        if isinstance(data, dict):
            data = urlencode(data)
        data = data.encode('utf-8')
        return self.request(url, data, options)

    def request(self, url, data = None, options = None):
        self.response = {}
        self.response['headers'] = {}
        url = self.buildURL(url, options)
        req = Request(url, headers=self.headers)
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

        try:
            self.handler = urlopen(req, data, self.timeout, context=ssl_context)
        except HTTPError as error:
            self.response['body'] = ''
            self.response['status_code'] = error.code
            return self.response

        self.response['status_code'] = self.handler.getcode()
        self.response['body'] = self.decompressBody()

        if options and not options.get('callback') and options.get('format') == 'json':
            self.parseJsonResponse()
        else:
            self.parseRegularResponse()

        return self.response

    def buildURL(self, url, options):
        options = urlencode(options or {})
        url = quote_plus(url)
        url = self.endPointUrl + '&url=' + url + '&' + options

        return url

    def decompressBody(self):
        body_stream = BytesIO(self.handler.read())
        body_gzip = gzip.GzipFile(fileobj=body_stream)

        return body_gzip.read()

    def parseJsonResponse(self):
        parsed_json = json.loads(self.response['body'])
        self.response['headers']['original_status'] = str(parsed_json['original_status'])
        self.response['headers']['pc_status'] = str(parsed_json['pc_status'])
        self.response['headers']['url'] = str(parsed_json['url'])

    def parseRegularResponse(self):
        headers = self.handler.headers
        self.response['headers']['original_status'] = str(headers.get('original_status'))
        self.response['headers']['pc_status'] = str(headers.get('pc_status'))
        self.response['headers']['url'] = str(headers.get('url'))
