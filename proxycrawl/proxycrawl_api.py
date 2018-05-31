try:
    # For Python 3.0 and later
    from urllib.request import urlopen, HTTPError
except ImportError:
    # Fall back to Python 2's
    from urllib2 import urlopen, HTTPError
try:
    # For Python 3.0 and later
    from urllib.parse import urlencode, quote_plus
except ImportError:
    # Fall back to Python 2's
    from urllib import urlencode, quote_plus
import json

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

    def __init__(self, options):
        if options['token'] is None or options['token'] == '':
            raise Exception('You need to specify the token')
        self.options = options
        self.endPointUrl = PROXYCRAWL_API_URL + '?token=' + options['token']

    def get(self, url, options = {}):
        return self.request(url, None, options)

    def post(self, url, data, options = {}):
        if isinstance(data, dict):
            data = urlencode(data)
        data = data.encode('utf-8')
        return self.request(url, data, options)

    def request(self, url, data = None, options = {}):
        self.response = {}
        url = self.buildURL(url, options)

        try:
            handler = urlopen(url, data, self.timeout)
        except HTTPError as error:
            self.response['headers'] = {}
            self.response['body'] = ''
            self.response['status_code'] = error.code
            return self.response

        self.response['status_code'] = handler.getcode()
        self.response['headers'] = handler.headers
        self.response['body'] = handler.read()
        if 'format' in options and options['format'] == 'json':
            self.parseJsonResponse()

        return self.response

    def buildURL(self, url, options):
        options = urlencode(options)
        url = quote_plus(url)
        url = self.endPointUrl + '&url=' + url + '&' + options

        return url

    def parseJsonResponse(self):
        parsed_json = json.loads(self.response['body'])
        self.response['headers']['original_status'] = str(parsed_json['original_status'])
        self.response['headers']['pc_status'] = str(parsed_json['pc_status'])
        self.response['headers']['url'] = parsed_json['url']
        self.response['body'] = parsed_json['body']
