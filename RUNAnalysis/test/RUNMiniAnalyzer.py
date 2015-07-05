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
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TMath
from array import array
from scaleFactors import scaleFactor as SF

gROOT.SetBatch()

######################################
def myAnalyzer( sample, couts, grooming):


	inputFile = TFile( sample, 'read' )
	outputFileName = sample.replace('RUNAnalysis','RUNMiniAnalysis')
	outputFile = TFile( outputFileName, 'RECREATE' )
	#outputFile = TFile( 'test.root', 'RECREATE' )

	###################################### output Tree
	#tree = TTree('RUNAFinTree'+grooming, 'RUNAFinTree'+grooming)
	#AvgMass = array( 'f', [ 0. ] )
	#tree.Branch( 'AvgMass', AvgMass, 'AvgMass/F' )
	#Scale = array( 'f', [ 0. ] )
	#tree.Branch( 'Scale', Scale, 'Scale/F' )


	################################################################################################## Trigger Histos
	nBinsMass	= 60
	maxMass		= 600
	nBinsHT		= 150
	maxHT		= 1500

	massAve_Standard 	= TH1F('massAve_Standard', 'massAve_Standard', nBinsMass, 0, maxMass )
	massAve_EffStandard 	= TH1F('massAve_EffStandard', 'massAve_EffStandard', nBinsMass, 0, maxMass )
	
	AK4HT_PFHT800 	= TH1F('AK4HT_PFHT800', 'AK4HT_PFHT800', nBinsHT, 0, maxHT )
	massAve_PFHT800 	= TH1F('massAve_PFHT800', 'massAve_PFHT800', nBinsMass, 0, maxMass )
	AK4HT_EffPFHT800 	= TH1F('AK4HT_EffPFHT800', 'AK4HT_EffPFHT800', nBinsHT, 0, maxHT )
	massAve_EffPFHT800 	= TH1F('massAve_EffPFHT800', 'massAve_EffPFHT800', nBinsMass, 0, maxMass )

	AK4HT_Brock 	= TH1F('AK4HT_Brock', 'AK4HT_Brock', 200, 0, 2000 )
	massAve_Brock 	= TH1F('massAve_Brock', 'massAve_Brock', nBinsMass, 0, maxMass )

	#### For optimization
	massAve_massAsym00 	= TH1F('massAve_massAsym00', 'massAve_massAsym00', nBinsMass, 0, maxMass )
	massAve_massAsym01 	= TH1F('massAve_massAsym01', 'massAve_massAsym01', nBinsMass, 0, maxMass )
	massAve_massAsym02 	= TH1F('massAve_massAsym02', 'massAve_massAsym02', nBinsMass, 0, maxMass )
	massAve_massAsym03 	= TH1F('massAve_massAsym03', 'massAve_massAsym03', nBinsMass, 0, maxMass )
	massAve_massAsym04 	= TH1F('massAve_massAsym04', 'massAve_massAsym04', nBinsMass, 0, maxMass )
	massAve_massAsym05 	= TH1F('massAve_massAsym05', 'massAve_massAsym05', nBinsMass, 0, maxMass )
	massAve_massAsym06 	= TH1F('massAve_massAsym06', 'massAve_massAsym06', nBinsMass, 0, maxMass )
	massAve_massAsym07 	= TH1F('massAve_massAsym07', 'massAve_massAsym07', nBinsMass, 0, maxMass )
	massAve_massAsym08 	= TH1F('massAve_massAsym08', 'massAve_massAsym08', nBinsMass, 0, maxMass )
	massAve_massAsym09 	= TH1F('massAve_massAsym09', 'massAve_massAsym09', nBinsMass, 0, maxMass )
	massAve_massAsym10 	= TH1F('massAve_massAsym10', 'massAve_massAsym10', nBinsMass, 0, maxMass )

	###################################### Get GenTree 
	events = inputFile.Get( 'RUNATree'+grooming+'/RUNATree' )
	numEntries = events.GetEntriesFast()

	print '------> Number of events: '+str(numEntries)
	d = 0
	eventsPassed = 0
	newSF = SF(sample)*1000
	for i in xrange(numEntries):
		events.GetEntry(i)

		#---- progress of the reading --------
		fraction = 10.*i/(1.*numEntries)
		if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		d = TMath.FloorNint(fraction)

		#---- progress of the reading --------
		Run      = events.run
		Lumi     = events.lumi
		NumEvent = events.event
		if couts: print 'Entry ', Run, ':', Lumi, ':', NumEvent

		HT		= events.HT
		trimmedMass	= events.trimmedMass
		numJets		= events.numJets
		massAve		= events.massAve
		massAsym	= events.massAsym
		cosThetaStar	= events.cosThetaStar
		jet1SubjetPtRatio	= events.jet1SubjetPtRatio
		jet2SubjetPtRatio	= events.jet2SubjetPtRatio
		scale		= events.scale
		numPV           = events.numPV
		AK4HT           = events.AK4HT
		jet1Pt          = events.jet1Pt
		jet1Eta         = events.jet1Eta
		jet1Phi         = events.jet1Phi
		jet1E           = events.jet1E
		jet1Mass        = events.jet1Mass
		jet2Pt          = events.jet2Pt
		jet2Eta         = events.jet2Eta
		jet2Phi         = events.jet2Phi
		jet2E           = events.jet2E
		jet2Mass        = events.jet2Mass
		subjet11Pt      = events.subjet11Pt
		subjet11Eta     = events.subjet11Eta
		subjet11Phi     = events.subjet11Phi
		subjet11E       = events.subjet11E
		subjet12Pt      = events.subjet12Pt
		subjet12Eta     = events.subjet12Eta
		subjet12Phi     = events.subjet12Phi
		subjet12E       = events.subjet12E
		subjet21Pt      = events.subjet21Pt
		subjet21Eta     = events.subjet21Eta
		subjet21Phi     = events.subjet21Phi
		subjet21E       = events.subjet21E
		subjet22Pt      = events.subjet22Pt
		subjet22Eta     = events.subjet22Eta
		subjet22Phi     = events.subjet22Phi
		subjet22E       = events.subjet22E
		jet1Tau21       = events.jet1Tau21
		jet1Tau31       = events.jet1Tau31
		jet1Tau32       = events.jet1Tau32
		cosPhi13412     = events.cosPhi13412
		cosPhi31234     = events.cosPhi31234

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) and ( numJets > 1 ) )  
		subjetPtRatio = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		massAsymCut = ( massAsym < 0.1 ) 
		cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		subjetPtRatioCut = ( subjetPtRatio ) 

		if triggerCut and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			eventsPassed +=1
			#AvgMass = massAve
			#Scale = scale
			massAve_Standard.Fill( massAve, newSF )
			#print AvgMass, newSF, scale

		if ( ( HT > 800 ) and ( trimmedMass > 50 ) ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			massAve_EffStandard.Fill( massAve, newSF )
		
		if ( AK4HT > 800 ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			AK4HT_PFHT800.Fill( AK4HT, newSF )
			massAve_PFHT800.Fill( massAve, newSF )

		if ( AK4HT > 900 ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			AK4HT_EffPFHT800.Fill( AK4HT, newSF )
			massAve_EffPFHT800.Fill( massAve, newSF )

		if ( AK4HT > 1600 ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			AK4HT_Brock.Fill( AK4HT, newSF )
			massAve_Brock.Fill( massAve, newSF )

		##### For Optimization:
		if triggerCut and ( massAsym < 0.0 ): massAve_massAsym00.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.1 ): massAve_massAsym01.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.2 ): massAve_massAsym02.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.3 ): massAve_massAsym03.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.4 ): massAve_massAsym04.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.5 ): massAve_massAsym05.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.6 ): massAve_massAsym06.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.7 ): massAve_massAsym07.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.8 ): massAve_massAsym08.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 0.9 ): massAve_massAsym09.Fill( massAve, newSF )
		if triggerCut and ( massAsym < 1.0 ): massAve_massAsym10.Fill( massAve, newSF )

		#tree.Fill()
	print eventsPassed
				#print triggerCut, analysisCut, massAsym, cosThetaStar, subjetPtRatio


	##### write output file 
	#outputFile.cd()
	#for key in inputFile.GetListOfKeys():
	#	print key
	#	saveDir = TDirectory()
		#adir = saveDir.mkdir( key.GetName() )
		#adir.cd()
		#if key.GetClassName() == 'TDirectoryFile':
		#	if not 'Tree' in key.GetName():
		#		newDir = outputFile.mkdir( key.GetName() )
		#		newDir.cd()
		#for q in key.GetList():
		#	print q
				#	print key.GetName(), q


	outputFile.Write()

	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Close()

	###### Extra: send prints to file
	#if couts == False: 
	#	sys.stdout = outfileStdOut
	#	f.close()
	#########################


#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', type=int, dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store',  dest='grooming', default='Pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--pileup', action='store',  dest='pileup', default='PU20bx25', help='Pileup' )
	parser.add_argument( '-d', '--debug', action='store_true', dest='couts', default=False, help='True print couts in screen, False print in a file' )
	parser.add_argument( '-s', '--sample', action='store',   dest='samples', default='RPV', help='Type of sample' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	PU = args.pileup
	couts = args.couts
	grooming = args.grooming
	samples = args.samples

	if 'RPV' in samples: 
		inputFileName = 'Rootfiles/v03_v09/RUNAnalysis_RPVSt'+str(mass)+'tojj_PHYS14_'+PU+'_v03_v09.root'
		myAnalyzer( inputFileName, couts, grooming )
	else: 
		for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800' ]: 
			inputFileName = 'Rootfiles/v03_v09/RUNAnalysis_QCD_Pt-'+qcdBin+'_PHYS14_'+PU+'_v03_v09.root'
			myAnalyzer( inputFileName, couts, grooming )

