#!/usr/bin/env python
#-*- coding:utf-8 -*-

#. 任务：求数组 [1, 8, 9, 20, 3, 9] 每个元素的平方和
ldemo = [1, 8, 9, 20, 3, 9]

def fun_map(l):
	"""映射，平方
	"""
	return (i**2 for i in l)

def fun_reduce(l):
	"""化约， 相加
	"""
	return sum(l)

def mapreduce():
	"""map-reduce程序演示
	"""
	mapout = fun_map(ldemo)
	reduceout = fun_reduce(mapout)

	return reduceout

res = mapreduce()
print res

ldemo = [1, 8, 9, 20, 3, 9]
gdemo = [1, 8, 9, 20, 3, 9]
# 真正的python版本
mapout = map(lambda x: x**2,  ldemo, gdemo)


reduceout = reduce(lambda x, y: x+y, mapout)
print type(mapout), type(reduceout), reduceout




# map的函数特性：
# 参数： 必须与后面的列表数相等
# 过程： 将列表里的参数，一个个按顺序传进去，进行处理
# 返回： 列表
# map(lambda x, y: x+y, l1, l2)

# reduce的函数特性：
# 参数： 只能2个
# 过程： 将列表里面的前两个参数传进去，返回值与第三个参数一起传进去，如此类推
# 返回： 一个值

# filter的函数特性：filter(function,sequence)
# 参数： 只能1个， function的返回值只能是True或False
# 过程： 把sequence中的值逐个当参数传给function，如果function(x)的返回值是True，就把x加到filter的返回值里面。
# 返回： 一般来说filter的返回值是list，特殊情况如sequence是string或tuple，则返回值按照sequence的类型
