#!/usr/bin/env python
#-*- coding:utf-8 -*-
######################################################################
## Filename:	  adaboost.py
##				  
## Copyright (C) 2014,	renewjoy
## Version:		  
## Author:		  renewjoy <oyea9le@gmail.com>
## Created at:	  Sun Mar 23 12:12:07 2014
##				  
## Modified by:	  renewjoy <oyea9le@gmail.com>
## Modified at:	  Sun Mar 23 13:56:26 2014
## Description:	  
##				  
######################################################################

import numpy as np

from stump_classify import build_stump, stump_classify

def load_data_set(file_name):
	"""
	general function to parse tab -delimited floats
	"""

	num_feat = len(open(file_name).readline().split()) # get number of fields 
	data_mat = []
	label_mat = []
	
	fr = open(file_name)
	for line in fr.readlines():
		line_arr =[]
		cur_line = line.strip().split()

		for i in range(num_feat-1):
			line_arr.append(float(cur_line[i]))

		data_mat.append(line_arr)

		label_mat.append(float(cur_line[-1]))

	return data_mat, label_mat

def ada_boost_train_DS(data_arr, class_labels, num_it=40):
	"""
	DS: Decision Stump: 单层决策树
	"""
	weak_class_arr = []
	m = np.shape(data_arr)[0]
	D = np.mat(np.ones((m, 1))/m)	  # init D to all equal
	agg_class_est = np.mat(np.zeros((m, 1)))

	for i in range(num_it):
		best_stump, error, class_est = build_stump(data_arr, class_labels, D) # build Stump

		# print "D:", D.T
		alpha = float(0.5*np.log((1.0-error)/max(error, 1e-16))) # calc alpha, throw in max(error, eps) to account for error=0

		best_stump['alpha'] = alpha	 
		weak_class_arr.append(best_stump) # store Stump Params in Array

		# print "class_est: ", class_est.T
		expon = np.multiply(-1*alpha*np.mat(class_labels).T, class_est) # exponent for D calc, getting messy
		D = np.multiply(D, np.exp(expon))	   # Calc New D for next iteration
		D = D/D.sum()

		# calc training error of all classifiers, if this is 0 quit for loop early (use break)
		agg_class_est += alpha*class_est
		# print "agg_class_est: ", agg_class_est.T
		agg_errors = np.multiply(np.sign(agg_class_est) != np.mat(class_labels).T, np.ones((m, 1)))
		error_rate = agg_errors.sum()/m
		print "total error: ", error_rate

		if error_rate == 0.0:
			break

	return weak_class_arr, agg_class_est

def ada_classify(dat_to_class, classifier_arr):

	data_matrix = np.mat(dat_to_class) # do stuff similar to last agg_class_est in ada_boost_train_DS
	m = np.shape(data_matrix)[0]
	agg_class_est = np.mat(np.zeros((m, 1)))

	for i in range(len(classifier_arr)):
		class_est = stump_classify(data_matrix, classifier_arr[i]['dim'], \
								   classifier_arr[i]['thresh'], \
								   classifier_arr[i]['ineq']) # call stump classify

		agg_class_est += classifier_arr[i]['alpha']*class_est

		print agg_class_est

	return np.sign(agg_class_est)

if __name__ == '__main__':
	dat_arr, label_arr = load_data_set('horseColicTraining2.txt')
	classifier_array = ada_boost_train_DS(dat_arr, label_arr, 50)
	print classifier_array


	# test_arr, test_labels = load_data_set('horseColicTest2.txt')
	# prediction10 = ada_classify(test_arr, classifier_array)
	# print prediction10
