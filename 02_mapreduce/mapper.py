#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys

for line in sys.stdin:
	line = line.strip()
	words = line.split()
	for word in words:
		word = word.replace(',', '')
		print '%s\t%s' % (word, 1)
