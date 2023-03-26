from locust import HttpUser, between
from performance.simples.various_adformat_meister import *
from performance.simples.various_adformat_kraken import *


class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = {various_adformat_kraken_hb: 1, various_adformat_kraken_non_hb: 1,
             various_adformat_meister_hb: 1, various_adformat_meister_non_hb: 1}


