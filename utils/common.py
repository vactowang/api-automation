import csv

import bson
import pytest
import requests
import logging
from json import dumps
import random
import uuid
import base64
import urllib.parse
from settings import *
import gzip
from datetime import datetime, timedelta
from bson.objectid import ObjectId


# Create a request headers

def headers(vungle_src=None, vungle_version=None, auth_token=None):
    headers = {'Accept': "application/json",
               'Content-Type': "application/json",
               'cache-control': "no-cache"
               }

    if vungle_src is not None:
        headers['vungle-source'] = vungle_src

    if vungle_version is not None:
        headers['vungle-version'] = vungle_version

    if auth_token is not None:
        headers['Authorization'] = 'Bearer %s' % auth_token

    return headers


# Create a platform headers
def platform_headers(sdk_version=test_default_sdk_version, src_ip=non_eu_country_ip, vungle_version='5.8', debug=None,
                     rtb_selector=None, experiment=None, override_bid_ext=None, override_bid_price=None,
                     override_bid_adomain=None, omid=None,
                     accept_encoding=None, content_encoding=None, is_hb=False, override_crid=None,
                     override_price_any=None, override_bid_response_any=None, app_id=None,
                     demoApp_DSPkey=None, demoApp_Explain=None):
    headers = {
        'Accept': "application/json",
        'Content-Type': 'application/json',
        'cache-control': 'no-cache',
        'X-Forwarded-For': src_ip,
        'X-VUNGLE-BUNDLE-ID': 'com.outfit7.mytalkingtomfree',
        'X-VUNGLE-LANGUAGE': 'ru',
        'X-VUNGLE-TIMEZONE': 'Asia/Shanghai',
        'Vungle-Version': vungle_version,
    }

    if sdk_version is not None:
        headers['user-agent'] = sdk_version

    if app_id is not None:
        headers['X-Vungle-App-Id'] = app_id

    if debug is not None:
        headers['Vungle-explain'] = debug

    if rtb_selector is not None:
        headers['X-Vungle-RTB-ID'] = rtb_selector

    if experiment is not None:
        headers['X-Vungle-Experiment-Bucket'] = experiment

    if override_bid_ext is not None:
        headers['X-Vungle-Override-Bid-Ext'] = override_bid_ext

    if override_bid_price is not None:
        headers['X-Vungle-Override-Bid-Price'] = override_bid_price

    if override_bid_adomain is not None:
        headers['X-Vungle-Override-Bid-Adomain'] = override_bid_adomain

    if override_bid_response_any is not None:
        headers['X-Vungle-Override-Bid-Response-Any'] = override_bid_response_any

    if override_crid is not None:
        if 'X-Vungle-Override-Bid-Response-Any' not in headers:
            headers['X-Vungle-Override-Bid-Response-Any'] = 'seatbid.0.bid.0.crid@"%s"' % str(override_crid)
        else:
            headers['X-Vungle-Override-Bid-Response-Any'] = headers[
                                                                'X-Vungle-Override-Bid-Response-Any'] + '|seatbid.0.bid.0.crid@"%s"' % str(
                override_crid)
    if override_price_any is not None:
        if 'X-Vungle-Override-Bid-Response-Any' not in headers:
            headers['X-Vungle-Override-Bid-Response-Any'] = 'seatbid.0.bid.0.price@%s' % override_price_any
        else:
            headers['X-Vungle-Override-Bid-Response-Any'] = headers[
                                                                'X-Vungle-Override-Bid-Response-Any'] + '|seatbid.0.bid.0.price@%s' % override_price_any

    if omid is not None:
        headers['X-Vungle-Omid'] = omid

    if accept_encoding is not None:
        headers['Accept-Encoding'] = accept_encoding

    if content_encoding is not None:
        headers['Content-Encoding'] = content_encoding

    if is_hb:
        headers['user-agent'] = sdk_version + ';' + is_hb

    if demoApp_DSPkey is not None:
        headers['X-Vungle-DSPKey'] = demoApp_DSPkey


    if demoApp_Explain is not None:
        headers['vungle-explain-demoapp'] = demoApp_Explain

    return headers


