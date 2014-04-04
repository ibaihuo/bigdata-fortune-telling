大数据算命系列（8）
===================

spark框架与pyspark简介
~~~~~~~~~~~~~~~~~~~~~~

     -----  大数据算命师

     -----  2014.04.4

----------------------------------------------------------------------

==========
Spark简介
==========

链接：http://spark.incubator.apache.org/

1. AMPlab实验室
#. 快速迭代（可使用内存），适合机器学习
#. 用scala语言写，提供三种api（scala, java, python)
#. dpark(豆瓣)
#. mllib：机器学习

  1. classification
  #. clustering
  #. recommentdation
  #. resgression
  #. linlg

----------------------------------------------------------------------

====
部署
====

链接：http://spark.incubator.apache.org/docs/latest/cluster-overview.html

1. local： 可以当成多进程
2. standalone: 本身自带的集群（方便推广）
3. mesos
4. yarn
5. EC2

监控界面：http://10.8.0.232:8081/

----------------------------------------------------------------------

=========================
localhost与standalone部署
=========================

1. 下载0.9.0版本
#. 编译：bin/sbt assembly (可能需要很长时间，视网络情况)
#. 目录build下面的是不依赖于scala语言的，复制到其它有java环境的机器的/opt/spark
#. 将/opt/spark同步到集群中的所有机器的/opt/spark目录
#. 配置conf下的：
  
  1. master: cdh-232-renlj
  #. slavers:

    cdh-231-lux
    cdh-232-renlj
    cdh-233-liujh
    cdh-234-yang
#. sbin/start-all.sh

----------------------------------------------------------------------

========
由此开始
========

1. spark交互环境

  spark-shell

#. pyspark交互环境

  pyspark

#. ipython notebook
  IPYTHON=1 pyspark(前提：安装ipython)

  IPYTHON_OPTS="notebook --pylab inline" ./pyspark(前提：ipython notebook能用)

#. 两个概念(sc与rdd)
  1. sc: SparkContext，Spark上下文环境

    sc = SparkContext("local", "app-name")

  #. rdd: 弹性分布式数据集，主要处理的对象

    rdd = sc.textFile("head.log")

----------------------------------------------------------------------

===============
例子：wordcount
===============

1. 三种运行方式
  1. 本机单cpu（"local", 文件在本机）
  2. 本机多cpu（"local[4]", 文件在本机）
  3. 集群多cpu（"spark://cdh-232-renlj:7077", 需要文件能每个机器都能访问）
#. 注意：如果脚本要import自己的库，或者依赖于数据文件，需要使用pyFile将文件分发到其它机器：

import kw,hacktoo, vuleye     # vuleye.py依赖数据文件data.json
sc = SparkContext("spark://cdh-232-renlj:7077", "gac.data", pyFiles=['data.json', 'kw.py', 'hacktool.py', 'vuleye.py'])


.. code-block:: python

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

----------------------------------------------------------------------

======================
transformation与action
======================

链接：http://spark.apache.org/docs/latest/api/pyspark/index.html

1. transformation: 变形(从一种形式的rdd到另外的rdd)
  1. filter()：       过滤
  #. reduceByKey()：  按key进行合并
  #. groupByKey()：   聚合
  #. combineByKey():  能将两个元素合并成一个不同类型的元素
  #. ...

2. action: 行动(通常是得出结论)
  1. first():  返回rdd里面第一个值
  #. take(n):  从rdd里面取出前n个
  #. collect():  返回全部的rdd元素
  #. sum():   求和
  #. count():  求个数
  3. ...

----------------------------------------------------------------------

============
机器学习例子
============

1. 注意
  0. 依赖numpy
  #. mllib从spark 0.8版本才引入，现在完全不完善
  #. scala的接口比python的接口要多些，比如linlg

#. from pyspark.mllib.clustering import KMeans
#. 返回中心

----------------------------------------------------------------------

======
SparkR
======

链接： https://github.com/amplab-extras/SparkR-pkg

例子：

.. code-block:: python

   sc <- sparkR.init("local")
   lines <- textFile(sc, "hdfs://cdh-232-renlj:8020/tmp/head.log")
   wordsPerLine <- lapply(lines, function(line) { length(unlist(strsplit(line, " "))) })

----------------------------------------------------------------------

===============
mesos及框架应用
===============

链接：http://mesos.apache.org/documentation/latest/mesos-frameworks/

1. dpark
2. hadoop
3. spark
4. storm
5. cassandra
6. elastic search

----------------------------------------------------------------------

==========
生态及其它
==========

0. 主要用户
  1. tweeter/amblab
  #. taobao/douban

1. AMPlab 的野心（https://amplab.cs.berkeley.edu/software/）
  1. BDAS: Berkeley Data Analytics Stack
  #. mesos:  集群资源管理器(提供三个接口：C++, java, python, 可以写应用)       类似于：yarn   
  #. Tachyon：  内存文件系统      类似于：hadoop:  hdfs文件系统
  #. Spark：    弹性分布式计算    类似于：hadoop map-reduce
  #. shark:   离线数据仓库        类似于：hive
  #. mlbase:   机器学习
  #. GraphX：   图计算(pagerank)
  #. Spark Streaming:            类似于hadoop Streaming
   
  #. 个人的感觉：pyspark:   python数据分析api，   类似于：pig
   
----------------------------------------------------------------------

========
 Thanks
========
