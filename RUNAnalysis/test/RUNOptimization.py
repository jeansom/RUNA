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
	numCosTheta00 = numCosTheta01 = numCosTheta02 = numCosTheta03 = numCosTheta04 = numCosTheta05 = numCosTheta06 = numCosTheta07 = numCosTheta08 = numCosTheta09 = numCosTheta10 = 0
	numSubjetPtRatio00 = numSubjetPtRatio01 = numSubjetPtRatio02 = numSubjetPtRatio03 = numSubjetPtRatio04 = numSubjetPtRatio05 = numSubjetPtRatio06 = numSubjetPtRatio07 = numSubjetPtRatio08 = numSubjetPtRatio09 = numSubjetPtRatio10 = 0

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
		#print 'Entry ', Run, ':', Lumi, ':', NumEvent

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
#		jet1Eta         = events.jet1Eta
#		jet1Phi         = events.jet1Phi
#		jet1E           = events.jet1E
#		jet1Mass        = events.jet1Mass
#		jet2Pt          = events.jet2Pt
#		jet2Eta         = events.jet2Eta
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
#		jet1Tau21       = events.jet1Tau21
#		jet1Tau31       = events.jet1Tau31
#		jet1Tau32       = events.jet1Tau32
#		cosPhi13412     = events.cosPhi13412
#		cosPhi31234     = events.cosPhi31234

		#### TEST

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )
		dijet = ( numJets > 1 )   
		subjetPtRatio = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		massAsymCut = ( massAsym < 0.1 ) 
		cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		subjetPtRatioCut = ( subjetPtRatio ) 

		if triggerCut and dijet and massAsymCut and cosThetaStarCut and subjetPtRatioCut: eventsPassed +=1

		##### For Optimization:
		if triggerCut: eventsAfterTrigger +=1

		if triggerCut and dijet and ( massAsym <= 0.0 ): numMassAsym00 += 1
		if triggerCut and dijet and ( massAsym <= 0.1 ): numMassAsym01 += 1
		if triggerCut and dijet and ( massAsym <= 0.2 ): numMassAsym02 += 1
		if triggerCut and dijet and ( massAsym <= 0.3 ): numMassAsym03 += 1
		if triggerCut and dijet and ( massAsym <= 0.4 ): numMassAsym04 += 1
		if triggerCut and dijet and ( massAsym <= 0.5 ): numMassAsym05 += 1
		if triggerCut and dijet and ( massAsym <= 0.6 ): numMassAsym06 += 1
		if triggerCut and dijet and ( massAsym <= 0.7 ): numMassAsym07 += 1
		if triggerCut and dijet and ( massAsym <= 0.8 ): numMassAsym08 += 1
		if triggerCut and dijet and ( massAsym <= 0.9 ): numMassAsym09 += 1
		if triggerCut and dijet and ( massAsym <= 1.0 ): numMassAsym10 += 1


		if triggerCut and dijet and ( cosThetaStar <= 0.0 ): numCosTheta00 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.1 ): numCosTheta01 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.2 ): numCosTheta02 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.3 ): numCosTheta03 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.4 ): numCosTheta04 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.5 ): numCosTheta05 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.6 ): numCosTheta06 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.7 ): numCosTheta07 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.8 ): numCosTheta08 += 1
		if triggerCut and dijet and ( cosThetaStar <= 0.9 ): numCosTheta09 += 1
		if triggerCut and dijet and ( cosThetaStar <= 1.0 ): numCosTheta10 += 1


		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.0 ) and ( jet1SubjetPtRatio >= 0.0 ): numSubjetPtRatio00 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.1 ) and ( jet1SubjetPtRatio >= 0.1 ): numSubjetPtRatio01 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.2 ) and ( jet1SubjetPtRatio >= 0.2 ): numSubjetPtRatio02 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.3 ) and ( jet1SubjetPtRatio >= 0.3 ): numSubjetPtRatio03 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.4 ) and ( jet1SubjetPtRatio >= 0.4 ): numSubjetPtRatio04 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.5 ) and ( jet1SubjetPtRatio >= 0.5 ): numSubjetPtRatio05 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.6 ) and ( jet1SubjetPtRatio >= 0.6 ): numSubjetPtRatio06 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.7 ) and ( jet1SubjetPtRatio >= 0.7 ): numSubjetPtRatio07 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.8 ) and ( jet1SubjetPtRatio >= 0.8 ): numSubjetPtRatio08 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 0.9 ) and ( jet1SubjetPtRatio >= 0.9 ): numSubjetPtRatio09 += 1
		if triggerCut and dijet and ( jet1SubjetPtRatio >= 1.0 ) and ( jet1SubjetPtRatio >= 1.0 ): numSubjetPtRatio10 += 1


	tmpTotalMassAsym = [ numMassAsym00, numMassAsym01, numMassAsym02, numMassAsym03, numMassAsym04, numMassAsym05, numMassAsym06, numMassAsym07, numMassAsym08, numMassAsym09, numMassAsym10 ]
	totalMassAsym = [ x * newSF for x in tmpTotalMassAsym  ] 
	tmpTotalCosTheta = [ numCosTheta00, numCosTheta01, numCosTheta02, numCosTheta03, numCosTheta04, numCosTheta05, numCosTheta06, numCosTheta07, numCosTheta08, numCosTheta09, numCosTheta10 ]
	totalCosTheta = [ x * newSF for x in tmpTotalCosTheta  ] 
	tmpTotalSubjetPtRatio = [ numSubjetPtRatio00, numSubjetPtRatio01, numSubjetPtRatio02, numSubjetPtRatio03, numSubjetPtRatio04, numSubjetPtRatio05, numSubjetPtRatio06, numSubjetPtRatio07, numSubjetPtRatio08, numSubjetPtRatio09, numSubjetPtRatio10 ]
	totalSubjetPtRatio = [ x * newSF for x in tmpTotalSubjetPtRatio  ] 

	TOTAL1  = [ totalMassAsym, totalCosTheta, totalSubjetPtRatio  ]
	print 'massAsym', totalMassAsym
	print 'cosThetaStar', totalCosTheta
	print 'subjetPtRatio', totalSubjetPtRatio
	print 'events after trigger', eventsAfterTrigger, 'events that pass selection', eventsPassed

	return TOTAL1


