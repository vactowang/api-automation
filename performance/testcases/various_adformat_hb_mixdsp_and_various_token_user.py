from locust import HttpUser, between
from performance.simples.various_adformat_meister import *
from performance.simples.various_adformat_kraken import *
from performance.simples.various_adformat_invalid_token import *
from performance.simples.various_adformat_expiry_token import *
from performance.simples.various_adformat_meister_multipule_cache_token import *
from performance.simples.various_adformat_kraken_multipule_cache_token import *


class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = {various_adformat_kraken_hb: 2, various_adformat_meister_multipule_cache_token: 2,
             various_adformat_meister_hb: 2, various_adformat_Kraken_multipule_cache_token: 2,
             various_adformat_expiry_token: 1, various_adformat_invalid_token: 1}