def hbp_headers(openrtb=None, sdk_version=test_default_sdk_version, src_ip=au_ip, debug=None, rtb_selector=None,
                Content_Type_uft8=None, override_bid_response_any=None, accept_encoding=None, content_encoding=None,
                Source=None, X_Env=None, demoApp_DSPkey=None, demoApp_Response=None, demoApp_Explain=None,
                override_bid_price=None):
    headers = {
        'Accept': "application/json",
        'Content-Type': 'application/json',
        'user-agent': sdk_version,
        'X-Forwarded-For': src_ip,
    }

    if openrtb is not None:
        headers['X-OpenRTB-Version'] = openrtb

    if debug is not None:
        headers['Vungle-explain'] = debug

    if rtb_selector is not None:
        headers['X-Vungle-RTB-ID'] = rtb_selector
    if Content_Type_uft8 is True:
        headers['Content-Type'] = 'application/json; charset=utf-8'

    if override_bid_price is not None:
        headers['X-Vungle-Override-Bid-Price'] = override_bid_price

    if override_bid_response_any is not None:
        headers['X-Vungle-Override-Bid-Response-Any'] = override_bid_response_any

    if accept_encoding is not None:
        headers['Accept-Encoding'] = accept_encoding

    if content_encoding is not None:
        headers['Content-Encoding'] = content_encoding

    if Source is not None:
        headers['X-Source'] = Source

    if X_Env is not None:
        headers['X-Env'] = X_Env

    if demoApp_DSPkey is not None:
        headers['X-Vungle-DSPKey'] = demoApp_DSPkey

    if demoApp_Response is not None:
        headers['X-Vungle-Demo-App-Response'] = demoApp_Response

    if demoApp_Explain is not None:
            headers['vungle-explain-demoapp'] = demoApp_Explain

    return headers


# Create a GET request and return the resposne instance
def get(url, params=None, headers=headers()):
    try:

        logging.info('Send get request with below parameters:')
        logging.info('Request headers =\n%s' % dumps(headers, indent=4))
        r = requests.get(url=url, params=params, headers=headers)
        logging.info('Request Url = %s' % r.url)
        path = url.split('//')[-1].replace(url.split('//')[-1].split('/')[0], '')
        if r.text != '':
            logging.info('Response payload =\n%s' % dumps(r.json(), indent=4))
            logging.info('Response headers =\n%s' % r.headers)
            logging.info('Response length = %s' %
                         get_content_length('response', 'GET', path, r.headers, r.content.decode()))
        return r
    except Exception as ex:
        logging.exception('An exception happens while sending get request')
        raise ex


# Create a DELETE reqeust and return the response instance
def delete(url, params=None, headers=()):
    try:
        pass
        logging.info('Send delete request with below parameters:')
        logging.info('Request headers =\n%s' % dumps(headers, indent=4))
        r = requests.delete(url=url, params=params, headers=headers)
        if r.text != '':
            logging.info('Response payload =\n%s' % dumps(r.json(), indent=4))
        return r
    except Exception as ex:
        logging.exception('An excepiton happens while sending delete request')
        raise ex


# Create a POST request and return the response instance
def post(url, json, headers=headers()):
    logging.info('Send post request with below parameters:')
    logging.info('Request Url = %s' % url)
    path = url.split('//')[-1].replace(url.split('//')[-1].split('/')[0], '')
    logging.info('Request payload =\n%s' % dumps(json, indent=4))
    logging.info('Request headers =\n%s' % dumps(headers, indent=4))
    logging.info('Request content length = %s' % get_content_length('request', 'POST', path, headers, json))

    is_int_case = False

    if 'X-Vungle-RTB-ID' not in headers.keys():
        is_int_case = True
    elif url == ads_v5_endpoint_qa_real_adbuilder:
        is_int_case = True
    else:
        for rtb in headers['X-Vungle-RTB-ID'].split(','):
            if rtb in meister_rtb_ids_list:
                is_int_case = True
                break
    if is_int_case and skip_int:
        assert True
        pytest.skip('Skipped due to the filtering out of integration test cases.')
    else:
        try:
            r = requests.post(url, json=json, headers=headers)
            if r.text != '':
                logging.info('Response payload =\n%s' % dumps(r.json(), indent=4))
                logging.info('Response headers =\n%s' % r.headers)
                logging.info('Response length = %s' %
                             get_content_length('response', 'POST', path, r.headers, r.content.decode()))
            return r
        except Exception as ex:
            logging.exception('An exception happens while sending get request')
            raise ex


