import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('scrat - cache bust')
class TestScratCacheBust(object):

    @allure.feature('cache bust')
    @allure.tag('smoke', 'v0.140.0', 'test_mode', 'v0.151.0')
    @allure.story('PBJ-3890 Moving the cache bust endpoints to events.api.vungle.com'
                  'PBJ-4258 Support Cache Bust Setting to clear the cache')
    @allure.description('Verify the cache bust response info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('last_cache_bust', [0, None])
    def test_cache_bust_endpoint(self, pub_app_id, last_cache_bust):
        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(isinstance(response_payload['cache_bust']['last_updated'], int))
        assert_that(isinstance(response_payload['cache_bust']['campaign_ids'], list))
        assert_that(isinstance(response_payload['cache_bust']['creative_ids'], list))

    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.140.0', 'test_mode')
    @allure.story('PBJ-3890 Moving the cache bust endpoints to events.api.vungle.com')
    @allure.description('Verify the cache bust request with 0 or no last update time')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('last_cache_bust', [0, None])
    def test_cache_bust_endpoint_1(self, pub_app_id, last_cache_bust):
        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(isinstance(response_payload['cache_bust']['last_updated'], int))
        assert_that(isinstance(response_payload['cache_bust']['campaign_ids'], list))
        if len(response_payload['cache_bust']['campaign_ids']) > 0:
            assert_that(isinstance(response_payload['cache_bust']['campaign_ids'][0]['id'], str))
            assert_that(isinstance(response_payload['cache_bust']['campaign_ids'][0]['timestamp_bust_end'], int))
        assert_that(isinstance(response_payload['cache_bust']['creative_ids'], list))
        if len(response_payload['cache_bust']['creative_ids']) > 0:
            assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['id'], str))
            assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['timestamp_bust_end'], int))

    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.140.0', 'test_mode', 'v0.151.0')
    @allure.story('PBJ-3890 Moving the cache bust endpoints to events.api.vungle.com')
    @allure.description('Verify the cache bust request with last update time over the update time of all records')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('last_cache_bust', [4121553644])
    def test_cache_bust_endpoint_2(self, pub_app_id, last_cache_bust):
        '''
        4121553644 is a time on 2100-08-10
        '''
        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(len(response_payload['cache_bust']['campaign_ids']), equal_to(0))
        assert_that(len(response_payload['cache_bust']['creative_ids']), equal_to(0))


    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.151.0')
    @allure.story('PBJ-4258 Support Cache Bust Setting to clear the cache')
    @allure.description('Verify the cache bust request with last update time during the update time for the pub apps '
                        'that belongs to the config accounts')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('last_cache_bust', [1654684221])
    def test_cache_bust_endpoint_pub_setting_01(self, pub_app_id, last_cache_bust):
        """
        1654684221 is a time on 2022/06/08

        DB Setting:
        accounts:["597565c6c5511a1b62000990", "561e8d956b8d90f61a002742"]
        """

        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['id'], str))
        assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['timestamp_bust_end'], int))


    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.151.0')
    @allure.story('PBJ-4258 Support Cache Bust Setting to clear the cache')
    @allure.description('Verify the cache bust request with last update time during the update time for the pub apps '
                        'that belongs to the config account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('last_cache_bust', [1654684221])
    def test_cache_bust_endpoint_pub_setting_02(self, pub_app_id, last_cache_bust):
        """
        1654684221 is a time on 2022/06/08

        DB Setting:
        accounts:["597565c6c5511a1b62000990", "561e8d956b8d90f61a002742"]
        """

        req = request_payload.cache_bust_android(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['id'], str))
        assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['timestamp_bust_end'], int))



    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.151.0')
    @allure.story('PBJ-4258 Support Cache Bust Setting to clear the cache')
    @allure.description('Verify the cache bust request with last update time during the update time for the pub apps '
                        'that does not belongs to the config account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [mrec_test_app])
    @pytest.mark.parametrize('last_cache_bust', [40888044241])
    def test_cache_bust_endpoint_pub_setting_03(self, pub_app_id, last_cache_bust):
        """
        1654684221 is a time on 2099

        DB Setting:
        accounts:["597565c6c5511a1b62000990", "561e8d956b8d90f61a002742"]
        """

        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(len(response_payload['cache_bust']['campaign_ids']), equal_to(0))
        assert_that(len(response_payload['cache_bust']['creative_ids']), equal_to(0))


    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.151.0')
    @allure.story('PBJ-4258 Support Cache Bust Setting to clear the cache')
    @allure.description('Verify the cache bust request with last update time during the update time for the pub apps '
                        'tha belongs to the config account but is_deleted=True')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('last_cache_bust', [1654684221])
    def test_cache_bust_endpoint_pub_setting_04(self, pub_app_id, last_cache_bust):
        """
        1654684221 is a time on 2022/06/08

        DB Setting:
        accounts:["597565c6c5511a1b62000990", "561e8d956b8d90f61a002742"]

        is_delete: True
        """

        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(len(response_payload['cache_bust']['campaign_ids']), equal_to(0))
        assert_that(len(response_payload['cache_bust']['creative_ids']) > 0)



    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.151.0')
    @allure.story('PBJ-4258 Support Cache Bust Setting to clear the cache')
    @allure.description('Verify the cache bust request with last update time over the update time for the pub apps '
                        'tha belongs to the config account but is_deleted=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('last_cache_bust', [4121553644])
    def test_cache_bust_endpoint_pub_setting_05(self, pub_app_id, last_cache_bust):
        """
        4121553644 is a time on 2100-08-10

        DB Setting:
        accounts:["597565c6c5511a1b62000990", "561e8d956b8d90f61a002742"]

        is_delete: False
        """

        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(len(response_payload['cache_bust']['campaign_ids']), equal_to(0))
        assert_that(len(response_payload['cache_bust']['creative_ids']), equal_to(0))


    @allure.feature('cache bust')
    @allure.tag('normal', 'v0.151.0')
    @allure.story('PBJ-4258 Support Cache Bust Setting to clear the cache')
    @allure.description('Verify the timestamp_bust_end equal to the large one if both setting in cache_bust_pub and'
                        'cache_bust_requests collection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('last_cache_bust', [1654684221])
    def test_cache_bust_endpoint_pub_setting_06(self, pub_app_id, last_cache_bust):
        """
        1654684221 is a time on 2022/06/08

        DB Setting:
        cache_bust_pub:
        target:"5b50579f41cdd310218b2289"
        bust_end_date:1654510159000

        cache_bust_requests:
        target_ids:["5b50579f41cdd310218b2289", "60f06f4fd8803f0018dbc13e"]
        bust_end_date:1654742208251


        is_delete: False
        """

        req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
        r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.cache_bust)
        assert_that(len(response_payload['cache_bust']['campaign_ids']), equal_to(0))
        assert_that(len(response_payload['cache_bust']['creative_ids']) > 0)
        creative_ids = response_payload['cache_bust']['creative_ids']
        for x in creative_ids:
            if x['id'] == '5b50579f41cdd310218b2289':
                timestamp_1 = x['timestamp_bust_end']

            if x['id'] == '60f06f4fd8803f0018dbc13e':
                timestamp_2 = x['timestamp_bust_end']

        assert_that(timestamp_1, equal_to(timestamp_2))




