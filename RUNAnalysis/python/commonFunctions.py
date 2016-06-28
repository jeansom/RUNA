#!/usr/bin/env python

import sys,os,time, re
from math import *
from string import *
from array import array
from ROOT import * 
import numpy as np

##### Support functions
def checkLumi( Run, Lumi, NumEvent):
	"""docstring for checkLumi"""
	result = False
	allEvents = 'Run: '+str(Run)+' LumiSection: '+str(Lumi)+' Event: '+str(NumEvent)
	with open('boostedEventsRPV100tojj.txt') as f:
		lines = f.readlines()
		for i in lines: 
			if allEvents == i: result = True

	return result

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin()
	return idx

def getTree(filename, treename):
	hfile = TFile(filename)
	if not hfile.IsOpen():
		print "** can't open file %s" % filename
		sys.exit()
	tree = hfile.Get(treename)
	if tree == None:
		print "** can't find tree %s" % treename
		sys.exit()
	entries = tree.GetEntriesFast()
	return (hfile, tree, entries)

boostedMassAveBins = array( 'd', [ 0, 3, 6, 9, 12, 16, 19, 23, 26, 30, 34, 39, 43, 47, 52, 57, 62, 67, 72, 78, 83, 89, 95, 102, 108, 115, 122, 129, 137, 144, 153, 161, 170, 179, 188, 197, 207, 218, 228, 240, 251, 263, 275, 288, 301, 315, 329, 344, 359, 375, 391, 408, 425, 443, 462, 482, 502 ] )
boostedMassAveBinSize = array( 'd', [ 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 19, 19, 20, 21] )
