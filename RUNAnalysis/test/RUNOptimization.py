#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time
#import optparse
import argparse
#from collections import defaultdict
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2D, TMath
from array import array
from scaleFactors import scaleFactor as SF

gROOT.SetBatch()

def checkLumi( Run, Lumi, NumEvent):
	"""docstring for checkLumi"""
	result = False
	allEvents = 'Run: '+str(Run)+' LumiSection: '+str(Lumi)+' Event: '+str(NumEvent)
	with open('boostedEventsRPV100tojj.txt') as f:
		lines = f.readlines()
		for i in lines: 
			if allEvents == i: result = True

	return result

######################################
def calcOpt( sample, grooming):


	inputFile = TFile( sample, 'read' )


	###################################### Get GenTree 
	events = inputFile.Get( 'RUNATree'+grooming+'/RUNATree' )
	numEntries = events.GetEntriesFast()

	print '------> Number of events: '+str(numEntries)
	d = 0
	eventsPassed = 0
	eventsAfterTrigger = 0
	numMassAsym00 = numMassAsym01 = numMassAsym02 = numMassAsym03 = numMassAsym04 = numMassAsym05 = numMassAsym06 = numMassAsym07 = numMassAsym08 = numMassAsym09 = numMassAsym10 = 0
	numDeltaEta00 = numDeltaEta01 = numDeltaEta02 = numDeltaEta03 = numDeltaEta04 = numDeltaEta05 = numDeltaEta06 = numDeltaEta07 = numDeltaEta08 = numDeltaEta09 = numDeltaEta10 = 0
	numCosTheta00 = numCosTheta01 = numCosTheta02 = numCosTheta03 = numCosTheta04 = numCosTheta05 = numCosTheta06 = numCosTheta07 = numCosTheta08 = numCosTheta09 = numCosTheta10 = 0
	numJet1SubjetPtRatio00 = numJet1SubjetPtRatio01 = numJet1SubjetPtRatio02 = numJet1SubjetPtRatio03 = numJet1SubjetPtRatio04 = numJet1SubjetPtRatio05 = numJet1SubjetPtRatio06 = numJet1SubjetPtRatio07 = numJet1SubjetPtRatio08 = numJet1SubjetPtRatio09 = numJet1SubjetPtRatio10 = 0
	numJet2SubjetPtRatio00 = numJet2SubjetPtRatio01 = numJet2SubjetPtRatio02 = numJet2SubjetPtRatio03 = numJet2SubjetPtRatio04 = numJet2SubjetPtRatio05 = numJet2SubjetPtRatio06 = numJet2SubjetPtRatio07 = numJet2SubjetPtRatio08 = numJet2SubjetPtRatio09 = numJet2SubjetPtRatio10 = 0
	numSubjetPtRatio00 = numSubjetPtRatio01 = numSubjetPtRatio02 = numSubjetPtRatio03 = numSubjetPtRatio04 = numSubjetPtRatio05 = numSubjetPtRatio06 = numSubjetPtRatio07 = numSubjetPtRatio08 = numSubjetPtRatio09 = numSubjetPtRatio10 = 0
	numJet1Tau2100 = numJet1Tau2101 = numJet1Tau2102 = numJet1Tau2103 = numJet1Tau2104 = numJet1Tau2105 = numJet1Tau2106 = numJet1Tau2107 = numJet1Tau2108 = numJet1Tau2109 = numJet1Tau2110 = 0
	numJet1Tau3100 = numJet1Tau3101 = numJet1Tau3102 = numJet1Tau3103 = numJet1Tau3104 = numJet1Tau3105 = numJet1Tau3106 = numJet1Tau3107 = numJet1Tau3108 = numJet1Tau3109 = numJet1Tau3110 = 0
	numJet2Tau2100 = numJet2Tau2101 = numJet2Tau2102 = numJet2Tau2103 = numJet2Tau2104 = numJet2Tau2105 = numJet2Tau2106 = numJet2Tau2107 = numJet2Tau2108 = numJet2Tau2109 = numJet2Tau2110 = 0
	numJet2Tau3100 = numJet2Tau3101 = numJet2Tau3102 = numJet2Tau3103 = numJet2Tau3104 = numJet2Tau3105 = numJet2Tau3106 = numJet2Tau3107 = numJet2Tau3108 = numJet2Tau3109 = numJet2Tau3110 = 0

	newSF = SF(sample)*1000
	for i in xrange(numEntries):
		events.GetEntry(i)

		#---- progress of the reading --------
		fraction = 10.*i/(1.*numEntries)
		if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		d = TMath.FloorNint(fraction)
		#if i > 1000: break

		#---- progress of the reading --------
		Run      = events.run
		Lumi     = events.lumi
		NumEvent = events.event
		if 'RPV' in sample:
			if checkLumi( Run, Lumi, NumEvent): continue

		HT		= events.HT
		trimmedMass	= events.trimmedMass
		numJets		= events.numJets
		massAve		= events.massAve
		massAsym	= events.massAsym
		cosThetaStar	= events.cosThetaStar
		jet1SubjetPtRatio	= events.jet1SubjetPtRatio
		jet2SubjetPtRatio	= events.jet2SubjetPtRatio
