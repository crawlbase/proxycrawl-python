import uuid, re, os, tempfile
from proxycrawl.base_api import BaseAPI

#
# A Python class that acts as wrapper for ProxyCrawl Screenshots API.
#
# Read ProxyCrawl API documentation https://proxycrawl.com/docs/screenshots-api/
#
# Copyright ProxyCrawl
# Licensed under the Apache License 2.0
#
class ScreenshotsAPI(BaseAPI):
    base_path = 'screenshots'

    def get(self, url, options = {}):
        screenshotPath = options.pop('save_to_path') if options.has_key('save_to_path') else self.__generateFilepath()
        if not re.match(r".+\.(jpg|JPG|jpeg|JPEG)$", screenshotPath):
            raise Exception('save_to_path must end with .jpg or .jpeg')
        options['url'] = url
        response = self.request(options)
        file_handle = open(screenshotPath, 'w')
        file_handle.write(response['body'])
        file_handle.close()
        response['file'] = screenshotPath
        return response

    def post(self, url, data, options = {}):
        raise Exception('Only GET is allowed on the Screenshots API')

    def parseRegularResponse(self, handler):
        headers = handler.headers
        BaseAPI.parseRegularResponse(self, handler)
        self.response['headers']['success'] = str(headers.get('success'))
        self.response['headers']['remaining_requests'] = str(headers.get('remaining_requests'))
        self.response['headers']['screenshot_url'] = str(headers.get('screenshot_url'))

    def __generateFilename(self):
        return str(uuid.uuid4()) + ".jpg"

    def __generateFilepath(self):
        return os.path.join(tempfile.gettempdir(), self.__generateFilename())