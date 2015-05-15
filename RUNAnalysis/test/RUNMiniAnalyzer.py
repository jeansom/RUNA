#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time
import optparse
#from collections import defaultdict
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TMath
from array import array
from scaleFactors import scaleFactor

gROOT.SetBatch()

######################################
def myAnalyzer( sample, couts, grooming):


	inputFile = TFile( 'Rootfiles/RUNAnalysis_'+sample+'_v03_v09.root', 'read' )
	outputFile = TFile( 'Rootfiles/RUNMiniAnalysis_'+sample+'_v03_v09.root', 'RECREATE' )

	###################################### output Tree
	tree = TTree('RUNAFinTree'+grooming, 'RUNAFinTree'+grooming)
	AvgMass = array( 'f', [ 0. ] )
	tree.Branch( 'AvgMass', AvgMass, 'AvgMass/F' )
	Scale = array( 'f', [ 0. ] )
	tree.Branch( 'Scale', Scale, 'Scale/F' )


	################################################################################################## Trigger Histos
	nBinsMass	= 50
	maxMass		= 500

	massAve_allCuts 	= TH1F('h_massAve_allCuts', 'h_massAve_allCuts', nBinsMass, 0, maxMass )

	###################################### Get GenTree 
	events = inputFile.Get( 'RUNATree'+grooming+'/RUNATree' )
	numEntries = events.GetEntriesFast()

	SF = scaleFactor(sample)
	SF = SF*1000

	print '------> Number of events: '+str(numEntries)
	d = 0
	eventsPassed = 0
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

		#### Apply selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )

		if triggerCut:
			subjetPtRatio = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
			analysisCut = ( ( numJets > 1 ) and ( massAsym < 0.1 ) and ( abs( cosThetaStar ) < 0.3 ) and ( subjetPtRatio )  )

			if analysisCut:

				eventsPassed +=1
				AvgMass[0] = massAve
				Scale[0] = SF
				massAve_allCuts.Fill( massAve, SF )
				#print AvgMass, SF

		tree.Fill()
	print 'Raw number of events: ',eventsPassed
	outputFile.Write()

	##### Closing
	#print 'Writing output file: '+ outputFileName
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
	parser.add_argument( '-m', '--mass', action='store', type='int', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store', type='string', dest='grooming', default='Pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--pileup', action='store', type='string', dest='pileup', default='PU20bx25', help='Pileup' )
	parser.add_argument( '-d', '--debug', action='store_true', dest='couts', default=False, help='True print couts in screen, False print in a file' )
	parser.add_argument( '-s', '--sample', action='store',  type='string', dest='samples', default='Signal', help='Type of sample' )

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

	if 'QCD' in samples:
		QCDBins = [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800' ]
		for bin in QCDBins:
			sample = 'QCD_Pt-'+bin+'_PHYS14_'+PU
			myAnalyzer( sample, couts, grooming )
	else:
		sample = 'RPVSt'+str(mass)+'tojj_PHYS14_'+PU
		myAnalyzer( sample, couts, grooming )