#		#scale		= events.scale
#		numPV           = events.numPV
#		AK4HT           = events.AK4HT
#		jet1Pt          = events.jet1Pt
		jet1Eta         = events.jet1Eta
#		jet1Phi         = events.jet1Phi
#		jet1E           = events.jet1E
#		jet1Mass        = events.jet1Mass
#		jet2Pt          = events.jet2Pt
		jet2Eta         = events.jet2Eta
#		jet2Phi         = events.jet2Phi
#		jet2E           = events.jet2E
#		jet2Mass        = events.jet2Mass
#		subjet11Pt      = events.subjet11Pt
#		subjet11Eta     = events.subjet11Eta
#		subjet11Phi     = events.subjet11Phi
#		subjet11E       = events.subjet11E
#		subjet12Pt      = events.subjet12Pt
#		subjet12Eta     = events.subjet12Eta
#		subjet12Phi     = events.subjet12Phi
#		subjet12E       = events.subjet12E
#		subjet21Pt      = events.subjet21Pt
#		subjet21Eta     = events.subjet21Eta
#		subjet21Phi     = events.subjet21Phi
#		subjet21E       = events.subjet21E
#		subjet22Pt      = events.subjet22Pt
#		subjet22Eta     = events.subjet22Eta
#		subjet22Phi     = events.subjet22Phi
#		subjet22E       = events.subjet22E
		jet1Tau21       = events.jet1Tau21
		jet1Tau31       = events.jet1Tau31
		jet2Tau21       = events.jet2Tau21
		jet2Tau31       = events.jet2Tau31
