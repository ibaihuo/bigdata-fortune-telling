大数据算命系列(6)
=================

hadoop之hdfs技术
~~~~~~~~~~~~~~~~

  ----- 大数据算命师

  ----- 2013.09.24

--------------------------------------------------------------------------------

hadoop简介
~~~~~~~~~~


1. 背景

   1. google发布的论文
   2. yahoo!的开源实现
#. 功能

   1. 分布式文件存储系统(hdfs: Hadoop Distributed File System )
   2. 分布式并行计算框架(MapReduce)
#. API
   
   1. java编程接口
   #. streaming接口（加载任意可执行脚本）

--------------------------------------------------------------------------------

设计的目的
~~~~~~~~~~

1. NoSQL(Not Only SQL)
#. 低廉的硬件(Low-Cost)，集群是堆出来的
#. 方便横向扩展
#. 假定机器经常坏-> 高可用性
#. 简单一致性模型：一次性写，多次读
#. 解决两个问题（存储与计算）

--------------------------------------------------------------------------------

环境部署
~~~~~~~~

1. 单机模式（用于调试）
#. 伪分布式（用于调试）
#. 集群环境（完全分布式）

#. java环境

   1. oracle jdk (1.6或者1.7)， not openjdk

#. 机器之间无密码登录(证书登录)

--------------------------------------------------------------------------------

基本角色
~~~~~~~~

1. Master

   1. NameNode (元数据服务器)
   #. Secondary NameNode (辅助元数据服务器)

   #. 文件系统的目录信息，各个文件的分块信息，数据块的位置信息，并且管理各个数据服务器
   #. 会有单点故障

#. slave

   1. DataNodes(数据块存储)
   #. 分块与副本（查看：通过es的head插件来直观了解）

#. 作业控制

   1. JobTracker (任务调度员)： 50030
   #. Tasktracker(任务执行)： 50060
   #. speculative task(推测式任务)： 以空间换时间，同时启动多个相同的task，哪个完成的早使用哪个的结果（查看：Killed tasks）

#. client端
   
   1. 客户端连接（断开也无所谓）

--------------------------------------------------------------------------------

启动与进程
~~~~~~~~~~

1. 启动与关闭

.. code-block:: sh

   启动：$ start-all.sh
   关闭：$ stop-all.sh

#. 在master节点上，使用jps查看当前启动的进程，应该会有如下进程

.. code-block:: sh

   $ jps
   23344 Jps
   27808 NameNode
   32558 jar
   28329 TaskTracker
   27940 DataNode
   28177 JobTracker
   28076 SecondaryNameNode

#. 在slave节点上，使用jps查看当前启动的进程，应该会有如下进程

.. code-block:: sh

  $ jps
  28336 DataNode
  28448 TaskTracker
  6581 Jps

--------------------------------------------------------------------------------

作业管理
~~~~~~~~

1. job（作业）
#. task（任务，作业分出来的小任务）
#. kill掉job/task

   1. hadoop job -kill job_201301221529_0349
   #. hadoop job -kill-task task_201307261245_2373_m_000000

--------------------------------------------------------------------------------

dfs基本操作
~~~~~~~~~~~

1. 列目录
.. code-block:: sh

   hadoop fs -ls /
   hadoop fs -ls /access
   dfs表示使用它的hdfs接口，-ls和Linux里面的ls一样，可以用hadoop dfs -help来查看所有命令，/表示hadoop的根文件系统，注意和Linux本身的文件系统进行区别。

#. 配合Linux管道与命令
.. code-block:: sh

   hadoop文件系统里的文件，只有使用hadoop相应的接口查看，无法自己去文件系统里面查看 。
   $ hadoop dfs -cat /logs/20120819/10.9.0.5_*/*.log.gz | gzip -d | less

#. 上传文件
.. code-block:: sh

   $ hadoop dfs -put 20121118.summary / # 将Linux文件系统中文件保存到Hadoop中的文件系统

#. 获取文件
.. code-block:: sh

   hadoop dfs -get /20121118.summary /tmp # 将hadoop文件系统中的文件保存到Linux文件系统中

#. 删除文件
.. code-block:: sh

   hadoop dfs -rm /20121118.summary

#. *删除目录*
.. code-block:: sh

   hadoop dfs -rm /directory_not_exists # 小心使用，会删除整个目录且不会提示


--------------------------------------------------------------------------------

hadoop生态圈
~~~~~~~~~~~~

1. hadoop是既是指hadoop本身，也指这个生态圈
#. hdfs
#. MapReduce
#. Pig：一种数据流语言和运行环境，用以检索非常大的数据集
#. hive: 数据仓库
#. hbase： 列式数据库
#. Mahout: 一个可扩展的机器学习和数据挖掘库
#. Sqoop: 在传统数据库和HDFS之间高效传输数据的工具
#. Cassandra: 列式数据库
#. Impala: 类似于hive的
#. hue:   基于web的hadoop交互(python+django开发)
   1. 可进行权限控制

--------------------------------------------------------------------------------

NoSQL的厂商
~~~~~~~~~~~

1. 去IOE
#. google
#. yahoo!
#. facebook
#. twitter
#. Amazon
#. cloudera
#. datastax
#. hortonwords (yahoo!投资)


--------------------------------------------------------------------------------

hadoop发行版本
~~~~~~~~~~~~~~

1. cloudera
#. hortonworks
#. mapr
#. dse

--------------------------------------------------------------------------------

Thanks
~~~~~~
