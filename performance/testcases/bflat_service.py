from locust import HttpUser, between
from performance.tasks.bflat_apis import *
from locust import LoadTestShape
import math


class WebsiteUser(HttpUser):
    HOST = Bflat_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = {bflat.bflat_task_01}


