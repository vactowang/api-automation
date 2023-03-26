import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.protobuf_common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - sdk metrics logging')
class TestSDKMetricsLoggingBasic(object):

    @allure.feature('sdk metrics logging')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4412 SDK Error and Metrics logging - Implement metrics reporting endpoint')
    @allure.description('Verify the sdk metrics logging endpoint work fine')
    @allure.severity('smoke')
    def test_sdk_metrics_logging_basic(self):
        req = request_payload.sdk_metrics_logging()
        pb_message = generate_pb2_metrics_message(json_message=json.dumps(req))
        pb_serialized = pb_serialize_to_string(pb_message)
        r = post_gzip(sdk_metrics_logging_endpoint_qa, data=pb_serialized, headers=platform_headers(app_id=common_test_app))
        response_payload = r[0].json()
        assert_response_status_code(r[0].status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))
        # Verify metrics added to grafana
        # Verify that added to the sdk-metrics-20221212 topic.