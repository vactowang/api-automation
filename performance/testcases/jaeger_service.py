from locust import HttpUser, between
from performance.tasks.Jaeger_apis import *


class WebsiteUser(HttpUser):
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = {Jaeger.request_jaeger_qa0,
             Jaeger.request_jaeger_qa0_ext,
             Jaeger.request_jaeger_qa0_ext_non_test_mode,
             Jaeger.request_jaeger_qa0_test_mode_kraken,
             Jaeger.request_jaeger_qa0_non_test_mode_kraken
             }




