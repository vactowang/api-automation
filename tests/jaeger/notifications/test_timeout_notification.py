import allure
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('jaeger timeout')
class TestTimeoutEndpoint(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-5015 [Jaeger][Deprecate HBP] Sync TimeoutLossNotification endpoint')
    @allure.description('Verify /timeout endpoint work well on jaeger and record metric')
    def test_timeout_endpoint(self):
        r = get(jaeger_notification_timeout)
        assert_that(r.status_code, equal_to(200))
        # validate metric ssp_jaeger_timeout_notification_total
