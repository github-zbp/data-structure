# coding=utf8
import random

class Queue:
    def __init__(self,items=[]):
        self.items = items

    def enqueue(self,item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items==[]


# 应用1：热土豆问题（约瑟夫问题）
def hotPotato(players,k):
    queue = Queue(players)
    i = 1

    while queue.size()>1:
        if i==k:
            queue.dequeue()
            i=1
        else:
            queue.enqueue(queue.dequeue())
            i+=1

    return queue.dequeue()

# 或者也可以这样写
def hotPotato2(players,k):
    queue = Queue(players)

    while queue.size() > 1:
        for i in range(k-1):
            queue.enqueue(queue.dequeue())
        queue.dequeue()

    return queue.dequeue()
print(hotPotato2(list("ABCDEF"),7))


# 应用2：打印任务
class Printer:
    def __init__(self,speed=5):   # speed速度，整数 5 or 10 （每分钟打印5 or 10页）
        self.speed = speed
        self.currentTask = None     # 保存任务对象，当任务对象不为空
        self.spending = 0   # 记录本次打印需要花多少时间

    def busy(self):
        if self.currentTask:
            return True
        else:
            return False

    def tick(self):     # 打印1秒钟
        # 每打印1秒钟，本次打印需要花的时间就-1
        if self.currentTask :
            if self.spending>0:
                self.spending-=1
            else:
                # 如果所需打印时间为0说明本次打印完成
                self.currentTask = None

    def recTask(self,task):      # 接任务
        self.currentTask = task
        self._calculSpending()

    def _calculSpending(self):   # 计算本次打印所需时间
        # 60/self.speed是每页需要打印的时间
        self.spending = self.currentTask.pages * 60/self.speed

class Task:
    def __init__(self,time):
        self.pages = random.randint(1,20)

        # 该时间用于计算任务等待的总时间（入队列的时间到出队列的时间）
        self.st = time      # 任务开始的时间，其实是放入队列的时间而不是计算机开始打印本次任务的时间

    def calculWaitTime(self,time):
        return time - self.st

    @classmethod
    def createTask(cls):
        randNum = random.randint(1,180)
        if randNum == 180:
            return True
        else:
            return False


# 模拟打印
def simulate(totalTimes,speed):
    printer = Printer(speed)    # 打印机
    queue = Queue()             # 任务队列
    wait_times = []             # 存储每次打印任务的等待时间，即入队列到出队列的时长，不含打印时间（因为每人打印的页数不同，如果加入了打印时间就会不公平）

    for currentSec in range(totalTimes):
        # 每秒都有1/180的几率生成1个任务，如果生成了任务就往队列里面添加
        if Task.createTask():
            task = Task(currentSec)
            queue.enqueue(task)

        # 如果打印机不忙碌，每秒打印机都会尝试从队列取任务
        if not printer.busy() and not queue.isEmpty():
            ready_task = queue.dequeue()
            # print(ready_task.st,i)
            wait_times.append(ready_task.calculWaitTime(currentSec))
            printer.recTask(ready_task)   # 打印机接收从队列弹出的任务

        printer.tick()  # 执行打印，每秒执行一次tick()

    # 执行到这里，3600s已经过去了，计算平均等待的时间
    avg_time = sum(wait_times)/len(wait_times)

    # 可能3600s完了之后，还有些任务没开始打印，原因是它们在3600s末期才开始入列
    remain_task_num = queue.size()


    return avg_time,remain_task_num


for x in range(20):     # 进行10次试验
    print(simulate(3600,5))