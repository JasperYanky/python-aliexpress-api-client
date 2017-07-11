import logging
import json


try:
    # python 3.x
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    # python 2.x
    from urllib import urlopen, urlencode

from .config import ALIBABA_API_URL, ALIBABA_API_CALLS, ALIBABA_API_FIELDS, ALIBABA_API_PARAMS, ALIBABA_API_CATEGORIES
from .errors import *

LOGGER = logging.getLogger(__name__)


class AliExpress(object):
    api_key = None
    affiliate_id = None
    app_signature = None

    def __init__(self, api_key, affiliate_id=None, app_signature=None):
        self.api_key = api_key
        self.affiliate_id = affiliate_id
        self.app_signature = app_signature

    def get_product_list(self, fields, keywords, **kwargs):
        if not isinstance(fields, list):
            raise ValueError('Parameter %s must be a list', 'fields')

        for field in fields:
            if field not in ALIBABA_API_FIELDS['list']:
                raise ValueError('Field %s must be in %s' % (field, str(ALIBABA_API_FIELDS['list'])))

        params = {
            'fields': ','.join(fields),
            'keywords': keywords,
        }

        for param, value in kwargs.items():
            if param not in ALIBABA_API_PARAMS['list']:
                raise ValueError('Parameter %s must be in %s' % (param, str(ALIBABA_API_PARAMS['list'])))

            if param == 'categoryId' and value not in ALIBABA_API_CATEGORIES.keys():
                raise ValueError('Category %s must be in %s' % (value, str(ALIBABA_API_CATEGORIES)))

            params[param] = value

        response = self._make_call('list', params)

        if 'result' in response:
            return response['result']
        else:
            return None

    def get_product_details(self, fields, product_id, **kwargs):
        if not isinstance(fields, list):
            raise ValueError('Parameter %s must be a list', 'fields')

        for field in fields:
            if field not in ALIBABA_API_FIELDS['details']:
                raise ValueError('Field %s must be in %s' % (field, str(ALIBABA_API_FIELDS['details'])))

        params = {
            'fields': ','.join(fields),
            'productId': product_id
        }

        for param, value in kwargs.items():
            if param not in ALIBABA_API_PARAMS['details']:
                raise ValueError('Parameter %s must be in %s' % (param, str(ALIBABA_API_PARAMS['details'])))

            params[param] = value

        response = self._make_call('details', params)

        if 'result' in response:
            return response['result']
        else:
            return None

    def get_promotion_links(self, fields, urls, tracking_id=None):
        if tracking_id:
            self.affiliate_id = tracking_id

        if self.affiliate_id is None:
            raise ValueError('Affiliate tracking id is not present')

        if not isinstance(fields, list):
            raise ValueError('Parameter %s must be a list', 'fields')

        if not isinstance(urls, list):
            raise ValueError('Parameter %s must be a list', 'urls')

        for field in fields:
            if field not in ALIBABA_API_FIELDS['links']:
                raise ValueError('Field %s must be in %s' % (field, str(ALIBABA_API_FIELDS['links'])))

        params = {
            'fields': ','.join(fields),
            'trackingId': self.affiliate_id,
            'urls': ','.join(urls)
        }

        response = self._make_call('links', params)

        if 'result' in response:
            return response['result']
        else:
            return None

    def get_banner(self, category, **kwargs):
        if not category:
            category = 'all'
        params = {
            'category': category,
            'appSignature': self.app_signature,
        }

        for param, value in kwargs.items():
            if param not in ALIBABA_API_PARAMS['banner']:
                raise ValueError('Parameter %s must be in %s' % (param, str(ALIBABA_API_PARAMS['banner'])))
            params[param] = value

        if 'language' not in params:
            raise ValueError('language  must be in banner')

        if 'pageNo' not in params:
            raise ValueError('pageNo  must be in banner')

        response = self._make_call('banner', params)

        if 'result' in response:
            return response['result']
        else:
            return None

    def get_hot_products(self, categoryId, **kwargs):
        params = {
            'categoryId': categoryId,
        }
        for param, value in kwargs.items():
            if param not in ALIBABA_API_PARAMS['hot_products']:
                raise ValueError('Parameter %s must be in %s' % (param, str(ALIBABA_API_PARAMS['hot_products'])))

            params[param] = value

        response = self._make_call('hot_products', params)
        if 'result' in response:
            return response['result']
        else:
            return None

    def get_similar_products(self, productId, **kwargs):

        params = {
            'productId': productId,
        }
        for param, value in kwargs.items():
            if param not in ALIBABA_API_PARAMS['similar']:
                raise ValueError('Parameter %s must be in %s' % (param, str(ALIBABA_API_PARAMS['similar'])))

            params[param] = value

        response = self._make_call('similar', params)

        if 'result' in response:
            return response['result']
        else:
            return None

    def _make_call(self, call, params):
        url = ALIBABA_API_URL % {
            'api_call': ALIBABA_API_CALLS[call],
            'api_key': self.api_key,
            'call_parameters': urlencode(params)
        }

        LOGGER.info('Perform API request url: %s' % url)

        response = urlopen(url)

        if response.code != 200:
            raise NetworkError(call=call, code=response.code,
                               msg=json.loads(response.read().decode('utf-8'))['error_message'])

        response_json = json.loads(response.read().decode('utf-8'))

        if response_json['errorCode'] != 20010000:
            raise _e(call=call, code=response_json['errorCode'])

        return response_json
