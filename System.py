import random
import copy
import math


class System:
    def __init__(self, fnum, cnum):
        self.fnum = fnum  # 设备数量
        self.cnum = cnum  # 用户数量
        self.facilities = []
        self.status = [0] * self.fnum  # 工厂状态
        self.customers = []
        self.assignment = [0] * self.cnum  # 每个用户分配到哪个设备
        self.total_cost = 0  # 总成本
        self.best_assignment = [0] * self.cnum

    # 贪心算法
    def greed(self, status):
        facilities = copy.deepcopy(self.facilities)
        customers = copy.deepcopy(self.customers)
        total_cost = 0
        self.assignment = [-1] * self.cnum
        for i in range(self.fnum):  # 先计算开工厂的费用
            if status[i] == 1:
                total_cost += facilities[i].opening_cost
        for i in range(self.cnum):  # 为每个用户分配一个工厂
            min_cost = 999999999
            for j in range(self.fnum):  # 从已开的工厂中选择有足够剩余量、且费用最小的
                if status[j] == 1 and facilities[j].rest >= customers[i].demand:
                    cost = customers[i].assign_cost[j]
                    if cost < min_cost:
                        min_cost = cost
                        self.assignment[i] = j
            if self.assignment[i] != -1:  # 加上分配费用
                total_cost += min_cost
                facilities[self.assignment[i]].rest -= customers[i].demand
            else:  # 若没有工厂能容纳下，则无效
                return -1
                # for j in range(self.fnum):
                #     if status[j] == 0:
                #         self.assignment[i] = j
                #         status[j] = 1
                #         total_cost += facilities[j].opening_cost + self.customers[i].assign_cost[j]
                #         facilities[j].rest -= self.customers[i].demand
        self.status = status
        self.total_cost = total_cost
        return self.total_cost

    def show(self):
        print('result', self.total_cost)
        print('status', self.status)
        print('assignment:', self.assignment)

    # 模拟退火法
    def SA(self):
        # 设置初温
        T = 1000
        for i in range(self.cnum):
            self.assignment[i] = -1
        current = self.assignment
        _next = None
        # good = 0
        # 降温
        while T > 0.01:
            no = 0  # 记录连续多少次没有接收优解了
            # print(T)
            T *= 0.95
            # 内循环直至在该温度下稳定
            for i in range(1000):
                # 生成新解
                _next = self.generate(current)
                while not self.is_valid(_next):
                    _next = self.generate(current)
                dE = self.total(_next) - self.total(current)
                if dE < 0:  # 接收更优解
                    no = 0
                    # good += 1
                    current = _next
                    if self.total(self.assignment) > self.total(current):  # 记录到目前为止的最优解
                        self.assignment = current
                else:  # 以一定概率接受差解
                    no += 1
                    rd = random.random()
                    if math.exp(-dE / T) >= rd:
                        current = _next
                if no > 200:
                    break
        self.total_cost = self.total(self.assignment)
        for i in range(self.cnum):
            self.status[self.assignment[i]] = 1
        self.show()
        # print(good)

    # 通过领域操作生成新解
    def generate(self, current):
        customer_1 = random.randint(0, self.cnum - 1)
        customer_2 = random.randint(0, self.cnum - 1)
        _next = copy.deepcopy(current)
        while customer_2 == customer_1:
            customer_2 = random.randint(0, self.cnum - 1)
        method = random.randint(1, 4)
        if method == 1:  # 随机交换两个值
            _next[customer_1] = current[customer_2]
            _next[customer_2] = current[customer_1]
        elif method == 2:  # 随机改变两个值
            _next[customer_1] = random.randint(0, self.fnum - 1)
            _next[customer_2] = random.randint(0, self.fnum - 1)
        elif method == 3:  # 随机将某个值插到另一个位置
            if customer_1 < customer_2:
                for i in range(customer_1, customer_2):
                    _next[i] = current[i + 1]
                _next[customer_2] = current[customer_1]
            else:
                a = range(customer_2 + 1, customer_1 + 1)
                for i in reversed(a):
                    _next[i] = current[i - 1]
                _next[customer_2] = current[customer_1]
        elif method == 4:  # 倒置
            if customer_1 < customer_2:
                for i in range(customer_2 - customer_1):
                    _next[customer_1 + i] = current[customer_2 - i];
            else:
                for i in range(customer_1 - customer_2):
                    _next[customer_2 + i] = _next[customer_1 - i]
        # elif method == 5:  # 随机改变某一段的值
        #     if customer_1 < customer_2:
        #         for i in range(customer_2 - customer_1):
        #             _next[i] = random.randint(0, self.fnum - 1)
        #     else:
        #         for i in range(customer_1 - customer_2):
        #             _next[i] = random.randint(0, self.fnum - 1)
        return _next

    # 计算某分配的总成本
    def total(self, assignment):
        status = [0] * self.fnum
        for i in range(self.cnum):
            status[assignment[i]] = 1
        cost = 0
        for i in range(self.cnum):  # 计算总分配费用
            cost += self.customers[i].assign_cost[assignment[i]]
        for i in range(self.fnum):  # 计算开工厂的总费用
            if status[i] == 1:
                cost += self.facilities[i].opening_cost
        return cost

    # 判断一个分配序列是否有效
    def is_valid(self, assignment):
        if not isinstance(assignment, list):
            return False
        for i in range(self.fnum):  # 对所有工厂，计算对某工厂总需求量
            total_demand = 0
            for j in range(self.cnum):
                if assignment[j] == i:
                    total_demand += self.customers[j].demand
                    if total_demand > self.facilities[i].capacity:  # 若对某工厂的总需求超过总容量，则无效
                        return False
        return True
    
    # 模拟退火法2
    def SA2(self):
        min_cost = 99999999
        T = 10
        self.status = [1]*self.fnum
        # for i in range(self.fnum):
        #     self.status[i] = random.randint(0, 1)
        current = self.status
        greed_current = self.greed(current)
        _next = None
        good = 0
        while T > 0.1:
            no = 0  # 记录连续多少次没有接收优解了
            # print(T)
            T *= 0.95
            for i in range(12):
                # 生成新解
                _next = self.generate2(current)
                greed_next = self.greed(_next)
                while greed_next == -1:
                    _next = self.generate2(current)
                    greed_next = self.greed(_next)
                dE = greed_next - greed_current
                if dE < 0:  # 接收更优解
                    no = 0
                    good += 1
                    current = _next
                    greed_current = greed_next
                    if min_cost > greed_current:  # 记录到目前为止的最优解
                        min_cost = greed_current
                        self.best_assignment = self.assignment
                else:
                    no += 1
                    rd = random.random()
                    if math.exp(-dE / T) >= rd:
                        current = _next
                        greed_current = greed_next
                        if min_cost > greed_current:  # 记录到目前为止的最优解
                            min_cost = greed_current
                            self.best_assignment = self.assignment
                if no > 5:
                    break
        self.total_cost = min_cost
        self.assignment = self.best_assignment

        for i in range(self.cnum):
            j = self.assignment[i]
            self.status[j] = 1
        self.show()
        print(good)

    # 通过领域操作生成新解
    def generate2(self, current):
        facility_1 = random.randint(0, self.fnum - 1)
        facility_2 = random.randint(0, self.fnum - 1)
        _next = copy.deepcopy(current)
        while facility_1 == facility_2:
            facility_2 = random.randint(0, self.fnum - 1)
        method = random.randint(1, 4)
        if method == 1:  # 随机交换两个值
            _next[facility_1] = current[facility_2]
            _next[facility_2] = current[facility_1]
        elif method == 2:  # 随机翻转两个值
            _next[facility_1] = 1 - current[facility_1]
            _next[facility_2] = 1 - current[facility_2]
        elif method == 3:  # 随机将某个值插到另一个位置
            if facility_1 < facility_2:
                for i in range(facility_1, facility_2):
                    _next[i] = current[i + 1]
                _next[facility_2] = current[facility_1]
            else:
                a = range(facility_2 + 1, facility_1 + 1)
                for i in reversed(a):
                    _next[i] = current[i - 1]
                _next[facility_2] = current[facility_1]
        elif method == 4:  # 倒置
            if facility_1 < facility_2:
                for i in range(facility_2 - facility_1):
                    _next[facility_1 + i] = current[facility_2 - i];
            else:
                for i in range(facility_1 - facility_2):
                    _next[facility_2 + i] = _next[facility_1 - i]
        # elif method == 5:  # 随机改变某一段的值
        #     if customer_1 < customer_2:
        #         for i in range(customer_2 - customer_1):
        #             _next[i] = random.randint(0, self.fnum - 1)
        #     else:
        #         for i in range(customer_1 - customer_2):
        #             _next[i] = random.randint(0, self.fnum - 1)
        return _next



class Facility:
    def __init__(self):
        self.capacity = 0  # 总容量
        self.opening_cost = 0  # 开启成本
        self.rest = 0  # 剩余容量


class Customer:
    def __init__(self):
        self.demand = 0  # 需求量
        self.assign_cost = []  # 某设备分派给用户的成本