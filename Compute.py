#!/usr/bin/python

import re
from Element import *


class Compute(object):

	def __init__(self):
		pass

	def computeQueries(self, allElem, elem):
		rules1 = self.getElement(elem).getRules()
		self.computeNaturalRule(elem, rules1)

		rules2 = None
		if ("!" + elem in allElem):
			# print "OPOSITE EXIST"
			rules2 = self.getElement("!" + elem).getRules()
			self.computeNaturalRule(elem, rules2)
			# if ret1 == True and ret2 == True:
			# 	print "Conflict with element " + elem
			# 	exit(7)

	def computeNaturalRule(self, elem, rules):
		for i in rules:
			ret = self.computeSimpleNaturalRule(i)
			# print ret
			if ret == True:
				self.getElement(elem).setStatus()
				self.getElement(elem).setComputed()
				return True
		return False

	def computeSimpleNaturalRule(self, rule):
		# print "Rule: " + rule
		ret = self.splitLogicOperator(rule)
		# print ret
		if len(ret) == 1:
			# print ret[0]	
			A = self.getElement(ret[0])
			if (self.getElement(A.getName()).getComputed() == False):
				self.computeQueries(self._elem, A.getName())
			ret = A.getStatus(ret[0])
			# ret = self.getElement(ret[0]).getStatus(ret[0])
			# print ret
		else:
			A, operator, B = self.parseSimpleRule(rule)
			print str(A) + " " + operator + " " + str(B)
			ret = self.compute(A, operator, B)
		return ret

	def parseSimpleRule(self, rule):
		ret = self.splitLogicOperator(rule)
		operator = re.findall(self.regexOperator, rule)
		if (len(operator) <= 0):
			print "Error when parsing: " + rule
			exit(1)
		operator = operator[0]
		if (len(ret) != 2 and operator is not None):
			print "Error when parsing: " + rule
			exit(1)
		A = self.getElement(ret[0])
		B = self.getElement(ret[1])
		# print A.getName()
		# print A.getStatus(ret[0])
		# print B.getName()
		# print B.getStatus(ret[1])
		if (self.getElement(A.getName()).getComputed() == False):
			self.computeQueries(self._elem, A.getName())
		if (self.getElement(B.getName()).getComputed() == False):
			self.computeQueries(self._elem, B.getName())
			# print A.getStatus(ret[0])
			# print B.getStatus(ret[1])
		return (A.getStatus(ret[0]), operator, B.getStatus(ret[1]))

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
