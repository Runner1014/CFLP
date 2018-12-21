#!/usr/bin/python
# -*- coding: UTF-8 -*-
from idlelib.multicall import r

import re
import random
import copy
import math
from typing import Any, Union


class System:
    def __init__(self):
        self.fnum = 0  # 设备数量
        self.cnum = 0  # 用户数量
        self.facilities = []
        self.status = []  # 工厂状态
        self.customers = []
        self.assignment = []  # 每个用户分配到哪个设备
        self.total_cost = 0  # 总成本

    def total(self):  # 计算总成本
        for i in range(self.cnum):
            self.status[self.assignment[i]] = 1
        cost = 0
        for i in range(self.cnum):
            cost += self.customers[i].assign_cost[self.assignment[i]]
        for i in range(self.fnum):
            if self.status[i] == 1:
                cost += self.facilities[i].opening_cost
        self.total_cost = cost
        return cost


class Facility:
    def __init__(self):
        self.capacity = 0  # 总容量
        self.opening_cost = 0  # 开启成本
        self.rest = 0  # 剩余容量


class Customer:
    def __init__(self):
        self.demand = 0  # 需求量
        self.assign_cost = []  # 某设备分派给用户的成本


fnum = 0
cnum = 0
facilities = []
customers = []
total_cost = 0
status = []
assignment = []
best = []

def total(assignment):
    if assignment is None:
        return -1
    for i in range(cnum):
        status[assignment[i]] = 1
    cost = 0
    for i in range(cnum):
        cost += customers[i].assign_cost[assignment[i]]
    for i in range(fnum):
        if status[i] == 1:
            cost += facilities[i].opening_cost
    return cost


def generate(current):
    customer_1 = random.randint(0, cnum - 1)
    customer_2 = random.randint(0, cnum - 1)
    _next = copy.deepcopy(current)
    while customer_2 == customer_1:
        customer_2 = random.randint(0, cnum - 1)
    method = random.randint(1, 4)
    # print(method)
    if method == 1:
        _next[customer_1] = current[customer_2]
        _next[customer_2] = current[customer_1]
    elif method == 7:
        if customer_1 < customer_2:
            for i in range(customer_2 - customer_1):
                _next[customer_1 + i] = current[customer_2 - i];
        else:
            for i in range(customer_1 - customer_2):
                _next[customer_2 + i] = _next[customer_1 - i]
    elif method == 2 or method == 3 or method == 4:
        _next[customer_1] = random.randint(1, fnum - 1)
        _next[customer_2] = random.randint(1, fnum - 1)
    elif method == 4:
        if customer_1 < customer_2:
            for i in range(customer_2 - customer_1):
                _next[i] = random.randint(0, (fnum - 1) // 2 - 1)
        else:
            for i in range(customer_1 - customer_2):
                _next[i] = random.randint((fnum - 1) // 2, fnum - 1)

    return _next


def is_valid(assignment):
    if not isinstance(assignment, list):
        return False
    for i in range(fnum):
        total_demand = 0
        for j in range(cnum):
            if assignment[j] == i:
                total_demand += customers[j].demand
                if total_demand > facilities[i].capacity:
                    return False
    return True


def show():
    print('result', total_cost)
    print('status', status)
    print('assignment:', assignment)


# 贪心算法
def greed():
    global total_cost, status
    # status = [1] * fnum
    status = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
              0, 1, 1, 1, 1]
    for i in range(fnum):
        total_cost += facilities[i].opening_cost
    for i in range(cnum):
        min_cost = 999999999
        cost = 99999999
        for j in range(fnum):
            if status[j] == 1 and facilities[j].rest >= customers[i].demand:
                cost = customers[i].assign_cost[j]
                # if status[j] != 1:
                #     cost += facilities[j].opening_cost
                if cost < min_cost:
                    min_cost = cost
                    assignment[i] = j
        if assignment[i] != -1:
            total_cost += min_cost
            # status[assignment[i]] = 1
            facilities[assignment[i]].rest -= customers[i].demand
    show()
    print(total(assignment))


# 模拟退火算法
def SA():
    global total_cost, assignment, customers
    T = 100000
    # for i in range(cnum):
    #     assignment[i] = -1
    # status[assignment[i]] = 1
    print(assignment)
    print(status)
    current = assignment
    _next = None
    good = 0
    while T > 0.001:
        no = 0
        print(T)
        T *= 0.95
        for i in range(1000):
            _next = generate(current)
            while not is_valid(_next):
                # print(is_valid(_next))
                _next = generate(current)
            dE = total(_next) - total(current)
            if dE < 0:
                no = 0
                good += 1
                current = _next
                if total(assignment) > total(current):
                    assignment = current
            else:
                rd = random.random()
                if math.exp(-dE / T) >= rd:
                    current = _next
                    if total(assignment) > total(current):
                        assignment = current
                else:
                    no += 1
            if no > 200:
                break
    # assignment = current
    total_cost = total(assignment)

    for i in range(cnum):
        status[assignment[i]] = 1
    print(total(assignment))
    show()

    print(good)

    print(assignment)

    print(is_valid(assignment))

    print(total(assignment))


for seq in range(71, 72):
    fnum = 0
    cnum = 0
    facilities = []
    customers = []
    total_cost = 0
    system = System()
    with open("E:\大学\大三上\算法设计与分析\项目\Instances\p" + str(seq), 'r') as f:
        print("p" + str(seq) + ":")
        line = f.readline().split()
        fnum = int(line[0])
        cnum = int(line[1])
        # print(fnum, cnum)
        for i in range(fnum):
            facilities.append(Facility())
            line = f.readline().split()
            facilities[i].capacity = int(line[0])
            facilities[i].opening_cost = int(line[1])
            facilities[i].rest = facilities[i].capacity
            # print(facilities[i].capacity, facilities[i].opening_cost, facilities[i].rest)
        newline = True
        for i in range(cnum):
            if newline:
                if seq < 56:
                    line = re.findall(r'\d+', f.readline())
                else:
                    line = re.findall(r'\d+', f.readline())
                newline = False
                j = 0
            customers.append(Customer())
            customers[i].demand = int(line[j])
            # print(len(line), j)
            j += 1
            if j >= len(line):
                newline = True
        for i in range(cnum * fnum):
            if newline:
                if seq < 56:
                    line = re.findall(r'\d+', f.readline())
                else:
                    line = re.findall(r'\d+', f.readline())
                newline = False
                j = 0
            customers[i // fnum].assign_cost.append(int(line[j]))
            j += 1
            if j >= len(line):
                newline = True

    status = [0] * fnum
    assignment = [-1] * cnum

    greed()
    # SA()
