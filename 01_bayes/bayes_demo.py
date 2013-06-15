#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pprint import pprint

def calc_bayes_prob(good, bad):
	"""计算贝叶斯概率
	"""
	prob = {}

	# 所有的key
	keys = []
	good_keys = good.keys()
	bad_keys = bad.keys()
	keys.extend(good_keys)
	keys.extend(bad_keys)

	keys = list(set(keys))				# 去重

	good_sum = sum(good.values())
	bad_sum = sum(bad.values())

	for k in keys:
		prob[k] = {}
		if k in good:
			good_prob = good[k]/float(good_sum)
		else:
			good_prob = 0.01 # 没有就是非常低，非常低就取0.0001(万分之一)
		if k in bad:
			bad_prob = bad[k]/float(bad_sum)
		else:
			bad_prob = 0.01

		prob[k]["good_prob"] = good_prob
		prob[k]["bad_prob"] = bad_prob
		prob[k]["prob"] = bad_prob/(good_prob+bad_prob)

	return prob

def calc_union_prob(prob_dict, words):
	"""计算给定概率列表的联合概率
	"""
	# prob["fa"] = 

	# 复合概率公式
	#                          P1*P2*P3*...*Pn
	# P = -----------------------------------------------------------
	#       (P1*P2*P3*...*Pn + (1-P1)*(1-P2)*(1-P3)*...*(1-Pn))

	# mutil_prob: P1*P2*P3*...*Pn
	# onesub_muti_prob: (1-P1)*(1-P2)*(1-P3)*...*(1-Pn)

	mutil_prob = 1
	onesub_muti_prob = 1
	for w in words:
		prob = prob_dict[w]["prob"]
		print "[%s] [%s]" % (w, prob, )
		mutil_prob *= prob
		onesub_muti_prob *= (1-prob)

	attack_probability = mutil_prob/(mutil_prob + onesub_muti_prob)

	return attack_probability


def display_prob(good, bad, prob):
	"""打印进度信息
	"""
	print '*'*120
	print "Good Dict: ",
	pprint(good)
	print "Bad Dict:  ",
	pprint(bad)
	print "Prob Dict: "
	pprint(prob)

def self_taught(good, bad, words, probability):
	"""自学的代码
	"""
	if probability > 0.9:
		for w in words:
			bad[w] = bad.get(w, 0) + 1
	else:
		for w in words:
			good[w] = good.get(w, 0) + 1

	return good, bad


def display_evolution(good, bad, words):
	"""显示自学的过程
	"""
	prob = calc_bayes_prob(good, bad)
	display_prob(good, bad, prob)
	print "详细信息:"

	for w in words:
		if w not in prob:
			prob[w] = {}
			prob[w]["prob"] = 0.4
	
	probability = calc_union_prob(prob, words)
	good, bad = self_taught(good, bad, words, probability)

	return good, bad, probability
	

if __name__ == '__main__':
	good = {}
	bad = {}

	# 好词： 老师 大师
	good["lao"] = 1						# 老
	good["shi"] = 2						# 师
	good["da"] = 1						# 大

	# 坏的： 苍老师
	bad["cang"] = 1						# 苍
	bad["lao"] = 1						# 老
	bad["shi"] = 1						# 师


	# 老 师
	words = ["lao", "shi"]
	good, bad, probability = display_evolution(good, bad, words)
	print "老 师[1]", probability

	# 校 长
	words = ["xiao", "zhang"]
	good, bad, probability = display_evolution(good, bad, words)
	print "校 长", probability

	# 老 师2
	words = ["lao", "shi"]
	good, bad, probability = display_evolution(good, bad, words)
	print "老 师[2]", probability

	# 大牌老师
	words = ["da", "pai", "lao", "shi"]
	good, bad, probability = display_evolution(good, bad, words)
	print "大 牌 老 师", probability

	# 知道创宇
	words = ["zhi", "dao", "chuang", "yu"]
	good, bad, probability = display_evolution(good, bad, words)
	print "知 道 创 宇", probability

	# 知道创宇苍老师
	words = ["zhi", "dao", "chuang", "yu", "lao", "shi", "cang"]
	good, bad, probability = display_evolution(good, bad, words)
	print "知 道 创 宇 苍 老 师", probability

    # 大师
	words = ["da", "shi"]
	good, bad, probability = display_evolution(good, bad, words)
	print "大 师", probability
