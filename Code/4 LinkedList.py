# coding=utf8

class Node:
    def __init__(self,value):
        self.value = value      # 节点值
        self.next = None        # 节点向后指针

    def getData(self):
        return self.value

    def setData(self,value):
        self.value = value

    def getNext(self):
        return self.next

    def setNext(self,next):
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None    # 首部标记

    def size(self):
        # 需要遍历这个链表
        current = self.head
        size = 0
        while current:
            current = current.next
            size += 1

        return size

    def add(self,item):      # 往首部加入
        node = Node(item)

        if self.head:
            node.setNext(self.head)

        self.head = node

    def pop(self):
        previous = None
        current = self.head

        while True:
            if current.getNext() is None:
                if current == self.head:
                    self.head = None
                else:
                    previous.setNext(None)
                return current.getData()
            else:
                previous = current
                current = current.getNext()

    def search(self,item):
        current = self.head

        while current:
            if current.getData() == item:
                return True
            else:
                current = current.getNext()

        return False

    def remove(self,item,n=1):      # n表示可以删除n个值为item的节点
        current = self.head
        previous = None
        num = 0

        while current and num<n:
            if current.getData() == item:
                if current == self.head:
                    self.head = current.getNext()
                else:
                    previous.setNext(current.getNext())
                num += 1

            previous = current
            current = current.getNext()

    def isEmpty(self):
        return self.head is None    # 判断是否有首部节点即可

    def __str__(self):
        current = self.head
        cont = ""

        while current:
            cont += str(current.getData()) + "->"
            current = current.getNext()

        return cont.strip("->")

class OrderList(LinkedList):
    def add(self,item):
        current = self.head
        previous = None

        while current:
            if current.getData() > item:    # 如果遍历到数据项大于item的位置就可以停下来执行插入了
                break

            previous = current
            current = current.getNext()

        node = Node(item)
        if previous is None:    # 说明要插入的节点的值是比链表中的值都小，要插入链表的头部
            node.setNext(self.head)
            self.head = node
        else:
            previous.setNext(node)
            node.setNext(current)

    def search(self,item):
        current = self.head

        while current:
            if current.getData() == item:
                return True
            elif current.getData() > item:
                break

            current = current.getNext()

        return False

if __name__ == "__main__":
    orderlist = OrderList()
    orderlist.add(10)
    orderlist.add(5)
    orderlist.add(100)
    orderlist.add(55)
    orderlist.add(22)

    print(orderlist.search(10))
    print(orderlist.search(56))
    print(orderlist)

    print(orderlist.pop())
    print(orderlist.remove(11))
    print(orderlist.remove(10))
    print(orderlist)