import allure
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('jaeger status')
class TestStatusEndpoint(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4178 Add /status for HAProxy health check same with the main port for Bastion/Jaeger/HBP/Scrat')
    @allure.description('Verify /status endpoint work well on jaeger')
    @allure.severity('smoke')
    def test_haproxy_endpoint(self):
        r = get(jaeger_status_endpoint_qa)
        assert_that(r.status_code, equal_to(200))
