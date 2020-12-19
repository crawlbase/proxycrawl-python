import sys
from proxycrawl.base_api import BaseAPI

#
# A Python class that acts as wrapper for ProxyCrawl Leads API.
#
# Read ProxyCrawl API documentation https://proxycrawl.com/docs/leads-api/
#
# Copyright ProxyCrawl
# Licensed under the Apache License 2.0
#
class LeadsAPI(BaseAPI):
    base_path = 'leads'

    def get_from_domain(self, domain, options = {}):
        options['domain'] = domain
        return self.request(options)
