# -*- coding: utf-8 -*-
# !/usr/bin/env python
import consumer
import car


class SaleBot(object):
    def __init__(self):
        self.consumer = consumer.Consumer()
        self.car = car.Car()

    def run(self):
        pass


if __name__ == "__main__":
    # for test
    salebot = SaleBot()
    SaleBot.run()
