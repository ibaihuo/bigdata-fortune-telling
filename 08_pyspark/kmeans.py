#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans
from numpy import array
from math import sqrt

sc = SparkContext("local", "kmeans")
data = sc.textFile("kmeans.txt")

parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))

clusters = KMeans.train(parsedData, 10, maxIterations=50,
		runs=30, initializationMode="random")

print '类中心:'
print clusters.centers

class_all = {}

# # Evaluate clustering by computing Within Set Sum of Squared Errors
# def error(point):
# 	center = clusters.centers[clusters.predict(point)]
# 	print point, clusters.predict(point)
# 	return sqrt(sum([x**2 for x in (point - center)]))

# WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
# print("Within Set Sum of Squared Error = " + str(WSSSE))

def class_id(item):
	classid = clusters.predict(item)
	return classid, item

# def concat_list(a, b):
# 	return [a, b]
#allclass = parsedData.map(lambda item: class_id(item)).reduceByKey(lambda a, b: concat_list(a, b))

allclass = parsedData.map(lambda item: class_id(item)).groupByKey()

for classid, value in allclass.collect():
	print classid
	for item in value:
		print item,
	print
