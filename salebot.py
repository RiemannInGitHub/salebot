# -*- coding: utf-8 -*-
# !/usr/bin/env python
import car
import consumer
import aimlcov


class SaleBot(object):
    def __init__(self, userkey=None, carno=None):
        # load aiml kernel
        self.aiml = aimlcov.AimlBrain()
        self.consumer = consumer.Consumer()
        self.car = car.Car()
        if userkey:
            self.get_user_by_key(userkey)
        if carno:
            self.get_car_by_carno(carno)

    def get_user_by_key(self, userkey):
        self.consumer.loaduser(userkey)

    def get_car_by_carno(self, carno):
        self.car.loadcar(carno)

    def user_in_car(self):
        self.consumer.currentcar(self.car)

if __name__ == "__main__":
    # for test
    salerobot = SaleBot()
    while(1):
        print(salerobot.aiml.respond(raw_input(">")))