def optimization( mass, PU, grooming, outputFileName ):
	"""docstring for optimization"""

	inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15DR74_'+PU+'_v02p2_v06.root'
	signalTotal = calcOpt( inputFileName, grooming )
	signalMassAsym = signalTotal[0]
	signalCosTheta = signalTotal[1]
	signalSubjetPtRatio = signalTotal[2]

	qcdDict = {}
	for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800' ]: 
		inputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15DR74_'+PU+'_v01_v06.root'
		qcdDict[ qcdBin ] = calcOpt( inputFileName, grooming )

	tmpQCDMassAsym = []
	tmpQCDCosTheta = []
	tmpQCDSubjetPtRatio = []
	for qcdBin, qcdValues in qcdDict.iteritems():
		tmpQCDMassAsym.append( qcdValues[0] )
		tmpQCDCosTheta.append( qcdValues[1] )
		tmpQCDSubjetPtRatio.append( qcdValues[2] )
		
	qcdMassAsym = [sum(i) for i in zip(*tmpQCDMassAsym)]
	qcdCosTheta = [sum(i) for i in zip(*tmpQCDCosTheta)]
	qcdSubjetPtRatio = [sum(i) for i in zip(*tmpQCDSubjetPtRatio)]

	
	outputFile = TFile( outputFileName, 'RECREATE' )

	massAsymOnlyOpt 	= TH1F('massAsymOnlyOpt', 'massAsymOnlyOpt; Mass Asymmetry Only Optimization', len(qcdMassAsym), 0., len(qcdMassAsym) )
	cosThetaOnlyOpt 	= TH1F('cosThetaOnlyOpt', 'cosThetaOnlyOpt; Cos Theta StarOptimization', len(qcdCosTheta), 0., len(qcdCosTheta) )
	subjetPtRatioOnlyOpt 	= TH1F('subjetPtRatioOnlyOpt', 'subjetPtRatioOnlyOpt; Subjet Pt Ratio Optimization', len(qcdMassAsym), 0., len(qcdMassAsym) )

	for i in range( len( signalMassAsym ) ): 
		try: value = signalMassAsym[i]/ TMath.Sqrt( qcdMassAsym[i] + signalMassAsym[i] )
		except ZeroDivisionError: value = 0
		massAsymOnlyOpt.SetBinContent( i, value )

	for i in range( len( signalCosTheta ) ): 
		try: value = signalCosTheta[i]/ TMath.Sqrt( qcdCosTheta[i] + signalCosTheta[i] )
		except ZeroDivisionError: value = 0
		cosThetaOnlyOpt.SetBinContent( i, value )

	for i in range( len( signalSubjetPtRatio ) ): 
		try: value = signalSubjetPtRatio[i]/ TMath.Sqrt( qcdSubjetPtRatio[i] + signalSubjetPtRatio[i] )
		except ZeroDivisionError: value = 0
		subjetPtRatioOnlyOpt.SetBinContent( i, value )

	
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


