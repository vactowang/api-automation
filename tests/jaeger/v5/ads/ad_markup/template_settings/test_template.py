import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestTemplate(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('template settings')
    @allure.description('Verify template URLs from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    def test_template_url(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_10)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(ad_markup['templateURL']).count('http'), equal_to(1))

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('template settings')
    @allure.description('Verify template id from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement_id', [common_test_placement_10])
    def test_template_id(self, pub_app_id, placement_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(ad_markup).count('templateId'), equal_to(1))

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('template settings')
    @allure.description('Verify template type from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    def test_template_type(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_10)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['template_type'] in ['fullscreen', 'banner', 'flexview', 'flexfeed', 'mrec'])

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('external support')
    @allure.description('Verify the template type of programmatic banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_for_template_type_of_programmatic_banner(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, banner=True, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' not in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['template_type'], equal_to('banner'))

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('external support')
    @allure.description('Verify the template info of programmatic banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_for_template_info_of_programmatic_banner(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, banner=True, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' not in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(str(ad_markup['templateURL']).count('Banner'), equal_to(1))
            assert_that(ad_markup['templateId'], equal_to('527007e887faec9f4400007c'))

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('external support')
    @allure.description('Verify the template type of programmatic vast')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_template_type_of_programmatic_vast(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['template_type'], equal_to('fullscreen'))

    @allure.feature('static image end card')
    @allure.tag('normal', 'test_mode', 'R_1.125.0')
    @allure.story('PBJ-1498 Jaeger can support static image and html endcard')
    @allure.description('Verify template info of the static image end card inside China')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_static_image_end_card_china_1(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=au_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(ad_markup['templateURL']).count('programmaticEndcard_01'), equal_to(1))

    @allure.feature('experiment')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4187 Decoupling Programmatic Template releases from Jaeger Releases')
    @allure.description('Verify the experiment apply for template of video with endcard (id:5ea53bae55ac4bba122eb2fd)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_decoupling_template_and_jaeger_release_01(self, pub_app_id, placement):
        """
            experiment DB setting:

            {
              "_id": {
                "$oid": "6282f85346103c85f1a96cc7"
              },
              "name": "RTBEndCard_rollout",
              "mutual_id": "6279c05919e43e6d9bcbf063",
              "allocate_strategy": "math_random",
              "salt": "6282f85af215f17580b01112",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": true,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "buckets": [
                {
                  "_id": {
                    "$oid": "6282f864b0f3ca1d8d25f6ec"
                  },
                  "name": "RTBEndCard_v5",
                  "weight": 100,
                  "ext": {
                    "id": "RTBEndCard_v5_template_id",
                    "name": "RTBEndCard_v5_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/programmaticEndcard_01.zip"
                  }
                },
                {
                  "_id": {
                    "$oid": "6282f869295b2fea2298844c"
                  },
                  "name": "RTBEndCard_v6",
                  "weight": 0,
                  "ext": {
                    "id": "RTBEndCard_v6_template_id",
                    "name": "RTBEndCard_v6_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/programmaticEndcard_02.zip"
                  }
                }
              ],
              "app_whitelist": [],
              "placement_whitelist": []
            }
        """
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=au_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        assert_that(templateID, equal_to("5ea53bae55ac4bba122eb2fd"))
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(ad_markup['templateURL']).count('programmaticEndcard_01.zip'), equal_to(1))
            # Verify the experiment is added in transaction and delivery message.
            # \\""RTBEndCard_rollout\\"":\\"RTBEndCard_v5\\"

    @allure.feature('experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4187 Decoupling Programmatic Template releases from Jaeger Releases')
    @allure.description('Verify the experiment apply for of video with endcard (id:5ea53bae55ac4bba122eb2fd)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_decoupling_template_and_jaeger_release_02(self, pub_app_id, placement):
        """
            experiment DB setting:

            {
              "_id": {
                "$oid": "6282f85346103c85f1a96cc7"
              },
              "name": "RTBEndCard_rollout",
              "mutual_id": "6279c05919e43e6d9bcbf063",
              "allocate_strategy": "math_random",
              "salt": "6282f85af215f17580b01112",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": true,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "buckets": [
                {
                  "_id": {
                    "$oid": "6282f864b0f3ca1d8d25f6ec"
                  },
                  "name": "RTBEndCard_v5",
                  "weight": 100,
                  "ext": {
                    "id": "RTBEndCard_v5_template_id",
                    "name": "RTBEndCard_v5_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/programmaticEndcard_01.zip"
                  }
                },
                {
                  "_id": {
                    "$oid": "6282f869295b2fea2298844c"
                  },
                  "name": "RTBEndCard_v6",
                  "weight": 0,
                  "ext": {
                    "id": "RTBEndCard_v6_template_id",
                    "name": "RTBEndCard_v6_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/programmaticEndcard_02.zip"
                  }
                }
              ],
              "app_whitelist": [],
              "placement_whitelist": []
            }
        """
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb, src_ip=au_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        assert_that(templateID, equal_to("5ea53bae55ac4bba122eb2fd"))
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(ad_markup['templateURL']).count('programmaticEndcard_01.zip'), equal_to(1))
            # Verify the experiment is added in transaction and delivery message.
            # \\""RTBEndCard_rollout\\"":\\"RTBEndCard_v5\\"

    @allure.feature('experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4187 Decoupling Programmatic Template releases from Jaeger Releases')
    @allure.description('Verify the experiment apply for banner, TemplateID "527007e887faec9f4400007c"')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_decoupling_template_and_jaeger_release_03(self, pub_app_id, placement):
        """
            experiment DB setting:

            {
              "_id": {
                "$oid": "6284a4a753196a29c80638f4"
              },
              "name": "Banner_Mrec_rollout",
              "mutual_id": "6279c0244fb387ac302b4896",
              "allocate_strategy": "math_random",
              "salt": "6282f85af215f17580b01112",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": true,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "buckets": [
                {
                  "_id": {
                    "$oid": "6282f864b0f3ca1d8d25f6ec"
                  },
                  "name": "Banner_Mrec_v5",
                  "weight": 50,
                  "ext": {
                    "id": "Banner_Mrec_v5_template_id",
                    "name": "Banner_Mrec_v5_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/BannerEndcard_01.zip"
                  }
                },
                {
                  "_id": {
                    "$oid": "6282f869295b2fea2298844c"
                  },
                  "name": "Banner_Mrec_v6",
                  "weight": 50,
                  "ext": {
                    "id": "Banner_Mrec_v6_template_id",
                    "name": "Banner_Mrec_v6_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/Banner_Mrec_v6.zip"
                  }
                }
              ],
              "app_whitelist": [],
              "placement_whitelist": []
            }

        """
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb, src_ip=fr_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        assert_that(templateID, equal_to("527007e887faec9f4400007c"))
        assert_that(str(ad_markup['templateURL']).count('Banner'), equal_to(1))
        # Verify the experiment is added in transaction and delivery message.
        # Banner_Mrec_rollout\\"":\\"Banner_Mrec_v5\\"
        # Or
        # Banner_Mrec_rollout\\"":\\"Banner_Mrec_v6\\"

    @allure.feature('experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4187 Decoupling Programmatic Template releases from Jaeger Releases')
    @allure.description('Verify the experiment apply for mrec, TemplateID "5e93dfc72e4ace6b7a77f7a5"')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_video_mrec_placement])
    def test_decoupling_template_and_jaeger_release_04(self, pub_app_id, placement):
        """
            experiment DB setting:

            {
              "_id": {
                "$oid": "6284a4a753196a29c80638f4"
              },
              "name": "Banner_Mrec_rollout",
              "mutual_id": "6279c0244fb387ac302b4896",
              "allocate_strategy": "math_random",
              "salt": "6282f85af215f17580b01112",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": true,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "buckets": [
                {
                  "_id": {
                    "$oid": "6282f864b0f3ca1d8d25f6ec"
                  },
                  "name": "Banner_Mrec_v5",
                  "weight": 50,
                  "ext": {
                    "id": "Banner_Mrec_v5_template_id",
                    "name": "Banner_Mrec_v5_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/BannerEndcard_01.zip"
                  }
                },
                {
                  "_id": {
                    "$oid": "6282f869295b2fea2298844c"
                  },
                  "name": "Banner_Mrec_v6",
                  "weight": 50,
                  "ext": {
                    "id": "Banner_Mrec_v6_template_id",
                    "name": "Banner_Mrec_v6_template_name",
                    "url": "https://cdn-lb.vungle.com/template-rtb/Banner_Mrec_v6.zip"
                  }
                }
              ],
              "app_whitelist": [],
              "placement_whitelist": []
            }

        """
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb, src_ip=au_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        assert_that(templateID, equal_to("5e93dfc72e4ace6b7a77f7a5"))
        assert_that(str(ad_markup['templateURL']).count('Banner'), equal_to(1))
        # Verify the experiment is added in transaction and delivery message.
        # Banner_Mrec_rollout\\"":\\"Banner_Mrec_v5\\"
        # Or
        # Banner_Mrec_rollout\\"":\\"Banner_Mrec_v6\\"

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode', 'v1.222.0')
    @allure.story('PBJ-4204 Combines rtbvideoand and rtbendcard template rollout experiment.')
    @allure.description('Verify Combines rtbvideoand and rtbendcard template rollout experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_combine_rtbvideo_rtbendcard_to_exp(self, pub_app_id, placement):
        override_adm = 'seatbid.0.bid.0.adm@"<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?><VAST version=\\"2.0\\"><Ad id=\\"39569\\"><InLine><AdSystem>Chartboost<\\/AdSystem><Error><\\/Error><AdTitle><\\/AdTitle><Impression><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/impression?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Impression><Creatives><Creative><Linear><Duration>00:00:26<\\/Duration><MediaFiles><MediaFile bitrate=\\"906\\" delivery=\\"progressive\\" height=\\"1280\\" width=\\"720\\" maintainAspectRatio=\\"true\\" scalable=\\"true\\" type=\\"video\\/mp4\\"><![CDATA[https:\\/\\/v-ak.chartboost.com\\/videoads\\/617910ce629370079210e122_720-1635324110.mp4]]><\\/MediaFile><\\/MediaFiles><VideoClicks><ClickThrough><![CDATA[https:\\/\\/apps.apple.com\\/us\\/app\\/slots-cash-link-slot-machines\\/id1480805172?uo=4]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/click?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/ClickTracking><\\/VideoClicks><TrackingEvents><Tracking event=\\"firstQuartile\\"><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/completed_view?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Tracking><\\/TrackingEvents><\\/Linear><\\/Creative><\\/Creatives><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=au_ip,
                                                                        override_bid_response_any=override_adm))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateURL = ad_markup['templateURL']
        assert_that("programmaticEndcard_01.zip" in templateURL)
        # verify enter the RTBEndCard experiment "exp_to_bucket":"{\\"FlatCPM_Global_v6\\":\\"dynamic_ios_video_150\\",
        # \\"RTBEndCard_rollout\\":\\"RTBEndCard_v5\\"

    @allure.feature('Template')
    @allure.tag('normal')
    @allure.story('PBJ-4234 Combine rtbEndcard and programmatic fullscreen templates-Jaeger changes')
    @allure.description('Verify jaeger choose programmaticFullscreen template when dsp response FullScreen adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_combine_programmaticFullScreen_rtbEndcard_01(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=fr_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        templateType = ad_markup['template_type']
        templateURL = ad_markup['templateURL']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_that("https://cdn-lb.vungle.com/template-rtb/programmaticFullscreen-v4.zip" in templateURL)
        assert_that(templateID, equal_to('5ea53bae55ac4bba122eb2fd'))
        assert_that(templateType, equal_to('fullscreen'))
        assert_keys_exist(normal_replacements, 'EC_CLOSE_BUTTON_DELAY_SECONDS')
        assert_keys_exist(normal_replacements, 'INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS')
        assert_keys_exist(normal_replacements, 'SHOW_EC_CLOSE_BUTTON_COUNTDOWN')

    @allure.feature('Template')
    @allure.tag('normal')
    @allure.story('PBJ-4234 Combine rtbEndcard and programmatic fullscreen templates-Jaeger changes')
    @allure.description('Verify jaeger choose programmaticFullscreen template when dsp response rtbvideo only adm:'
                        'is_incentivized=True')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    def test_combine_programmaticFullScreen_rtbEndcard_02(self, pub_app_id, placement):
        '''

        placement db setting:
        is_incentivized: true
        '''
        override_adm = 'seatbid.0.bid.0.adm@"<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?><VAST version=\\"2.0\\"><Ad id=\\"39569\\"><InLine><AdSystem>Chartboost<\\/AdSystem><Error><\\/Error><AdTitle><\\/AdTitle><Impression><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/impression?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Impression><Creatives><Creative><Linear><Duration>00:00:26<\\/Duration><MediaFiles><MediaFile bitrate=\\"906\\" delivery=\\"progressive\\" height=\\"1280\\" width=\\"720\\" maintainAspectRatio=\\"true\\" scalable=\\"true\\" type=\\"video\\/mp4\\"><![CDATA[https:\\/\\/v-ak.chartboost.com\\/videoads\\/617910ce629370079210e122_720-1635324110.mp4]]><\\/MediaFile><\\/MediaFiles><VideoClicks><ClickThrough><![CDATA[https:\\/\\/apps.apple.com\\/us\\/app\\/slots-cash-link-slot-machines\\/id1480805172?uo=4]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/click?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/ClickTracking><\\/VideoClicks><TrackingEvents><Tracking event=\\"firstQuartile\\"><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/completed_view?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Tracking><\\/TrackingEvents><\\/Linear><\\/Creative><\\/Creatives><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=fr_ip,
                                                                        override_bid_response_any=override_adm))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        templateType = ad_markup['template_type']
        templateURL = ad_markup['templateURL']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_that("https://cdn-lb.vungle.com/template-rtb/programmaticFullscreen-v4.zip" in templateURL)
        assert_that(templateID, equal_to('528008e887faec9f4400007d'))
        assert_that(templateType, equal_to('fullscreen'))
        assert_keys_exist(normal_replacements, 'INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS')

    @allure.feature('Template')
    @allure.tag('normal')
    @allure.story('PBJ-4234 Combine rtbEndcard and programmatic fullscreen templates-Jaeger changes')
    @allure.description('Verify jaeger choose programmaticFullscreen template when dsp response rtbvideo only adm:'
                        'is_incentivized=False')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_21])
    def test_combine_programmaticFullScreen_rtbEndcard_03(self, pub_app_id, placement):
        '''

        placement db setting:
        is_incentivized: false
        '''
        override_adm = 'seatbid.0.bid.0.adm@"<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?><VAST version=\\"2.0\\"><Ad id=\\"39569\\"><InLine><AdSystem>Chartboost<\\/AdSystem><Error><\\/Error><AdTitle><\\/AdTitle><Impression><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/impression?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Impression><Creatives><Creative><Linear><Duration>00:00:26<\\/Duration><MediaFiles><MediaFile bitrate=\\"906\\" delivery=\\"progressive\\" height=\\"1280\\" width=\\"720\\" maintainAspectRatio=\\"true\\" scalable=\\"true\\" type=\\"video\\/mp4\\"><![CDATA[https:\\/\\/v-ak.chartboost.com\\/videoads\\/617910ce629370079210e122_720-1635324110.mp4]]><\\/MediaFile><\\/MediaFiles><VideoClicks><ClickThrough><![CDATA[https:\\/\\/apps.apple.com\\/us\\/app\\/slots-cash-link-slot-machines\\/id1480805172?uo=4]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/click?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/ClickTracking><\\/VideoClicks><TrackingEvents><Tracking event=\\"firstQuartile\\"><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/completed_view?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Tracking><\\/TrackingEvents><\\/Linear><\\/Creative><\\/Creatives><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=fr_ip,
                                                                        override_bid_response_any=override_adm))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        templateType = ad_markup['template_type']
        templateURL = ad_markup['templateURL']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_that("https://cdn-lb.vungle.com/template-rtb/programmaticFullscreen-v4.zip" in templateURL)
        assert_that(templateID, equal_to('528008e887faec9f4400007d'))
        assert_that(templateType, equal_to('fullscreen'))
        assert_keys_exist(normal_replacements, 'CLOSE_BUTTON_DELAY_SECONDS')

    @allure.feature('Template')
    @allure.tag('normal')
    @allure.story('PBJ-4234 Combine rtbEndcard and programmatic fullscreen templates-Jaeger changes')
    @allure.description('Verify jaeger choose programmaticFullscreen template when dsp response rtbEndcard only adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_combine_programmaticFullScreen_rtbEndcard_04(self, pub_app_id, placement):
        override_adm = 'seatbid.0.bid.0.adm@"<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?><VAST version=\\"2.0\\"><Ad id=\\"39569\\"><InLine><AdSystem>Chartboost<\\/AdSystem><Error><\\/Error><AdTitle><\\/AdTitle><Impression><![CDATA[https:\/\/ssp-events.chartboost.com\/impression?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\/Impression><Creatives><Creative><Linear><Duration>00:00:26<\\/Duration><MediaFiles><MediaFile bitrate=\\"906\\" delivery=\\"progressive\\" height=\\"1280\\" width=\\"720\\" maintainAspectRatio=\\"true\\" scalable=\\"true\\" type=\\"video\\/mp4\\"><![CDATA[https:\\/\\/v-ak.chartboost.com\\/videoads\\/617910ce629370079210e122_720-1635324110.mp4]]><\\/MediaFile><\\/MediaFiles><VideoClicks><ClickThrough><![CDATA[https:\\/\\/apps.apple.com\\/us\\/app\\/slots-cash-link-slot-machines\\/id1480805172?uo=4]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/click?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/ClickTracking><\\/VideoClicks><TrackingEvents><Tracking event=\\"firstQuartile\\"><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/completed_view?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Tracking><\\/TrackingEvents><\\/Linear><\\/Creative><Creative><CompanionAds><Companion assetHeight=\\"2000\\" assetWidth=\\"1125\\" height=\\"2000\\" width=\\"1125\\"><StaticResource creativeType=\\"image\\/jpeg\\"><![CDATA[https:\\/\\/a2.chartboost.com\\/creatives\\/5e81baac497fa20a2961bf25\\/6fd71b94fddc19110b7bcfd37089a30456fdda34.jpeg]]><\\/StaticResource><CompanionClickThrough><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/click?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ&companion=1]]><\\/CompanionClickThrough><\\/Companion><\\/CompanionAds><\\/Creative><\\/Creatives><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=fr_ip,
                                                                        override_bid_response_any=override_adm))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateID = ad_markup['templateId']
        templateType = ad_markup['template_type']
        templateURL = ad_markup['templateURL']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_that("https://cdn-lb.vungle.com/template-rtb/programmaticFullscreen-v4.zip" in templateURL)
        assert_that(templateID, equal_to('5ea53bae55ac4bba122eb2fd'))
        assert_that(templateType, equal_to('fullscreen'))
        assert_keys_exist(normal_replacements, 'EC_CLOSE_BUTTON_DELAY_SECONDS')
        assert_keys_exist(normal_replacements, 'INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS')
        assert_keys_exist(normal_replacements, 'SHOW_EC_CLOSE_BUTTON_COUNTDOWN')

    @allure.feature('Template')
    @allure.tag('normal')
    @allure.story('PBJ-4234 Combine rtbEndcard and programmatic fullscreen templates-Jaeger changes')
    @allure.description('Verify jaeger choose programmaticFullscreen template when dsp response rtbvideo only adm for '
                        'playable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01])
    def test_combine_programmaticFullScreen_rtbEndcard_playable_01(self, pub_app_id, placement):

        rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=fr_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateURL = ad_markup['templateURL']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_that("https://cdn-lb.vungle.com/template-rtb/programmaticFullscreen-v4.zip" in templateURL)
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seatbid = bid_response[rtb]['seatbid']
        adm = seatbid[0]['bid'][0]['adm']
        if 'VAST' not in adm:
            assert_keys_exist(normal_replacements, 'EC_HTML')
