# -*- coding: utf-8 -*-

import sys


def get_car_info():
    print("我有三辆车，分别是:\n 1, 车辆1;\n2, 车辆2;\n 3，车辆3")


def show_car_info(carindex):
    carTbl = {'1': "奔驰，价格1000000", '2': "宝马，价格800000", '3': "奥迪，价格600000"}
    print(carTbl[carindex])


def main():
    # 脚本调用无传入参数
    if len(sys.argv) <= 1:
        get_car_info()
    else:
        carindex = sys.argv[1]
        show_car_info(carindex)

if __name__ == '__main__':
    main()