#		jet1Tau32       = events.jet1Tau32
#		cosPhi13412     = events.cosPhi13412
#		cosPhi31234     = events.cosPhi31234

		#### TEST
		deltaEtaDijet = abs( jet1Eta - jet2Eta )

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )
		dijetCut = ( numJets > 1 )   
		subjetPtRatio = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		massAsymCut = ( massAsym < 0.1 ) 
		cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		subjetPtRatioCut = ( subjetPtRatio ) 

		if triggerCut and dijetCut and massAsymCut and cosThetaStarCut and subjetPtRatioCut: eventsPassed +=1

		##### For Optimization:
		eventsAfterTrigger +=1

		if dijetCut and ( massAsym <= 0.0 ): numMassAsym00 += 1
		if dijetCut and ( massAsym <= 0.1 ): numMassAsym01 += 1
		if dijetCut and ( massAsym <= 0.2 ): numMassAsym02 += 1
		if dijetCut and ( massAsym <= 0.3 ): numMassAsym03 += 1
		if dijetCut and ( massAsym <= 0.4 ): numMassAsym04 += 1
		if dijetCut and ( massAsym <= 0.5 ): numMassAsym05 += 1
		if dijetCut and ( massAsym <= 0.6 ): numMassAsym06 += 1
		if dijetCut and ( massAsym <= 0.7 ): numMassAsym07 += 1
		if dijetCut and ( massAsym <= 0.8 ): numMassAsym08 += 1
		if dijetCut and ( massAsym <= 0.9 ): numMassAsym09 += 1
		if dijetCut and ( massAsym <= 1.0 ): numMassAsym10 += 1

		if dijetCut and ( deltaEtaDijet <= 0.0 ): numDeltaEta00 += 1
		if dijetCut and ( deltaEtaDijet <= 0.5 ): numDeltaEta01 += 1
		if dijetCut and ( deltaEtaDijet <= 1.0 ): numDeltaEta02 += 1
		if dijetCut and ( deltaEtaDijet <= 1.5 ): numDeltaEta03 += 1
		if dijetCut and ( deltaEtaDijet <= 2.0 ): numDeltaEta04 += 1
		if dijetCut and ( deltaEtaDijet <= 2.5 ): numDeltaEta05 += 1
		if dijetCut and ( deltaEtaDijet <= 3.0 ): numDeltaEta06 += 1
		if dijetCut and ( deltaEtaDijet <= 3.5 ): numDeltaEta07 += 1
		if dijetCut and ( deltaEtaDijet <= 4.0 ): numDeltaEta08 += 1
		if dijetCut and ( deltaEtaDijet <= 4.5 ): numDeltaEta09 += 1
		if dijetCut and ( deltaEtaDijet <= 5.0 ): numDeltaEta10 += 1


		if dijetCut and ( cosThetaStar <= 0.0 ): numCosTheta00 += 1
		if dijetCut and ( cosThetaStar <= 0.1 ): numCosTheta01 += 1
		if dijetCut and ( cosThetaStar <= 0.2 ): numCosTheta02 += 1
		if dijetCut and ( cosThetaStar <= 0.3 ): numCosTheta03 += 1
		if dijetCut and ( cosThetaStar <= 0.4 ): numCosTheta04 += 1
		if dijetCut and ( cosThetaStar <= 0.5 ): numCosTheta05 += 1
		if dijetCut and ( cosThetaStar <= 0.6 ): numCosTheta06 += 1
		if dijetCut and ( cosThetaStar <= 0.7 ): numCosTheta07 += 1
		if dijetCut and ( cosThetaStar <= 0.8 ): numCosTheta08 += 1
		if dijetCut and ( cosThetaStar <= 0.9 ): numCosTheta09 += 1
		if dijetCut and ( cosThetaStar <= 1.0 ): numCosTheta10 += 1

		if dijetCut and ( jet1SubjetPtRatio >= 0.0 ): numJet1SubjetPtRatio00 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.1 ): numJet1SubjetPtRatio01 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.2 ): numJet1SubjetPtRatio02 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.3 ): numJet1SubjetPtRatio03 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.4 ): numJet1SubjetPtRatio04 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.5 ): numJet1SubjetPtRatio05 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.6 ): numJet1SubjetPtRatio06 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.7 ): numJet1SubjetPtRatio07 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.8 ): numJet1SubjetPtRatio08 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.9 ): numJet1SubjetPtRatio09 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 1.0 ): numJet1SubjetPtRatio10 += 1

		if dijetCut and ( jet2SubjetPtRatio >= 0.0 ): numJet2SubjetPtRatio00 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.1 ): numJet2SubjetPtRatio01 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.2 ): numJet2SubjetPtRatio02 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.3 ): numJet2SubjetPtRatio03 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.4 ): numJet2SubjetPtRatio04 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.5 ): numJet2SubjetPtRatio05 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.6 ): numJet2SubjetPtRatio06 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.7 ): numJet2SubjetPtRatio07 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.8 ): numJet2SubjetPtRatio08 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 0.9 ): numJet2SubjetPtRatio09 += 1
		if dijetCut and ( jet2SubjetPtRatio >= 1.0 ): numJet2SubjetPtRatio10 += 1

		if dijetCut and ( jet1SubjetPtRatio >= 0.0 ) and ( jet2SubjetPtRatio >= 0.0 ): numSubjetPtRatio00 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.1 ) and ( jet2SubjetPtRatio >= 0.1 ): numSubjetPtRatio01 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.2 ) and ( jet2SubjetPtRatio >= 0.2 ): numSubjetPtRatio02 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.3 ) and ( jet2SubjetPtRatio >= 0.3 ): numSubjetPtRatio03 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.4 ) and ( jet2SubjetPtRatio >= 0.4 ): numSubjetPtRatio04 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.5 ) and ( jet2SubjetPtRatio >= 0.5 ): numSubjetPtRatio05 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.6 ) and ( jet2SubjetPtRatio >= 0.6 ): numSubjetPtRatio06 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.7 ) and ( jet2SubjetPtRatio >= 0.7 ): numSubjetPtRatio07 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.8 ) and ( jet2SubjetPtRatio >= 0.8 ): numSubjetPtRatio08 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 0.9 ) and ( jet2SubjetPtRatio >= 0.9 ): numSubjetPtRatio09 += 1
		if dijetCut and ( jet1SubjetPtRatio >= 1.0 ) and ( jet2SubjetPtRatio >= 1.0 ): numSubjetPtRatio10 += 1

		if dijetCut and ( jet1Tau21 <= 0.0 ): numJet1Tau2100 += 1
		if dijetCut and ( jet1Tau21 <= 0.1 ): numJet1Tau2101 += 1
		if dijetCut and ( jet1Tau21 <= 0.2 ): numJet1Tau2102 += 1
		if dijetCut and ( jet1Tau21 <= 0.3 ): numJet1Tau2103 += 1
		if dijetCut and ( jet1Tau21 <= 0.4 ): numJet1Tau2104 += 1
		if dijetCut and ( jet1Tau21 <= 0.5 ): numJet1Tau2105 += 1
		if dijetCut and ( jet1Tau21 <= 0.6 ): numJet1Tau2106 += 1
		if dijetCut and ( jet1Tau21 <= 0.7 ): numJet1Tau2107 += 1
		if dijetCut and ( jet1Tau21 <= 0.8 ): numJet1Tau2108 += 1
		if dijetCut and ( jet1Tau21 <= 0.9 ): numJet1Tau2109 += 1
		if dijetCut and ( jet1Tau21 <= 1.0 ): numJet1Tau2110 += 1

		if dijetCut and ( jet1Tau31 <= 0.0 ): numJet1Tau3100 += 1
		if dijetCut and ( jet1Tau31 <= 0.1 ): numJet1Tau3101 += 1
		if dijetCut and ( jet1Tau31 <= 0.2 ): numJet1Tau3102 += 1
		if dijetCut and ( jet1Tau31 <= 0.3 ): numJet1Tau3103 += 1
		if dijetCut and ( jet1Tau31 <= 0.4 ): numJet1Tau3104 += 1
		if dijetCut and ( jet1Tau31 <= 0.5 ): numJet1Tau3105 += 1
		if dijetCut and ( jet1Tau31 <= 0.6 ): numJet1Tau3106 += 1
		if dijetCut and ( jet1Tau31 <= 0.7 ): numJet1Tau3107 += 1
		if dijetCut and ( jet1Tau31 <= 0.8 ): numJet1Tau3108 += 1
		if dijetCut and ( jet1Tau31 <= 0.9 ): numJet1Tau3109 += 1
		if dijetCut and ( jet1Tau31 <= 1.0 ): numJet1Tau3110 += 1

		if dijetCut and ( jet2Tau21 <= 0.0 ): numJet2Tau2100 += 1
		if dijetCut and ( jet2Tau21 <= 0.1 ): numJet2Tau2101 += 1
		if dijetCut and ( jet2Tau21 <= 0.2 ): numJet2Tau2102 += 1
		if dijetCut and ( jet2Tau21 <= 0.3 ): numJet2Tau2103 += 1
		if dijetCut and ( jet2Tau21 <= 0.4 ): numJet2Tau2104 += 1
		if dijetCut and ( jet2Tau21 <= 0.5 ): numJet2Tau2105 += 1
		if dijetCut and ( jet2Tau21 <= 0.6 ): numJet2Tau2106 += 1
		if dijetCut and ( jet2Tau21 <= 0.7 ): numJet2Tau2107 += 1
		if dijetCut and ( jet2Tau21 <= 0.8 ): numJet2Tau2108 += 1
		if dijetCut and ( jet2Tau21 <= 0.9 ): numJet2Tau2109 += 1
		if dijetCut and ( jet2Tau21 <= 1.0 ): numJet2Tau2110 += 1

		if dijetCut and ( jet2Tau31 <= 0.0 ): numJet2Tau3100 += 1
		if dijetCut and ( jet2Tau31 <= 0.1 ): numJet2Tau3101 += 1
		if dijetCut and ( jet2Tau31 <= 0.2 ): numJet2Tau3102 += 1
		if dijetCut and ( jet2Tau31 <= 0.3 ): numJet2Tau3103 += 1
		if dijetCut and ( jet2Tau31 <= 0.4 ): numJet2Tau3104 += 1
		if dijetCut and ( jet2Tau31 <= 0.5 ): numJet2Tau3105 += 1
		if dijetCut and ( jet2Tau31 <= 0.6 ): numJet2Tau3106 += 1
		if dijetCut and ( jet2Tau31 <= 0.7 ): numJet2Tau3107 += 1
		if dijetCut and ( jet2Tau31 <= 0.8 ): numJet2Tau3108 += 1
		if dijetCut and ( jet2Tau31 <= 0.9 ): numJet2Tau3109 += 1
		if dijetCut and ( jet2Tau31 <= 1.0 ): numJet2Tau3110 += 1


	tmpTotalMassAsym = [ numMassAsym00, numMassAsym01, numMassAsym02, numMassAsym03, numMassAsym04, numMassAsym05, numMassAsym06, numMassAsym07, numMassAsym08, numMassAsym09, numMassAsym10 ]
	totalMassAsym = [ x * newSF for x in tmpTotalMassAsym  ] 
	
	tmpTotalDeltaEta = [ numDeltaEta00, numDeltaEta01, numDeltaEta02, numDeltaEta03, numDeltaEta04, numDeltaEta05, numDeltaEta06, numDeltaEta07, numDeltaEta08, numDeltaEta09, numDeltaEta10 ]
	totalDeltaEta = [ x * newSF for x in tmpTotalDeltaEta  ] 
	
	tmpTotalCosTheta = [ numCosTheta00, numCosTheta01, numCosTheta02, numCosTheta03, numCosTheta04, numCosTheta05, numCosTheta06, numCosTheta07, numCosTheta08, numCosTheta09, numCosTheta10 ]
	totalCosTheta = [ x * newSF for x in tmpTotalCosTheta  ] 
	
	tmpTotalJet1SubjetPtRatio = [ numJet1SubjetPtRatio00, numJet1SubjetPtRatio01, numJet1SubjetPtRatio02, numJet1SubjetPtRatio03, numJet1SubjetPtRatio04, numJet1SubjetPtRatio05, numJet1SubjetPtRatio06, numJet1SubjetPtRatio07, numJet1SubjetPtRatio08, numJet1SubjetPtRatio09, numJet1SubjetPtRatio10 ]
	totalJet1SubjetPtRatio = [ x * newSF for x in tmpTotalJet1SubjetPtRatio  ] 

	tmpTotalJet2SubjetPtRatio = [ numJet2SubjetPtRatio00, numJet2SubjetPtRatio01, numJet2SubjetPtRatio02, numJet2SubjetPtRatio03, numJet2SubjetPtRatio04, numJet2SubjetPtRatio05, numJet2SubjetPtRatio06, numJet2SubjetPtRatio07, numJet2SubjetPtRatio08, numJet2SubjetPtRatio09, numJet2SubjetPtRatio10 ]
	totalJet2SubjetPtRatio = [ x * newSF for x in tmpTotalJet2SubjetPtRatio  ] 

	tmpTotalSubjetPtRatio = [ numSubjetPtRatio00, numSubjetPtRatio01, numSubjetPtRatio02, numSubjetPtRatio03, numSubjetPtRatio04, numSubjetPtRatio05, numSubjetPtRatio06, numSubjetPtRatio07, numSubjetPtRatio08, numSubjetPtRatio09, numSubjetPtRatio10 ]
	totalSubjetPtRatio = [ x * newSF for x in tmpTotalSubjetPtRatio  ] 

	tmpTotalJet1Tau21 = [ numJet1Tau2100, numJet1Tau2101, numJet1Tau2102, numJet1Tau2103, numJet1Tau2104, numJet1Tau2105, numJet1Tau2106, numJet1Tau2107, numJet1Tau2108, numJet1Tau2109, numJet1Tau2110 ]
	totalJet1Tau21 = [ x * newSF for x in tmpTotalJet1Tau21  ] 

	tmpTotalJet1Tau31 = [ numJet1Tau3100, numJet1Tau3101, numJet1Tau3102, numJet1Tau3103, numJet1Tau3104, numJet1Tau3105, numJet1Tau3106, numJet1Tau3107, numJet1Tau3108, numJet1Tau3109, numJet1Tau3110 ]
	totalJet1Tau31 = [ x * newSF for x in tmpTotalJet1Tau31  ] 

	tmpTotalJet2Tau21 = [ numJet2Tau2100, numJet2Tau2101, numJet2Tau2102, numJet2Tau2103, numJet2Tau2104, numJet2Tau2105, numJet2Tau2106, numJet2Tau2107, numJet2Tau2108, numJet2Tau2109, numJet2Tau2110 ]
	totalJet2Tau21 = [ x * newSF for x in tmpTotalJet2Tau21  ] 

	tmpTotalJet2Tau31 = [ numJet2Tau3100, numJet2Tau3101, numJet2Tau3102, numJet2Tau3103, numJet2Tau3104, numJet2Tau3105, numJet2Tau3106, numJet2Tau3107, numJet2Tau3108, numJet2Tau3109, numJet2Tau3110 ]
	totalJet2Tau31 = [ x * newSF for x in tmpTotalJet2Tau31  ] 

	TOTAL1  = [ totalMassAsym, totalCosTheta, totalSubjetPtRatio, totalDeltaEta, totalJet1SubjetPtRatio, totalJet2SubjetPtRatio, totalJet1Tau21, totalJet1Tau31, totalJet2Tau21, totalJet2Tau31  ]
	print 'massAsym', totalMassAsym
	print 'deltaEta', totalDeltaEta
	print 'cosThetaStar', totalCosTheta
	print 'jet1SubjetPtRatio', totalJet1SubjetPtRatio
	print 'jet2SubjetPtRatio', totalJet2SubjetPtRatio
	print 'subjetPtRatio', totalSubjetPtRatio
	print 'events after trigger', eventsAfterTrigger, 'events that pass selection', eventsPassed

	return TOTAL1


