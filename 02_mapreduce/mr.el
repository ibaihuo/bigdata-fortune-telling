;;(map list-type function list-1 list-2 ... list-n)
;;list-type是列表的类型，可以是vector,string等等，这个不是重点
;;map函数接受一个函数和N个列表，该函数接受N个参数；返回一个列表。返回列表的每个元素都是使用输入的函数对N个类别中的每个元素处理的结果
(setq mapout
(map 'vector #'(lambda (x)
				 (* x x))
	 (list 1 8 9 20 3 9))
)

;;reduce让一个指定的函数(function)作用于列表的第一个元素和第二个元素,然后在作用于上步得到的结果和第三个元素，直到处理完列表中所有元素。
(reduce  #'+ mapout)

(vector 1 2 3)
[1 2 3]

(list 1 2 3)
(1 2 3)

(string 97 98 99)
"abc"

;; (map 'list #'* (list 1 2 3) (list 3 4 5) (list 2 2 2))
;; (reduce #'+ (list 1 2 3 4))
