from locust import HttpUser, between
from performance.simples.various_adformat_meister import *
from performance.simples.various_adformat_kraken import *
from performance.simples.various_adformat_invalid_token import *
from performance.simples.various_adformat_expiry_token import *
from performance.simples.various_adformat_jaeger import *
from performance.simples.various_adformat_hbp import *



class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = {various_adformat_kraken_hb: 2, various_adformat_kraken_non_hb: 2,
             various_adformat_meister_hb: 2, various_adformat_meister_non_hb: 2,
             various_adformat_expiry_token: 1, various_adformat_invalid_token: 1,
             various_adformat_jaeger_kraken: 2, various_adformat_jaeger_meister: 2,
             various_adformat_hbp_kraken: 2, various_adformat_hbp_meister: 2}
