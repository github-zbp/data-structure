# 栈
class Stack:
    def __init__(self):
        self.items=[]

    def pop(self):
        return self.items.pop()

    def push(self,item):
        self.items.append(item)

    # 查看栈顶的元素
    def peak(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items==[]