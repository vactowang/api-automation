
import allure
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('hbp status')
class Teststatus(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4178 Add /status for HAProxy health check same with the main port for Bastion/Jaeger/HBP/Scrat')
    @allure.description('Verify /status endpoint work well on hbp')
    @allure.severity('smoke')
    def test_config_status_endpoint(self):
        r = get(hbp_status_endpoint_qa)
        assert_that(r.status_code, equal_to(200))
