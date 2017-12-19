#!/usr/bin/python

import re
from Expert import *

##############################
############ MAIN ############
##############################

e = Expert('data')

# if (len(e.queries) <= 0):
# 	print "Missing Queries"
# 	exit(1)

e.printAll()

print e.facts

for i in e.facts:
	e.elem[i].setStatus()

for i in e.elem:
	print e.elem[i].printInfoInLine()

for i in e.elem:
	if e.elem[i].getName()[0] != "!" and i in e.queries:
		print e.elem[i].getName() + " = " + str(e.elem[i].getStatus())
