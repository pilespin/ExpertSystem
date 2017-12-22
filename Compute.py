#!/usr/bin/python

import re
from Element import Element

class Compute(object):

	def __init__(self):
		pass

	def computeQueries(self, allElem, elem):
		if self.getElement(elem).getBeginComputed() == True:
			print "Loop Detected with: " + elem
			exit(10)
		self.getElement(elem).setBeginComputed()
		rules1 = self.getElement(elem).getRules()
		self.computeNaturalRule(elem, rules1)
		if ("!" + elem in allElem):
			rules2 = self.getElement("!" + elem).getRules()
			self.computeNaturalRule("!" + elem, rules2)
			if self.getElement("!" + elem).getStatus() == True:
				self.getElement(elem).setStatus(False)
		self.getElement(elem).setBeginComputed(False)

			# if ret1 == True and ret2 == True:
			# 	print "Conflict with element " + elem
			# 	exit(7)

	def computeNaturalRule(self, elem, rules):
		for i in rules:
			ret = self.computeSimpleNaturalRule(elem, i)
			if ret == True:
				self.getElement(elem).setStatus()
				self.getElement(elem).setComputed()

	def computeSimpleNaturalRule(self, elem, rule):
		ret = self.splitLogicOperator(rule)

		if len(ret) == 1:
			A = self.getElement(ret[0])
			if (A.getComputed() == False):
				self.computeQueries(self._elem, A.getName())
			ret = A.getStatus(ret[0])
		elif len(ret) >= 3:
			ret = self.parseLongRule(rule)
		else:
			A, operator, B = self.parseSimpleRule(rule)
			ret = self.compute(A, operator, B)
		return ret

	def parseLongRule(self, rule):
		elm = self.splitLogicOperator(rule)
		opr = re.findall(self.regexOperator, rule)

		if (len(elm) <= 1 and len(opr) <= 0 and len(opr) != len(elm) - 1):
			print "Error when parsing: " + rule
			exit(7)

		A = self.getElement(elm[0], negative=False)
		if (A.getComputed() == False):
				self.computeQueries(self._elem, A.getName())

		ret = self.getElement(elm[0], negative=False).getStatus(elm[0])
		for i in range(len(opr)):

			cur = elm[i]
			nxt = elm[i+1]

			B = self.getElement(nxt, negative=False)
			if (B.getComputed() == False):
				self.computeQueries(self._elem, B.getName())

			ret = self.compute(ret, opr[i], B.getStatus(nxt))
		
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
		A = self.getElement(ret[0], negative=False)
		B = self.getElement(ret[1], negative=False)
		if (A.getComputed() == False):
			self.computeQueries(self._elem, A.getName())
		if (B.getComputed() == False):
			self.computeQueries(self._elem, B.getName())
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
			if A == False and B == True:
				return True
			else:
				return False
		else:
			print "Operator not found"
			exit(4)
