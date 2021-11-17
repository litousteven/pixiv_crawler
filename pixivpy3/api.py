# -*- coding:utf-8 -*-
import hashlib
import json
import os
import shutil
from datetime import datetime

import cloudscraper
from requests.structures import CaseInsensitiveDict

from .utils import PixivError, JsonDict


class BasePixivAPI(object):
    client_id = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
    client_secret = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
    hash_secret = '28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c'

    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        self.cookie = None
        # self.requests = requests.Session()
        self.requests = cloudscraper.create_scraper()  # fix due to #140
        self.additional_headers = CaseInsensitiveDict(requests_kwargs.pop('headers', {}))
        self.requests_kwargs = requests_kwargs

    def set_additional_headers(self, headers):
        """manually specify additional headers. will overwrite API default headers in case of collision"""
        self.additional_headers = CaseInsensitiveDict(headers)

    # 设置HTTP的Accept-Language (用于获取tags的对应语言translated_name)
    # language: en-us, zh-cn, ...
    def set_accept_language(self, language):
        """set header Accept-Language for all requests (useful for get tags.translated_name)"""
        self.additional_headers['Accept-Language'] = language

    @classmethod
    def parse_json(cls, json_str):
        """parse str into JsonDict"""
        return json.loads(json_str, object_hook=JsonDict)

    def require_auth(self):
        if self.cookie is None:
            raise PixivError('Authentication required! Call login() or set_cookie() first!')

    def requests_call(self, method, url, headers=None, params=None, data=None, stream=False):
        """ requests http/https call for Pixiv API """
        merged_headers = self.additional_headers.copy()
        if headers:
            # Use the headers in the parameter to override the
            # additional_headers setting.
            merged_headers.update(headers)
        try:
            if method == 'GET':
                return self.requests.get(
                    url, params=params,
                    headers=merged_headers, stream=stream,
                    **self.requests_kwargs
                )
            elif method == 'POST':
                return self.requests.post(
                    url, params=params, data=data,
                    headers=merged_headers, stream=stream,
                    **self.requests_kwargs
                )
            elif method == 'DELETE':
                return self.requests.delete(
                    url, params=params, data=data,
                    headers=merged_headers, stream=stream,
                    **self.requests_kwargs
                )
        except Exception as e:
            raise PixivError('requests %s %s error: %s' % (method, url, e))

        raise PixivError('Unknown method: %s' % method)

    def set_cookie(self, cookie):
        self.cookie = cookie

    def set_client(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
