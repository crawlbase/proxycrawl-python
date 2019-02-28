# ProxyCrawl API Python class

A lightweight, dependency free Python class that acts as wrapper for ProxyCrawl API.

## Installing

Choose a way of installing:

- Download the python class from Github.
- Or use [PyPi](https://pypi.org/project/proxycrawl/) Python package manager. `pip install proxycrawl`

Then import the ProxyCrawlAPI

Python2:

```python
from proxycrawl import ProxyCrawlAPI
```

Python3:

```python
from proxycrawl.proxycrawl_api import ProxyCrawlAPI
```

## Class usage

First initialize the ProxyCrawlAPI class

```python
api = ProxyCrawlAPI({ 'token': 'YOUR_PROXYCRAWL_TOKEN' })
```

### GET requests

Pass the url that you want to scrape plus any options from the ones available in the [API documentation](https://proxycrawl.com/dashboard/docs).

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

Pass the url that you want to scrape, the data that you want to send which can be either a json or a string, plus any options from the ones available in the [API documentation](https://proxycrawl.com/dashboard/docs).

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
api = ProxyCrawlAPI({ 'token': 'YOUR_JAVASCRIPT_TOKEN' })
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

You can always get the original status and proxycrawl status from the response. Read the [ProxyCrawl documentation](https://proxycrawl.com/dashboard/docs) to learn more about those status.

```python
response = api.get('https://craiglist.com')
print(response['headers']['original_status'])
print(response['headers']['pc_status'])
```

If you have questions or need help using the library, please open an issue or [contact us](https://proxycrawl.com/contact).

---

Copyright 2019 ProxyCrawl
