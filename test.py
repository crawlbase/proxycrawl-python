import sys
import json

from proxycrawl import CrawlingAPI, ScraperAPI, LeadsAPI, ScreenshotsAPI, StorageAPI

normal_token = ''
javascript_token = ''

def process_response(response):
    if response['status_code'] == 200:
        print('Test passed')
    else:
        print('Test failed, expected status_code 200 but got: ' + str(response['status_code']))
        sys.exit(0)

normal_api = CrawlingAPI({ 'token': normal_token })

process_response(normal_api.get('http://httpbin.org/anything?hello=world'))

process_response(normal_api.get('http://httpbin.org/anything?useragent=test', { 'user_agent': 'Mozilla/5.0 (Windows NT 6.2 rv:20.0) Gecko/20121202 Firefox/20.0' }))

process_response(normal_api.get('http://httpbin.org/anything', { 'format': 'json' }))

process_response(normal_api.post('http://httpbin.org/post', { 'hello': 'post' }))

process_response(normal_api.post('http://httpbin.org/post', json.dumps({ 'hello': 'json' }), { 'post_content_type': 'application/json' }))

javascript_api = CrawlingAPI({ 'token': javascript_token })

process_response(javascript_api.get('http://httpbin.org/anything?hello=world'))

scraper_api = ScraperAPI({ 'token': normal_token })

process_response(scraper_api.get('https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y/'))

leads_api = LeadsAPI({ 'token': normal_token })

process_response(leads_api.get_from_domain('microsoft.com'))

screenshots_api = ScreenshotsAPI({ 'token': normal_token })

process_response(screenshots_api.get('https://www.apple.com'))

storage_api = StorageAPI({ 'token': normal_token })

rids = storage_api.rids()
print('Test passed')
response = storage_api.bulk(rids)
if response['status_code'] == 200:
    print('Test passed')
    for item in response['json']:
        process_response(storage_api.get(item['url']))
        process_response(storage_api.get(item['rid']))

    if (len(response['json']) == storage_api.totalCount()):
        print('Test passed')
