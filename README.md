# ProxyCrawl API Python class

A lightweight, dependency free Python class that acts as wrapper for ProxyCrawl API.

## Installing

Choose a way of installing:

- Download the python class from Github.
- Or use [PyPi](https://pypi.org/project/proxycrawl/) Python package manager. `pip install proxycrawl`

Then import the CrawlingAPI, ScraperAPI, etc as needed.

```python
from proxycrawl import CrawlingAPI, ScraperAPI, LeadsAPI, ScreenshotsAPI, StorageAPI
```

### Upgrading to version 3

Version 3 deprecates the usage of ProxyCrawlAPI in favour of CrawlingAPI (although is still usable). Please test the upgrade before deploying to production.

## Crawling API

First initialize the CrawlingAPI class.

```python
api = CrawlingAPI({ 'token': 'YOUR_PROXYCRAWL_TOKEN' })
```

### GET requests

Pass the url that you want to scrape plus any options from the ones available in the [API documentation](https://proxycrawl.com/docs).

```python
api.get(url, options = {})
```

Example:

```python
response = api.get('https://www.facebook.com/britneyspears')
if response['status_code'] == 200:
    print(response['body'])
```

You can pass any options from ProxyCrawl API.

Example:

```python
response = api.get('https://www.reddit.com/r/pics/comments/5bx4bx/thanks_obama/', {
    'user_agent': 'Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/30.0',
    'format': 'json'
})
if response['status_code'] == 200:
    print(response['body'])
```

### POST requests

Pass the url that you want to scrape, the data that you want to send which can be either a json or a string, plus any options from the ones available in the [API documentation](https://proxycrawl.com/docs).

```python
api.post(url, dictionary or string data, options = {})
```

Example:

```python
response = api.post('https://producthunt.com/search', { 'text': 'example search' })
if response['status_code'] == 200:
    print(response['body'])
```

You can send the data as `application/json` instead of `x-www-form-urlencoded` by setting option `post_content_type` as json.

```python
import json
response = api.post('https://httpbin.org/post', json.dumps({ 'some_json': 'with some value' }), { 'post_content_type': 'json' })
if response['status_code'] == 200:
    print(response['body'])
```

### Javascript requests

If you need to scrape any website built with Javascript like React, Angular, Vue, etc. You just need to pass your javascript token and use the same calls. Note that only `.get` is available for javascript and not `.post`.

```python
api = CrawlingAPI({ 'token': 'YOUR_JAVASCRIPT_TOKEN' })
```

```python
response = api.get('https://www.nfl.com')
if response['status_code'] == 200:
    print(response['body'])
```

Same way you can pass javascript additional options.

```python
response = api.get('https://www.freelancer.com', { 'page_wait': 5000 })
if response['status_code'] == 200:
    print(response['body'])
```

## Original status

You can always get the original status and proxycrawl status from the response. Read the [ProxyCrawl documentation](https://proxycrawl.com/docs) to learn more about those status.

```python
response = api.get('https://craiglist.com')
print(response['headers']['original_status'])
print(response['headers']['pc_status'])
```

If you have questions or need help using the library, please open an issue or [contact us](https://proxycrawl.com/contact).

## Scraper API

The usage of the Scraper API is very similar, just change the class name to initialize.

```python
scraper_api = ScraperAPI({ 'token': 'YOUR_NORMAL_TOKEN' })

response = scraper_api.get('https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y/')
if response['status_code'] == 200:
    print(response['json']['name']) # Will print the name of the Amazon product
```

## Leads API

To find email leads you can use the leads API, you can check the full [API documentation](https://proxycrawl.com/docs/leads-api/) if needed.

```python
leads_api = LeadsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })

response = leads_api.get_from_domain('microsoft.com')

if response['status_code'] == 200:
    print(response['json']['leads'])
```

## Screenshots API

Initialize with your Screenshots API token and call the `get` method.

```python
screenshots_api = ScreenshotsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
response = screenshots_api.get('https://www.apple.com')
if response['status_code'] == 200:
    print(response['headers']['success'])
    print(response['headers']['url'])
    print(response['headers']['remaining_requests'])
    print(response['file'])
```

or specifying a file path

```python
screenshots_api = ScreenshotsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
response = screenshots_api.get('https://www.apple.com', { 'save_to_path': 'apple.jpg' })
if response['status_code'] == 200:
    print(response['headers']['success'])
    print(response['headers']['url'])
    print(response['headers']['remaining_requests'])
    print(response['file'])
```

or if you set `store=true` then `screenshot_url` is set in the returned headers 

```python
screenshots_api = ScreenshotsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
response = screenshots_api.get('https://www.apple.com', { 'store': 'true' })
if response['status_code'] == 200:
    print(response['headers']['success'])
    print(response['headers']['url'])
    print(response['headers']['remaining_requests'])
    print(response['file'])
    print(response['headers']['screenshot_url'])
```

Note that `screenshots_api.get(url, options)` method accepts an [options](https://proxycrawl.com/docs/screenshots-api/parameters)

## Storage API

Initialize the Storage API using your private token.

```python
storage_api = StorageAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
```

Pass the [url](https://proxycrawl.com/docs/storage-api/parameters/#url) that you want to get from [Proxycrawl Storage](https://proxycrawl.com/dashboard/storage).

```python
response = storage_api.get('https://www.apple.com')
if response['status_code'] == 200:
    print(response['headers']['original_status'])
    print(response['headers']['pc_status'])
    print(response['headers']['url'])
    print(response['headers']['rid'])
    print(response['headers']['stored_at'])
    print(response['body'])
```

or you can use the [RID](https://proxycrawl.com/docs/storage-api/parameters/#rid)

```python
response = storage_api.get('RID_REPLACE')
if response['status_code'] == 200:
    print(response['headers']['original_status'])
    print(response['headers']['pc_status'])
    print(response['headers']['url'])
    print(response['headers']['rid'])
    print(response['headers']['stored_at'])
    print(response['body'])
```

Note: One of the two RID or URL must be sent. So both are optional but it's mandatory to send one of the two.

### [Delete](https://proxycrawl.com/docs/storage-api/delete/) request

To delete a storage item from your storage area, use the correct RID

```python
if storage_api.delete('RID_REPLACE'):
  print('delete success')
else:
  print('Unable to delete')
```

### [Bulk](https://proxycrawl.com/docs/storage-api/bulk/) request

To do a bulk request with a list of RIDs, please send the list of rids as an array

```python
response = storage_api.bulk(['RID1', 'RID2', 'RID3', ...])
if response['status_code'] == 200:
    for item in response['json']:
        print(item['original_status'])
        print(item['pc_status'])
        print(item['url'])
        print(item['rid'])
        print(item['stored_at'])
        print(item['body'])
```

### [RIDs](https://proxycrawl.com/docs/storage-api/rids) request

To request a bulk list of RIDs from your storage area

```python
rids = storage_api.rids()
print(rids)
```

You can also specify a limit as a parameter

```python
storage_api.rids(100)
```

### [Total Count](https://proxycrawl.com/docs/storage-api/total_count)

To get the total number of documents in your storage area

```python
total_count = storage_api.totalCount()
print(total_count)
```

## Custom timeout

If you need to use a custom timeout, you can pass it to the class instance creation like the following:

```python
api = CrawlingAPI({ 'token': 'TOKEN', 'timeout': 120 })
```

Timeout is in seconds.

---

Copyright 2021 ProxyCrawl
