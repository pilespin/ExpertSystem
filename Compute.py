#!/usr/bin/python

import re
from Element import *


class Compute(object):

	def __init__(self):
		pass

	def compute(self, A, operator, B):
		if operator == '+':
			if A == True and B == True:
				return True
			else:
				return False
		if operator == '|':
			if A == True or B == True:
				return True
			else:
				return False
		if operator == '^':
			if A == True and B == False:
				return (True)
			if A == True and B == False:
				return True
			else:
				return False
		else:
			print "Operator not found"
			exit(4)
