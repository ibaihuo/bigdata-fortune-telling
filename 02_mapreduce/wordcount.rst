我们以wordcount为例，假设有个6400M的文件，100台hadoop机器（准确地说应该是tasktracker机），默认block大小为64M，这样每台执行map的文件刚好是一个64M的block文件（假设这个分发过程已经完成，同时忽略备份数之类的细节），并且我们使用10个reduce任务来归并文件。Hadoop的mapreducer的执行过程如下：

这100台机器上面的map都是并发、独立的执行，以wordcount为例，步骤如下：

1、  每个map任务使用默认的textinputformat类的LineRecordReader方法按行读取文件，这个读取的行数据就被交给map函数去执行，wordcount的map做的就是提取里面的单词，并以单词为key，1为value作为输出，格式为：<word integer（1）>。

2、  如果有combine，先对第一步的输出结果就行combine操作。Combine就是个小reduce操作，作用就是对某个map自己的输出结果先进行一次归并，把相同word的计数累加，这样假设某个map输出结果做如果有50%的重复word，那combine后的中间结果大小可以减少一半，可减少后续的patition、copy、sort等的开销，提高性能。

3、  每个map对自己的输出文件进行patition操作。上面提到有10个reducer任务，那默认的patition操作就是对map的输出kay进行hash，并对10求余（hash(key)），并提供10个文件（内存足够的话可以是链表等内存数据结构），假设是r1、r2….r10这10个文件，把不同key的放到不同的文件，这次操作就可以把相同key聚合到同一个文件。由于算法一样，保证了每个map的输出结果经过这个操作后，相同key的肯定在同一个聚合文件里，比如某个单词word肯定都在r1文件里。

4、  接下来就是copy文件的过程了，10个reducer任务各自从所有map机器上取到属于自己的文件，比如reducer1会从100台map机器上取到所有r1文件，reducer2取所有r2的文件，这样同一类word已经到了同一台reducer机器上了。

5、  每个reducer合并（meger）自己取到的文件，reducer1就是合并100个r1文件（实际过程是在上面第4步操作中会边copy边meger，在内存中）。

6、  合并好后进行下sort（排序）操作，再次把不同小文件中的同一个单词聚合在一起。作为提供给reduce操作的数据。

7、  进行reduce操作，对同一个单词的value列表再次进行累加，最终得到某个单词的词频数。

8、  Outputformat操作，把reduce结果写到磁盘。

所以，总的流程应该是这样的：

* Inputformat ====> map ====>（combine）====> partition ====> copy&merge ====> sort ====> reduce ====> outputformat

由此我们也可以看出，执行reduce的代价还是有些的，所以如果我们的应用只使用map就能搞定的话，那就尽量不要再有reduce操作在其中。
