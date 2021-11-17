# -*- coding:utf-8 -*-
import os
import shutil

from requests.structures import CaseInsensitiveDict

from .api import BasePixivAPI
from .utils import PixivError


# Public-API
class PixivAPI(BasePixivAPI):

    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        super(PixivAPI, self).__init__(**requests_kwargs)

    # Check auth and set BearerToken to headers
    def auth_requests_call(self, method, url, headers=None, params=None, data=None):
        self.require_auth()
        headers = CaseInsensitiveDict(headers or {})
        headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                'Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53 '
        headers['cookie'] = self.cookie
        r = self.requests_call(method, url, headers, params, data)
        r.encoding = 'utf-8'  # Manually set the encoding due to #11 #18 #26, thanks @Xdynix
        return r

    @classmethod
    def parse_result(cls, req):
        try:
            return cls.parse_json(req.text)
        except Exception as e:
            raise PixivError('parse_json() error: %s' % e, header=req.headers, body=req.text)

    # 排行榜/过去排行榜
    # ranking_type: [all, illust, manga, ugoira]
    # mode: [daily, weekly, monthly, rookie, original, male, female, daily_r18, weekly_r18, male_r18, female_r18, r18g]
    #       for 'illust' & 'manga': [daily, weekly, monthly, rookie, daily_r18, weekly_r18, r18g]
    #       for 'ugoira': [daily, weekly, daily_r18, weekly_r18],
    # page: [1-n]
    # date: '2015-04-01' (仅过去排行榜)
    def ranking(self, content='illust', mode='daily', p=1, date=None):
        # url = 'https://public-api.secure.pixiv.net/v1/ranking/%s.json' % ranking_type
        url = "https://www.pixiv.net/ranking.php"
        params = {
            "content": content,
            'mode': mode,
            'p': p,
            'format': "json",
        }
        if date:
            params['date'] = date
        r = self.auth_requests_call('GET', url, params=params)
        # print(r.request.headers, r.request.url)
        return self.parse_result(r)

    def download(self, url, prefix='', path=os.path.curdir, name=None, replace=False, fname=None,
                 referer='https://app-api.pixiv.net/'):
        """Download image to file (use 6.0 app-api)"""
        if hasattr(fname, 'write'):
            # A file-like object has been provided.
            file = fname
        else:
            # Determine file path by parameters.
            name = prefix + (name or fname or os.path.basename(url))
            file = os.path.join(path, name)
            if os.path.exists(file) and not replace:
                return False
        self.require_auth()
        headers = {'Referer': referer,
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53 ', 'cookie': self.cookie}
        response = self.requests_call('GET', url, headers, stream=True)

        if isinstance(file, str):
            with open(file, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        else:
            shutil.copyfileobj(response.raw, file)
        return True
