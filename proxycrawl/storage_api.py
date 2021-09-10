import re, json
from proxycrawl.base_api import BaseAPI

#
# A Python class that acts as wrapper for ProxyCrawl Storage API.
#
# Read ProxyCrawl API documentation https://proxycrawl.com/docs/storage-api/
#
# Copyright ProxyCrawl
# Licensed under the Apache License 2.0
#

INVALID_TOKEN = 'Token is required'
INVALID_RID = 'RID is required'
INVALID_RID_ARRAY = 'One or more RIDs are required'
INVALID_URL_OR_RID = 'Either URL or RID is required'

class StorageAPI(BaseAPI):

    def get(self, url_or_rid, options = {}):
        if url_or_rid is None or url_or_rid == '':
            raise Exception(INVALID_URL_OR_RID)
        if not options.has_key('format'):
            options['format'] = 'html'
        options.update(self.__decideUrlOrRID(url_or_rid))
        self.base_path = 'storage'
        response = self.request(options)
        if options['format'] == 'json':
            response['json_body'] = response.pop('json')
        return response

    def delete(self, rid):
        if rid is None or rid == '':
            raise Exception(INVALID_RID)
        options = { 'rid': rid, 'HTTP_METHOD': 'DELETE' }
        self.base_path = 'storage'
        response = self.request(options)
        return response['status_code'] == 200

    def bulk(self, ridsArray = []):
        if not ridsArray:
            raise Exception(INVALID_RID_ARRAY)
        self.base_path = 'storage/bulk'
        self.headers = { 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json' }
        data = { 'rids': ridsArray }
        response = self.request({}, json.dumps(data))
        return response

    def rids(self, limit = -1):
        self.base_path = 'storage/rids'
        options = {}
        if limit >= 0:
            options['limit'] = limit
        response = self.request(options)
        return response['json']

    def totalCount(self):
        self.base_path = 'storage/total_count'
        response = self.request({})
        return int(response['json']['totalCount'])

    def __decideUrlOrRID(self, url_or_rid):
        if re.match(r"^https?://", url_or_rid):
            return { 'url': url_or_rid }
        else:
            return { 'rid': url_or_rid }

    def parseJsonResponse(self):
        BaseAPI.parseJsonResponse(self)
        parsed_json = json.loads(self.response['body'])
        if 'original_status' in parsed_json:
            self.response['headers']['rid'] = str(parsed_json['rid'])
            self.response['headers']['stored_at'] = str(parsed_json['stored_at'])

    def parseRegularResponse(self, handler):
        BaseAPI.parseRegularResponse(self, handler)
        headers = handler.headers
        self.response['headers']['rid'] = str(headers.get('rid'))
        self.response['headers']['stored_at'] = str(headers.get('stored_at'))
