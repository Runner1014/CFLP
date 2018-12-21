from System import System, Facility, Customer
import re
import time

result_table = open("E:\大学\大三上\算法设计与分析\项目\\result_table_SA.md", 'w')
detail = open("E:\大学\大三上\算法设计与分析\项目\\detail_SA.md", 'w')

result_table.write("""|      | Result | Time |
                | ---- | ------ | ---- |
                """)

for seq in range(1, 72):
    # 读取数据
    with open("E:\大学\大三上\算法设计与分析\项目\Instances\p" + str(seq), 'r') as f:
        print("p" + str(seq) + ":")
        line = f.readline().split()
        system = System(int(line[0]), int(line[1]))
        # print(fnum, cnum)
        for i in range(system.fnum):
            system.facilities.append(Facility())
            line = f.readline().split()
            system.facilities[i].capacity = int(line[0])
            system.facilities[i].opening_cost = int(line[1])
            system.facilities[i].rest = system.facilities[i].capacity
        newline = True
        for i in range(system.cnum):
            if newline:
                if seq < 56:
                    line = re.findall(r'\d+', f.readline())
                else:
                    line = re.findall(r'\d+', f.readline())
                newline = False
                j = 0
            system.customers.append(Customer())
            system.customers[i].demand = int(line[j])
            # print(len(line), j)
            j += 1
            if j >= len(line):
                newline = True
        for i in range(system.cnum * system.fnum):
            if newline:
                if seq < 56:
                    line = re.findall(r'\d+', f.readline())
                else:
                    line = re.findall(r'\d+', f.readline())
                newline = False
                j = 0
            system.customers[i // system.fnum].assign_cost.append(int(line[j]))
            j += 1
            if j >= len(line):
                newline = True

    start = time.process_time()  # 开始时间
    # 贪心算法
    # status = [1] * system.fnum
    # system.greed(status)
    # system.show()

    # 模拟退火法
    system.SA()

    # 贪心 + 模拟退火
    # system.SA2()

    # 写出结果到文件
    stop = time.process_time()
    cost_time = float("%.2f" % (stop - start))
    print(cost_time)
    result_table.write("|p" + str(seq) + "|" + str(system.total_cost) + "|" + str(time) + str(cost_time) + "|\n")
    detail.write('p' + str(seq) + ':\nResult: ' + str(system.total_cost) + '\nstatus: ' + str(system.status) + "\nassignment: " + str(system.assignment) + "\n")
result_table.close()
detail.close()

