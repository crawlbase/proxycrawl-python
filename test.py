import sys
import json
try:
    # For Python 3.0 and later
    from proxycrawl.proxycrawl_api import ProxyCrawlAPI
except ImportError:
    # Fall back to Python 2's
    from proxycrawl import ProxyCrawlAPI

normal_token = ''
javascript_token = ''

def process_response(response):
    if response['status_code'] == 200:
        print('Test passed')
    else:
        print('Test failed, expected status_code 200 but got: ' + str(response['status_code']))
        sys.exit(0)

normal_api = ProxyCrawlAPI({ 'token': normal_token })

process_response(normal_api.get('http://httpbin.org/anything?hello=world'))

process_response(normal_api.get('http://httpbin.org/anything?useragent=test', { 'user_agent': 'Mozilla/5.0 (Windows NT 6.2 rv:20.0) Gecko/20121202 Firefox/20.0' }))

process_response(normal_api.get('http://httpbin.org/anything', { 'format': 'json' }))

process_response(normal_api.post('http://httpbin.org/post', { 'hello': 'post' }))

process_response(normal_api.post('http://httpbin.org/post',  json.dumps({ 'hello': 'json' }), { 'post_content_type': 'application/json' }))

javascript_api = ProxyCrawlAPI({ 'token': javascript_token })

process_response(javascript_api.get('http://httpbin.org/anything?hello=world'))
