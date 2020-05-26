# 单向队列（列表实现，unshift头部添加复杂度O(n),pop尾部弹出复杂度O(1)）
class ListQueue:
    def __init__(self,aList = []):
        self.queue = aList

    def getSize(self):
        return len(self.queue)

    def unshift(self,item):
        self.queue.insert(0,item)

    def pop(self):
        return self.queue.pop() if self.getSize() else None

    def isEmpty(self):
        return self.getSize() == 0


# 双向队列（列表实现，push O(n), pop O(1), unshift O(n), shift O(1)）
class DoubleListQueue:
    def __init__(self):
        self.items=[]

    def getSize(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []

    # 首部添加
    def unshift(self,item):
        self.items.insert(0,item)

    # 尾部添加
    def push(self,item):
        self.items.append(item)

    # 首部弹出
    def shift(self):
        return self.items.pop(0)

    # 尾部弹出
    def pop(self):
        return self.items.pop()


from .LinkedList import Node,DoubleLinkedList

# 改良单向队列(双向链表实现，unshift和pop都是O(1))
class LinkedListQueue(DoubleLinkedList):
    def __init__(self, aList=[]):
        super(LinkedListQueue, self).__init__()
        self.init(aList)

    def init(self,aList):
        for index in range(len(aList)):
            self.unshift(index,index)

    def unshift(self,item):
        super(LinkedListQueue, self).unshift(item,item)

    def pop(self):
        return super(LinkedListQueue, self).pop()

    def shift(self):
        raise Exception("Method shift is forbidden in class LinkedListQueue ！")

    def push(self,item):
        raise Exception("Method push is forbidden in class LinkedListQueue ！")

    def get(self):
        raise Exception("Method get is forbidden in class LinkedListQueue ！")

# 改良双向队列(双向链表实现，unshift，shift，push和pop都是O(1)）
class DoubleLinkedListQueue(DoubleLinkedList):
    def __init__(self, aList=[]):
        super(DoubleLinkedListQueue, self).__init__()
        self.init(aList)

    def init(self,aList):
        for index in range(len(aList)):
            self.unshift(index,index)

    def unshift(self,item):
        super(DoubleLinkedListQueue, self).unshift(item,item)

    def pop(self):
        return super(DoubleLinkedListQueue, self).pop()

    def shift(self):
        return super(DoubleLinkedListQueue, self).shift()

    def push(self,item):
        super(DoubleLinkedListQueue, self).push(item,item)

    def get(self,item):
        raise Exception("Method get is forbidden in class LinkedListQueue ！")