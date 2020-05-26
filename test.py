# coding=utf-8

from Structure.Queue import DoubleLinkedListQueue,LinkedListQueue
from Structure.LinkedList import OrderList

def isSymmetry(words):
    queue = DoubleLinkedListQueue()

    for word in words:
        print(word)
        queue.unshift(word)

    while queue.getSize() > 1:
        left = queue.shift().getValue()
        right = queue.pop().getValue()
        if left != right:
            return False

    return True

if __name__ == "__main__":
    order_list = OrderList()
    order_list.push(5)
    order_list.push(6)
    order_list.push(12)
    order_list.push(2)
    order_list.push(55)
    order_list.push(16)
    order_list.push(17)
    order_list.push(32)
    order_list.push(2)

    print(order_list)

    order_list.shift()
    order_list.shift()
    order_list.push(20)
    order_list.push(2)
    print(order_list)

    print(order_list.search(16))
    print(order_list.search(18))
