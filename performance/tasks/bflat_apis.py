from locust import TaskSet
from performance.common.config import *
from performance.common.util import LocustBehaviors as LB
from random import choice



class bflat(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        self.client.verify = False
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    def bflat_task_01(self):
        LB().request_bflat(x=self, bidid=bidid, nick_name='Bflat',
                           experiment=choice(bflat_experiment_list))

    def bflat_task_02(self):
        self.client.get('/status')