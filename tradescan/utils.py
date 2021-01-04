import json
import requests

class TradescanApiException(Exception):

    def __init__(self, error_code, error_message, error):
        super(TradescanApiException, self).__init__(error_message)
        self.error_code = error_code
        self.error = error

class Request(object):

    def __init__(self, api_url = 'https://switcheo.org', timeout = 30):
        self.url = api_url.rstrip('/')
        self.timeout = timeout

    def get(self, path, params=None):
        """Perform GET request"""
        r = requests.get(url=self.url + path, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def post(self, path, data=None, json_data=None, params=None):
        """Perform POST request"""
        r = requests.post(url=self.url + path, data=data, json=json_data, params=params, timeout=self.timeout)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise TradescanApiException(r.json().get('error_code'), r.json().get('error_message'), r.json().get('error'))
        return r.json()

    def status(self):
        r = requests.get(url=self.url)
        r.raise_for_status()
        return r.json()