# Create a gzip POST request and return the response instance
def post_gzip(url, data, headers=headers(), stream=False):
    logging.info('Send post request with below parameters:')
    logging.info('Request Url = %s' % url)
    path = url.split('//')[-1].replace(url.split('//')[-1].split('/')[0], '')
    logging.info('Request payload =\n%s' % data)
    logging.info('Request headers =\n%s' % dumps(headers, indent=4))
    logging.info('Request content length = %s' % get_content_length('request', 'POST', path, headers, data))

    is_int_case = False

    if 'X-Vungle-RTB-ID' not in headers.keys():
        is_int_case = True
    else:
        for rtb in headers['X-Vungle-RTB-ID'].split(','):
            if rtb in meister_rtb_ids_list:
                is_int_case = True
                break

    if is_int_case and skip_int:
        assert True
        pytest.skip('Skipped due to the filtering out of integration test cases.')
    else:
        try:

            r = requests.post(url, data=data, headers=headers, stream=stream)
            gzip_length = 0
            if stream:
                # logging.info('Actual gzip response body = %s' % r.raw.read())
                gzip_length = len(r.raw.read())
                r = requests.post(url, data=data, headers=headers, stream=stream)
            else:
                if r.text != '':
                    logging.info('Response payload =\n%s' % dumps(r.json(), indent=4))
                    logging.info('Response headers =\n%s' % r.headers)
                    logging.info('Response length = %s' %
                                 get_content_length('response', 'POST', path, r.headers,
                                                    gzip_encode(r.content.decode())))
            return r, gzip_length
        except Exception as ex:
            logging.exception('An exception happens while sending get request')
            raise ex


def patch(url, json, params=None, headers=headers()):
    logging.info('Send patch request with below parameters:')
    logging.info('Request Url = %s' % url)
    logging.info('Request payload =\n%s' % dumps(json, indent=4))
    logging.info('Request headers =\n%s' % dumps(headers, indent=4))
    try:
        r = requests.patch(url, params=params, json=json, headers=headers)
        if r.text != '':
            logging.info('Response payload =\n%s' % dumps(r.json(), indent=4))
        return r
    except Exception as ex:
        logging.exception('An exception happens while sending pact request')
        raise ex


def gen_device_id(digital=36):
    seed = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    id_str = []
    for i in range(digital):
        id_str.append(random.choice(seed))
    return ''.join(id_str)

def gen_unique_objId():
    demoid = bson.ObjectId()
    return demoid

def gen_test_app_id(platform = 'ios'):
    if platform == 'ios':
        test_app_generate = test_app_id_ios.replace("5fe4586f775977000126f603", str(gen_unique_objId()))
    elif platform == 'android':
        test_app_generate = test_app_id_android.replace("5f54f5eecf0f3500016d5e37", str(gen_unique_objId()))
    elif platform == 'windows':
        test_app_generate = test_app_id_windows.replace("btafg7qvsp461bgcg0ng", str(gen_unique_objId()))
    return test_app_generate


def decode_ext(url):
    ext = url.split('ext=')[1]
    ext = ext.split('&')[0]
    decoded = base64.b64decode(ext.encode('ascii')).decode('ascii')

    if decoded.count('true') > 0:
        decoded = decoded.replace('true', 'True')
    if decoded.count('false') > 0:
        decoded = decoded.replace('false', 'False')

    return eval(decoded)


