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
    def get(self, url, options = None):
        return self.request(url, None, options)

    def post(self, url, data, options = None):
        if isinstance(data, dict):
            data = urlencode(data)
        data = data.encode('utf-8')
        return self.request(url, data, options)
