import requests
import logging
from typing import Optional


logger = logging.getLogger(__name__)


class ServiceError(Exception):
    pass


def make_request(url, method='get', **kwargs):
    m = getattr(requests, method)
    try:
        response = m(url, **kwargs)
    except requests.ConnectionError as e:
        raise ServiceError from e
    return response


def get(url, params=None, **kwargs):
    return make_request(url, method='get', params=params, **kwargs)


def post(url, data=None, **kwargs):
    return make_request(url, method='post', data=data, **kwargs)


def put(url, data=None, **kwargs):
    return make_request(url, method='put', data=data, **kwargs)


class Service:
    def __init__(self, location):
        self.location = location

    def build_absolute_url(self, path: Optional[str]) -> str:
        """Build absolute URI with given (optional) path."""
        path = path or ''
        if path.startswith('http://') or path.startswith('https://'):
            return path
        if self.location.endswith('/') and path.startswith('/'):
            path = path[1:]
        return host_url + path

    def get(self, path, params):
        url = self.build_absolute_url(path)
        r = get(url, params=params, **kwargs)
        return r.json()

    def post(self, path, data):
        url = self.build_absolute_url(path)
        r = post(url, data=data, **kwargs)
        return r.json()

    def put(self, path, data):
        url = self.build_absolute_url(path)
        r = put(url, data=data, **kwargs)
        return r.json()