def optimization( mass, PU, grooming, outputFileName ):
	"""docstring for optimization"""

	inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15DR74_'+PU+'_v02p2_v06.root'
	signalTotal = calcOpt( inputFileName, grooming )
	sys.exit(0)
	signalMassAsym = signalTotal[0]
	signalCosTheta = signalTotal[1]
	signalSubjetPtRatio = signalTotal[2]
	signalDeltaEta = signalTotal[3]
	signalJet1SubjetPtRatio = signalTotal[4]
	signalJet2SubjetPtRatio = signalTotal[5]
	signalJet1Tau21 = signalTotal[6]
	signalJet1Tau31 = signalTotal[7]
	signalJet2Tau21 = signalTotal[8]
	signalJet2Tau31 = signalTotal[9]

	qcdDict = {}
	for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800' ]: 
		inputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15DR74_'+PU+'_v01_v06.root'
		qcdDict[ qcdBin ] = calcOpt( inputFileName, grooming )

	tmpQCDMassAsym = []
	tmpQCDCosTheta = []
	tmpQCDSubjetPtRatio = []
	tmpQCDDeltaEta = []
	tmpQCDJet1SubjetPtRatio = []
	tmpQCDJet2SubjetPtRatio = []
	tmpQCDJet1Tau21 = []
	tmpQCDJet1Tau31 = []
	tmpQCDJet2Tau21 = []
	tmpQCDJet2Tau31 = []


	for qcdBin, qcdValues in qcdDict.iteritems():
		tmpQCDMassAsym.append( qcdValues[0] )
		tmpQCDCosTheta.append( qcdValues[1] )
		tmpQCDSubjetPtRatio.append( qcdValues[2] )
		tmpQCDDeltaEta.append( qcdValues[3] )
		tmpQCDJet1SubjetPtRatio.append( qcdValues[4] )
		tmpQCDJet2SubjetPtRatio.append( qcdValues[5] )
		tmpQCDJet1Tau21.append( qcdValues[6] )
		tmpQCDJet1Tau31.append( qcdValues[7] )
		tmpQCDJet2Tau21.append( qcdValues[8] )
		tmpQCDJet2Tau31.append( qcdValues[9] )
		
	qcdMassAsym = [sum(i) for i in zip(*tmpQCDMassAsym)]
	qcdCosTheta = [sum(i) for i in zip(*tmpQCDCosTheta)]
	qcdSubjetPtRatio = [sum(i) for i in zip(*tmpQCDSubjetPtRatio)]
	qcdDeltaEta = [sum(i) for i in zip(*tmpQCDDeltaEta)]
	qcdJet1SubjetPtRatio = [sum(i) for i in zip(*tmpQCDJet1SubjetPtRatio)]
	qcdJet2SubjetPtRatio = [sum(i) for i in zip(*tmpQCDJet2SubjetPtRatio)]
	qcdJet1Tau21 = [sum(i) for i in zip(*tmpQCDJet1Tau21)]
	qcdJet1Tau31 = [sum(i) for i in zip(*tmpQCDJet1Tau31)]
	qcdJet2Tau21 = [sum(i) for i in zip(*tmpQCDJet2Tau21)]
	qcdJet2Tau31 = [sum(i) for i in zip(*tmpQCDJet2Tau31)]

	inputFileNameTTJets = 'Rootfiles/RUNAnalysis_TTJets_RunIISpring15DR74_Asympt25ns_v01_v06.root'
	TTJetsTotal = calcOpt( inputFileNameTTJets, grooming )
	TTJetsMassAsym = TTJetsTotal[0]
	TTJetsCosTheta = TTJetsTotal[1]
	TTJetsSubjetPtRatio = TTJetsTotal[2]
	TTJetsDeltaEta = TTJetsTotal[3]
	TTJetsJet1SubjetPtRatio = TTJetsTotal[4]
	TTJetsJet2SubjetPtRatio = TTJetsTotal[5]
	TTJetsJet1Tau21 = TTJetsTotal[6]
	TTJetsJet1Tau31 = TTJetsTotal[7]
	TTJetsJet2Tau21 = TTJetsTotal[8]
	TTJetsJet2Tau31 = TTJetsTotal[9]

	inputFileNameWJets = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIISpring15DR74_Asympt25ns_v01p2_v06.root'
	WJetsTotal = calcOpt( inputFileNameWJets, grooming )
	WJetsMassAsym = WJetsTotal[0]
	WJetsCosTheta = WJetsTotal[1]
	WJetsSubjetPtRatio = WJetsTotal[2]
	WJetsDeltaEta = WJetsTotal[3]
	WJetsJet1SubjetPtRatio = WJetsTotal[4]
	WJetsJet2SubjetPtRatio = WJetsTotal[5]
	WJetsJet1Tau21 = WJetsTotal[6]
	WJetsJet1Tau31 = WJetsTotal[7]
	WJetsJet2Tau21 = WJetsTotal[8]
	WJetsJet2Tau31 = WJetsTotal[9]

	inputFileNameZJets = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600ToInf_RunIISpring15DR74_Asympt25ns_v01p2_v06.root'
	ZJetsTotal = calcOpt( inputFileNameZJets, grooming )
	ZJetsMassAsym = ZJetsTotal[0]
	ZJetsCosTheta = ZJetsTotal[1]
	ZJetsSubjetPtRatio = ZJetsTotal[2]
	ZJetsDeltaEta = ZJetsTotal[3]
	ZJetsJet1SubjetPtRatio = ZJetsTotal[4]
	ZJetsJet2SubjetPtRatio = ZJetsTotal[5]
	ZJetsJet1Tau21 = ZJetsTotal[6]
	ZJetsJet1Tau31 = ZJetsTotal[7]
	ZJetsJet2Tau21 = ZJetsTotal[6]
	ZJetsJet2Tau31 = ZJetsTotal[7]
	
	outputFile = TFile( outputFileName, 'RECREATE' )

	massAsymOnlyOpt 	= TH1F('massAsymOnlyOpt', 'massAsymOnlyOpt; Mass Asymmetry Only Optimization', len(qcdMassAsym)-1, 0., 1. )
	cosThetaOnlyOpt 	= TH1F('cosThetaOnlyOpt', 'cosThetaOnlyOpt; Cos Theta StarOptimization', len(qcdCosTheta)-1, 0., 1. )
	subjetPtRatioOnlyOpt 	= TH1F('subjetPtRatioOnlyOpt', 'subjetPtRatioOnlyOpt; Subjet Pt Ratio Optimization', len(qcdSubjetPtRatio)-1, 0., 1. )
	deltaEtaOnlyOpt 	= TH1F('deltaEtaOnlyOpt', 'deltaEtaOnlyOpt; Delta Eta Dijet Only Optimization', len(qcdDeltaEta)-1, 0., 5. )
	jet1SubjetPtRatioOnlyOpt 	= TH1F('jet1SubjetPtRatioOnlyOpt', 'jet1SubjetPtRatioOnlyOpt; Subjet Pt Ratio Optimization', len(qcdJet1SubjetPtRatio)-1, 0., 1. )
	jet2SubjetPtRatioOnlyOpt 	= TH1F('jet2SubjetPtRatioOnlyOpt', 'jet2SubjetPtRatioOnlyOpt; Subjet Pt Ratio Optimization', len(qcdJet2SubjetPtRatio)-1, 0., 1. )
	jet1Tau21OnlyOpt 	= TH1F('jet1Tau21OnlyOpt', 'jet1Tau21OnlyOpt; Tau21 Optimization', len(qcdJet1Tau21)-1, 0., 1. )
	jet1Tau31OnlyOpt 	= TH1F('jet1Tau31OnlyOpt', 'jet1Tau31OnlyOpt; Tau31 Optimization', len(qcdJet1Tau31)-1, 0., 1. )
	jet2Tau21OnlyOpt 	= TH1F('jet2Tau21OnlyOpt', 'jet2Tau21OnlyOpt; Tau21 Optimization', len(qcdJet2Tau21)-1, 0., 1. )
	jet2Tau31OnlyOpt 	= TH1F('jet2Tau31OnlyOpt', 'jet2Tau31OnlyOpt; Tau31 Optimization', len(qcdJet2Tau31)-1, 0., 1. )

	for i in range( len( signalMassAsym ) ): 
		try: value = signalMassAsym[i]/ TMath.Sqrt( qcdMassAsym[i] + TTJetsMassAsym[i] + WJetsMassAsym[i] + ZJetsMassAsym[i] + signalMassAsym[i] )
		except ZeroDivisionError: value = 0
		massAsymOnlyOpt.SetBinContent( i, value )

	for i in range( len( signalCosTheta ) ): 
		try: value = signalCosTheta[i]/ TMath.Sqrt( qcdCosTheta[i] + TTJetsCosTheta[i] + WJetsCosTheta[i] + ZJetsCosTheta[i] + signalCosTheta[i] )
		except ZeroDivisionError: value = 0
		cosThetaOnlyOpt.SetBinContent( i, value )

	for i in range( len( signalSubjetPtRatio ) ): 
		try: value = signalSubjetPtRatio[i]/ TMath.Sqrt( qcdSubjetPtRatio[i] + TTJetsSubjetPtRatio[i] + WJetsSubjetPtRatio[i] + ZJetsSubjetPtRatio[i] + signalSubjetPtRatio[i] )
		except ZeroDivisionError: value = 0
		subjetPtRatioOnlyOpt.SetBinContent( i, value )

	for i in range( len( signalDeltaEta ) ): 
		try: value = signalDeltaEta[i]/ TMath.Sqrt( qcdDeltaEta[i] + TTJetsDeltaEta[i] + WJetsDeltaEta[i] + ZJetsDeltaEta[i] + signalDeltaEta[i] )
		except ZeroDivisionError: value = 0
		deltaEtaOnlyOpt.SetBinContent( i, value )

	for i in range( len( signalJet1SubjetPtRatio ) ): 
		try: value = signalJet1SubjetPtRatio[i]/ TMath.Sqrt( qcdJet1SubjetPtRatio[i] + TTJetsJet1SubjetPtRatio[i] + WJetsJet1SubjetPtRatio[i] + ZJetsJet1SubjetPtRatio[i] + signalJet1SubjetPtRatio[i] )
		except ZeroDivisionError: value = 0
		jet1SubjetPtRatioOnlyOpt.SetBinContent( i, value )
	
	for i in range( len( signalJet2SubjetPtRatio ) ): 
		try: value = signalJet2SubjetPtRatio[i]/ TMath.Sqrt( qcdJet2SubjetPtRatio[i] + TTJetsJet2SubjetPtRatio[i] + WJetsJet2SubjetPtRatio[i] + ZJetsJet2SubjetPtRatio[i] + signalJet2SubjetPtRatio[i] )
		except ZeroDivisionError: value = 0
		jet2SubjetPtRatioOnlyOpt.SetBinContent( i, value )

	for i in range( len( signalJet1Tau21 ) ): 
		try: value = signalJet1Tau21[i]/ TMath.Sqrt( qcdJet1Tau21[i] + TTJetsJet1Tau21[i] + WJetsJet1Tau21[i] + ZJetsJet1Tau21[i] + signalJet1Tau21[i] )
		except ZeroDivisionError: value = 0
		jet1Tau21OnlyOpt.SetBinContent( i, value )

	for i in range( len( signalJet1Tau31 ) ): 
		try: value = signalJet1Tau31[i]/ TMath.Sqrt( qcdJet1Tau31[i] + TTJetsJet1Tau31[i] + WJetsJet1Tau31[i] + ZJetsJet1Tau31[i] + signalJet1Tau31[i] )
		except ZeroDivisionError: value = 0
		jet1Tau31OnlyOpt.SetBinContent( i, value )

	for i in range( len( signalJet2Tau21 ) ): 
		try: value = signalJet2Tau21[i]/ TMath.Sqrt( qcdJet2Tau21[i] + TTJetsJet2Tau21[i] + WJetsJet2Tau21[i] + ZJetsJet2Tau21[i] + signalJet2Tau21[i] )
		except ZeroDivisionError: value = 0
		jet2Tau21OnlyOpt.SetBinContent( i, value )

	for i in range( len( signalJet2Tau31 ) ): 
		try: value = signalJet2Tau31[i]/ TMath.Sqrt( qcdJet2Tau31[i] + TTJetsJet2Tau31[i] + WJetsJet2Tau31[i] + ZJetsJet2Tau31[i] + signalJet2Tau31[i] )
		except ZeroDivisionError: value = 0
		jet2Tau31OnlyOpt.SetBinContent( i, value )

	
	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Write()
	outputFile.Close()




#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', type=int, dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store',  dest='grooming', default='Pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--pileup', action='store',  dest='pileup', default='Asympt25ns', help='Pileup' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	PU = args.pileup
	grooming = args.grooming

	outputFileName = 'Rootfiles/RUNOptimizationStudies.root'
	optimization( mass, PU, grooming, outputFileName )


