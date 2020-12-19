try:
    # For Python 3.0 and later
    from urllib.parse import urlencode, quote_plus
except ImportError:
    # Fall back to Python 2's
    from urllib import urlencode, quote_plus

from proxycrawl.base_api import BaseAPI

#
# A Python class that acts as wrapper for ProxyCrawl Crawling API.
#
# Read ProxyCrawl API documentation https://proxycrawl.com/docs/crawling-api/
#
# Copyright ProxyCrawl
# Licensed under the Apache License 2.0
#
class CrawlingAPI(BaseAPI):
    def get(self, url, options = {}):
        options['url'] = url
        return self.request(options)

    def post(self, url, data, options = {}):
        if isinstance(data, dict):
            data = urlencode(data)
        data = data.encode('utf-8')
        options['url'] = url
        return self.request(options, data)
