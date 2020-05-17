# coding=utf-8
import turtle

def listsum(numList):
    if len(numList) == 0:
        return 0

    if len(numList) == 1:
        return numList[0]

    res = numList[0] + listsum(numList[1:])

    return res


def baseConverter(num,base=2):
    convert_string = "0123456789ABCDEF"
    res = num // base
    yu = convert_string[num % base]

    if res == 0:
        return yu
    else:
        return baseConverter(res,base)+yu   # 字符串连接，不是加法运算

# 或者可以写成
# def baseConverter(num,base=2):
    # convert_string = "0123456789ABCDEF"
    
    # if n < base:
        # return convert_string[n]
    # else:
        # return baseConverter(n//base,base) + convert_string[n%base]

def tree(t,length):   # t为turtle对象，length为主干的长度
    if length >= 5:     # 绘制的分支最小长度为5
        t.forward(length)
        t.right(20)
        tree(t,length - 5)   # 绘制右分支
        t.left(40)
        tree(t,length - 5)     # 绘制左分支
        t.right(20)             # 角度调回来
        t.backward(length)      # 退回起点

def moveTower(height,fromPole,withPole,toPole):    # 移动最底部的那个甜甜圈之上的甜甜圈塔
    if height >= 1:
        moveTower(height - 1, fromPole,toPole,withPole)
        moveDisk(height, fromPole, toPole)
        moveTower(height - 1, withPole,fromPole,toPole)

def moveDisk(disk,fromPole,toPole):  # 移动最底部的甜甜圈
    print("Moving disk[%s] from {%s} to {%s}" % (str(disk),fromPole,toPole))


def returnCoins(change,coinList=[1,2,5,10,20,50]):   # change是要找的钱,按人民币来说，change应该小于100;coinList是货币面值
    coin = coinList.pop()

    res = change // coin
    yu = change % coin

    if yu == 0:     # 说明要找的钱刚好是某货币的面值
        return res
    else:
        # print(coinList)
        return res + returnCoins(yu, coinList)

def returnCoins2(change,coinList=[1,2,5,10,20,50],knownResult=[]):
    minCount = change       # 记录所有面值中，找回的最少的张数
    rightCoin = 1           # 记录所有面值中，找回的最少张数的那个面值

    for coin in coinList:
        if coin in knownResult or change < coin:
            continue

        count = change // coin
        nextChange = change % coin

        if count < minCount:
            minCount = count    # 记录minCount的目的是为了找到对应的rightCoin
            rightCoin = coin

    # 此时已经筛选出张数最少的那种币值
    if nextChange:      # 如果还没找完则递归
        knownResult.append(rightCoin)
        return [rightCoin] * count + returnCoins2(nextChange,coinList,knownResult)
    else:
        return [rightCoin] * count

def dfReturnCoins(change,coinList=[1,2,5,10,20,50]):
    storeList = [0] * (change+1)        # 存放最优解的容器，其中找的钱为x的最优解放在storeList[x]中，storeList[0]不存放任何钱的最优解而用于计算1块钱的最优解而设置的

    # 计算change的最优解就要先计算1~change-1这些找钱的最优解，最后也将change的最优解放在表中
    for money in range(1,change+1):
        minCount = money        # 设定初始最优解，初始最优解是全部用1块的解

        for coin in [c for c in coinList if c<=money]:
            if storeList[money-coin] + 1 <= minCount:   # 如果money对某一币值的最优解（即money-某一币值的钱的最优解+1，这个1是指coin这张纸币）小于当前最优解，则更新当前最优解
                minCount = storeList[money-coin] + 1

        # 记录下money的最优解
        storeList[money] = minCount
    print(storeList)
    return storeList[change]


# 博物馆大盗问题的动态规划算法
# 该函数返回最优解的宝藏item
def stealTreasure(capacity,treasureDict):   # 小偷背包的容量和宝物清单
    storeList = [{"value":0,"item":[]}]

    for c in range(1,capacity+1):
        maxValue = 0
        maxValueItems = []
        limitDict = {item:info for item,info in treasureDict.items() if info["weight"] <= c}
        for item,treasure in limitDict.items():
            nowMaxValue = storeList[c - treasure["weight"]]["value"] + treasure["value"]
            if nowMaxValue >= maxValue:
                maxValue = nowMaxValue
                maxValueItems = storeList[c - treasure["weight"]]["item"] + [item]

        c_dict = {"value":maxValue,"item":maxValueItems}
        storeList.append(c_dict)

    return storeList[capacity]


# 博物馆大盗问题的递归解法(该算法的性能远远低于动态规划算法)
# 该函数返回最优解的宝藏item
def stealTreasure2(capacity,treasureDict,zeroDict):   # 小偷背包的容量和宝物清单
    maxValueDict = zeroDict
    treasureDict = {item:info for item,info in treasureDict.items() if info["weight"] <= capacity}     # 只挑选重量小于背包剩余容量的宝物
    
    if not len(treasureDict.keys()):    # 递归结束条件
        return zeroDict

    for item,info in treasureDict.items(): 
        resDict1 = {'value':0,"items":[]}
        resDict1['items'].append(item)
        resDict1['value'] += info["value"]
        leftCapacity = capacity - info["weight"]
        resDict1 = combineDict(resDict1,stealTreasure2(leftCapacity,treasureDict,zeroDict))
        
        if resDict1['value'] > maxValueDict['value']:
            maxValueDict = resDict1
    
    return maxValueDict

def combineDict(dict1,dict2):
    final_resDict = {"value":0,"items":[]}
    final_resDict['value'] = dict1['value']+dict2['value']
    final_resDict['items'] = dict1['items']+dict2['items']

    return final_resDict

if __name__ == "__main__":
    capacity = 20
    treasureDict = {
        "1":{"weight":2,"value":3},
        "2":{"weight":3,"value":4},
        "3":{"weight":4,"value":8},
        "4":{"weight":5,"value":8},
        "5":{"weight":9,"value":10},
    }
    print(stealTreasure2(20,treasureDict,{'value':0,"items":[]}))
    print(stealTreasure(20,treasureDict))