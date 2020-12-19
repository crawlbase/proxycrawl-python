from proxycrawl.base_api import BaseAPI

#
# A Python class that acts as wrapper for ProxyCrawl Scraper API.
#
# Read ProxyCrawl API documentation https://proxycrawl.com/docs/scraper-api/
#
# Copyright ProxyCrawl
# Licensed under the Apache License 2.0
#
class ScraperAPI(BaseAPI):
    base_path = 'scraper'

    def get(self, url, options = {}):
        options['url'] = url
        return self.request(options)

    def post(self, url, data, options = {}):
        raise Exception('Only GET is allowed on the Scraper API')