def str_to_json(str):
    return json.loads(str)


def dict_to_str(dict):
    return json.dumps(dict)


def parse_url_params(url, key):
    obj = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(obj.query)

    return params[key]


def url_decoder(str):
    return urllib.parse.unquote(str)


def url_encoder(str):
    return urllib.parse.quote(str)


def decode_modes(mode):
    mode_int = int(mode)
    return mode_int >> 1 & 1 == 1, mode_int & 1 == 1


def decode_base64(data):
    """Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    return base64.b64decode(data)


def read_one_column_of_csv(path, col_title):
    """read one column in csv based on col_title.
        :param path: path of csv file.
        :param col_title: the column title.
        :returns: list of a specify colum title.
    """
    if not path and col_title:
        return
    with open(path) as f:
        reader = csv.DictReader(f)
        column = [row[col_title] for row in reader if row[col_title]]
    return column


def gzip_encode(data):
    if isinstance(data, dict):
        data = dict_to_str(data)
    gzip_encoded = gzip.compress(data.encode('utf-8'))

    return gzip_encoded


def gzip_decode(data):
    gzip_decoded = gzip.decompress(data).decode()

    return gzip_decoded


def decode_adunit(data):
    base64_decoded = decode_base64(data)
    gzip_decoded = gzip_decode(base64_decoded)

    if gzip_decoded.count('true') > 0:
        gzip_decoded = gzip_decoded.replace('true', 'True')
    if gzip_decoded.count('false') > 0:
        gzip_decoded = gzip_decoded.replace('false', 'False')

    return eval(gzip_decoded)


def get_content_length(type, method, path, headers, body):
    if body is None:
        body = ''
    elif isinstance(body, dict):
        body = dict_to_str(body)

    headers_content = ''
    for key in headers.keys():
        headers_content = headers_content + key + ': ' + headers.get(key) + ' \n\r'

    start_line = ''
    if type == 'request':
        request_line = method + ' ' + path + ' HTTP/1.1\n\r'
        start_line = request_line
    elif type == 'response':
        status_line = 'HTTP/1.1 200 OK\n\r'
        start_line = status_line

    return len(headers_content) + len(body) + len('\n\r') + len(start_line)


def is_json(str):
    try:
        json.loads(str)
        return True
    except:
        return False


def get_current_timestamp():
    now = datetime.now()

    timestamp = datetime.timestamp(now)
    return timestamp


def native_response_idsp(CTA_BUTTON_TEXT=None, CTA_BUTTON_URL=None, VUNGLE_PRIVACY_URL=None):
    data = {
        "id": "625fd0d71f3f6ddd5f0a7bbb",
        "campaign": "591007e887faec9f44000018|574351a9740cf4426b30d030|dsp-rtb_id|625fd0d71f3f6ddd5f0a7bbb",
        "app_id": "$0${\"app_id\":\"5727cbb4630ae51d400000cf\",\"eventID\":\"625fd0d71f3f6ddd5f0a7bbb\"}",
        "expiry": 1619538623,
        "delay": 0,
        "showClose": 0,
        "showCloseIncentivized": 0,
        "countdown": 0,
        "url": "",
        "videoWidth": 0,
        "videoHeight": 0,
        "adType": "vungle_mraid",
        "templateURL": "mock-url",
        "templateSettings": {
            "normal_replacements": {
                "SPONSORED_BY": "SPONSORED_BY",
                "APP_NAME": "my App text.",
                "APP_DESCRIPTION": "test test test",
                "CTA_BUTTON_TEXT": "cta text",
                "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
                "APP_RATING_VALUE": "3.5",
                "VUNGLE_PRIVACY_URL": "https://vungle.com/privacy/"
            },
            "cacheable_replacements": {
                "VUNGLE_PRIVACY_ICON_URL": {
                    "url": "https://cdn-lb.vungle.com/creative/design-framework/assets/vungle-privacy.png",
                    "extension": "png"
                },
                "APP_ICON": {
                    "url": "https://cdn-lb.vungle.com/assets/525ec4576ca69a3b4100000d/icon.png",
                    "extension": "png"
                },
                "MAIN_IMAGE": {
                    "url": "https://vungle2-cdn-qa.s3.amazonaws.com/assets/Vungle+1200+x+628-20211020-180638.jpg",
                    "extension": "png"
                }
            }
        },
        "templateId": "6088b9c76267db393dba74dd",
        "template_type": "native",
        "requires_sideloading": False,
        "timestamp": 1619535023
    }

    if CTA_BUTTON_TEXT is not None:
        data.get('templateSettings').get('normal_replacements').update({'CTA_BUTTON_TEXT': CTA_BUTTON_TEXT}),

    if CTA_BUTTON_URL is not None:
        data.get('templateSettings').get('normal_replacements').update({'CTA_BUTTON_URL': CTA_BUTTON_URL}),

    if VUNGLE_PRIVACY_URL is not None:
        data.get('templateSettings').get('normal_replacements').update({'VUNGLE_PRIVACY_URL': VUNGLE_PRIVACY_URL}),

    return data


def native_response_edsp(*asserts_fields_obj, eventtrackers=True, imptrackers=False, clicktrackers=False):
    data = {
        "native": {
            "link": {
                "url": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302"
            },
            "assets": [
                {
                    "id": 1,
                    "required": 1,
                    "img": {
                        "w": 800,
                        "h": 417,
                        "url": "https://vungle2-cdn-qa.s3.amazonaws.com/assets/Vungle+1200+x+628-20211020-180638.jpg"
                    },
                    "link": {
                        "url": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302"
                    }
                },
                {
                    "id": 6,
                    "required": 1,
                    "title": {
                        "text": "My App"
                    }
                },
                {
                    "id": 5,
                    "required": 1,
                    "img": {
                        "url": "https://cdn-lb.vungle.com/assets/525ec4576ca69a3b4100000d/icon.png"
                    },
                    "link": {
                        "url": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302"
                    }
                },
                {
                    "id": 7,
                    "required": 1,
                    "data": {
                        "value": "my App text."
                    }
                },
                {
                    "id": 9,
                    "required": 1,
                    "img": {
                        "url": "https://cdn-lb.vungle.com/creative/design-framework/assets/vungle-privacy.jpeg"
                    }
                },
                {
                    "id": 10,
                    "required": 1,
                    "data": {
                        "value": "https://privacy.vungle.com"
                    }
                }
                # {
                #     "id": 11,
                #     "required": 1,
                #     "data": {
                #         "value": "emily_test_assert_11"
                #     }
                # }
            ],
            "privacy": "http://www.myprivacyurl.com"
        }

    }

    if asserts_fields_obj is not None:
        for x in asserts_fields_obj:
            data.get('native').get('assets').append(x)
    eventtrackers_obj = [
        {
            "event": 1,
            "method": 2,
            "url": "https://us-event.app-install.bid/rtb/impr?id=124"
        }
    ]
    imptrackers_obj = [
        "https://www.mytracker.com/imptracker.js"
    ]
    clicktrackers_obj = [
        "https://www.mytracker.com/clicktracker.js"
    ]

    if eventtrackers:
        data.get('native').update({'eventtrackers': eventtrackers_obj})
    if imptrackers:
        data.get('native').update({'imptrackers': imptrackers_obj})
    if clicktrackers:
        data.get('native').get('link').update({'clicktrackers': clicktrackers_obj})

    return data


def generate_unique_objId():
    demoid = bson.ObjectId()
    return demoid


def encode_demo_app_response(bid_reponse):
    if bid_reponse is not None:
        gzip_str = gzip_encode(bid_reponse)
        base64_str = base64.b64encode(gzip_str)
        return base64_str
    else:
        return False


def decode_demo_app_response(str):
    if str is not None:
        decode_str = decode_base64(str)
        decode_gzip = gzip_decode(decode_str)
        return decode_gzip
    else:
        return False


