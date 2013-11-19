大数据算命系列(5)
=================

数据仓库hive技术
~~~~~~~~~~~~~~~~

  ----- 大数据算命师

  ----- 2013.09.12

--------------------------------------------------------------------------------

数据仓库
~~~~~~~~

1. 来源于facebook
2. 类型于sql语句（工业界非常熟悉）
#. 数据存储在hdfs中（依赖hadoop）
#. 调用hadoop的MapReduce来执行
#. 数据库与数据仓库
   
   1. 柜台与货仓
   #. 漂亮的MM -> UI
   #. 柜台 -> 数据库（低延时，小于1秒）
   #. 货仓 -> 数据仓库（高延时，高于1分）

.. code-block:: sh

   $ dse hadoop fs -ls /user/hive/warehouse
   $ dse hadoop fs -put log.log /usr/hive/warehouse/tmp/

--------------------------------------------------------------------------------

访问接口
~~~~~~~~

命令行接口（cli）
+++++++++++++++++

.. code-block:: sh

   dse hive
   dse hive -f select.sql
   dse hive -S -f select.sql
   dse hive -e 'use logs; show tables;'


jobtracker(web ui)
++++++++++++++++++


1. 查看当前任务队列
#. 查看失败详细原因
#. 其它细节

--------------------------------------------------------------------------------

创建表
~~~~~~

1. 数据与元数据
#. 内部表与外部表
#. 分区与分桶
#. 字段分隔符
#. CTAS(Create Table As Select)
#. 示例

.. code-block:: sql

   PARTITIONED BY (zz string, yy string, xx string)
   ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '
   create external table xxoo1(oo1 string, oo2 string) ... LOCATION /xxoo/
   use logs;
   show tables;
   show partitions table;
   create table xxoo
   as 
   select oo1, oo2 from xxyy where oo1 > 100;

--------------------------------------------------------------------------------

数据导入/导出
~~~~~~~~~~~~~

导入数据
++++++++

1. load data local inpath '/data/tmp/log.log' overwrite into table xxoo;
#. insert overwrite table ... select from
#. 外部表，建立对应关系，添加分区

导出数据
++++++++

1. 导出到

   1. hdfs
   #. hive表
   #. Linux文件系统(insert overwrite local directory '/data/tmp/xxoolog' select ...)

#. 处理导出的分隔符\001

.. code-block:: she

   sed: cat 000000_0 | sed 's/\x1/ /g' > file.log
   awk: awk -F'\001' '{print $1, $2}' 000000_0 > file.log
   awk: awk 'BEGIN{FS="\001";OFS=" ";}{$1=$1;print $0}'

--------------------------------------------------------------------------------

Hive-QL
~~~~~~~

语法继承于MySQL, 或者非常类似

导出来源于baidu news的新闻TOP100, 按次数进行降序排列

.. code-block:: sql
   
   from logs.ncsa_2013
   insert overwrite local directory '/data/tmp/new_host'
   select host, count(1) as times
   where logdate='2013-07-21' and referer like '%news.baidu.com%' 
   group by host
   distributed by host
   order by times desc
   limit 100;

1. 先from表
2. 再insert导出
#. 再select查询
#. 再where条件(分区列是合法的列， DSE(BUG): and 1=1)
#. 再group by
#. 再order by
#. 再limit

--------------------------------------------------------------------------------

模糊与正则匹配
~~~~~~~~~~~~~~

1. like模糊

   1. %匹配多个字符
   2. _匹配一个字符
   3. 不匹配为：not like

#. regexp查询
   
   1. escape: \\
   2. hive -e '\\.php'  

.. code-block:: sql

   from logs.ncsa_2013
   insert overwrite local directory '/data/tmp/404_month8'
   select *
   where month(logdate)='08' and resp_code='404' 
      and req_uri regexp '.*\.(php|asp|aspx|asa|jsp)$';

--------------------------------------------------------------------------------

其它特性
~~~~~~~~

1. 多表插入
#. 索引
#. 内嵌Map-Reduce逻辑
#. 读时模式（对比写时模式）
#. 不支持修改表，如果修改后，必须导出到新表

多表插入

.. code-block:: sql

   from attack_access
      insert overwrite table os
        select 
           transform(user_agent) 
           using 'awk -f os.awk'
        as (osdate, ostype, oscount)

      insert overwrite table browser
        select 
           transform(user_agent) 
           using 'awk -f browser.awk'
        as (brdate, brtype, brcount)

--------------------------------------------------------------------------------

外部脚本
~~~~~~~~

1. 建表

.. code-block:: sql

   create table if not exists os(
      osdate string,
      ostype string,
      oscount bigint)
   ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ' ';

#. 添加外部脚本

.. code-block:: sql

   add file /data/joy/os.awk;

#. 执行脚本并插入结果到表

.. code-block:: sql

   insert into table os
   select 
	 transform(user_agent) 
	 using 'awk -f os.awk'
	 as (osdate, ostype, oscount)
   from attack_access;

--------------------------------------------------------------------------------

聚合查询
~~~~~~~~

1. 相关语句
  
   1. group by
   2. order/sort/distributed/clustered by
   
#. 相关聚合函数

   1. sum/min/max
   #. count/distinct

#. 示例（统计每个ip，在一天中访问的网站数目）

.. code-block:: sql

   from logs.ncsa_2013
   insert overwrite local directory '/data/tmp/ip_site_times'
   select client_ip, count(distinct host) as sites
   where logdate='2013-08-01'
   group by client_ip
   sort by sites desc;

--------------------------------------------------------------------------------

mapjoin查询
~~~~~~~~~~~

1. 语句(C注释风格)

.. code-block:: sql

   use logs;
   insert overwrite local directory '/data/tmp/scan_logs'
   select /*+ mapjoin(a) */  b.* from tmp_iplist a join ncsa_2013 b 
      on (a.ip=b.client_ip)
   where logdate='2013-08-01';

#. 适用场景

   1. 一大一小表join, 小表在1000行以下，大表在1亿以上
   2. 不等值join(on a.length > b.length)
   3. 从一个月的日志中，导出列表里面的ip（ip数目小于1000个）的所有访问日志

--------------------------------------------------------------------------------


Thanks
~~~~~~
