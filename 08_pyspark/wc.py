#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from operator import add
from pyspark import SparkContext

if __name__ == '__main__':
	# sc = SparkContext("spark://cdh-232-renlj:7077", "wc")
	# sc = SparkContext("local[4]", "wc")
	sc = SparkContext("local", "wc")

	#lines = sc.textFile("hdfs://cdh-232-renlj:8020/tmp/head.log")
	lines = sc.textFile("wc.txt", 1)
	
	wc = lines.flatMap(lambda x: x.split(' ')) \
         .map(lambda x: (x, 1)) \
         .reduceByKey(add)

	for (word, count) in wc.collect():
		print "%s: %i" % (word, count)
