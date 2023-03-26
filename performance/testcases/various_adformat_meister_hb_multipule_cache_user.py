from locust import HttpUser, between
from performance.simples.various_adformat_meister_multipule_cache_token import *


class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = [various_adformat_meister_multipule_cache_token]

