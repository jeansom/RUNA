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

	trimmedMassVsHT 	= TH2D('trimmedMassVsHT', 'trimmedMassVsHT', nBinsMass, 0, maxMass, nBinsHT, 0, maxHT )
	massAve_Standard 	= TH1F('massAve_Standard', 'massAve_Standard', nBinsMass, 0, maxMass )
	massAve_EffStandard 	= TH1F('massAve_EffStandard', 'massAve_EffStandard', nBinsMass, 0, maxMass )
	
	AK4HT_PFHT800 	= TH1F('AK4HT_PFHT800', 'AK4HT_PFHT800', nBinsHT, 0, maxHT )
	massAve_PFHT800 	= TH1F('massAve_PFHT800', 'massAve_PFHT800', nBinsMass, 0, maxMass )
	AK4HT_EffPFHT800 	= TH1F('AK4HT_EffPFHT800', 'AK4HT_EffPFHT800', nBinsHT, 0, maxHT )
	massAve_EffPFHT800 	= TH1F('massAve_EffPFHT800', 'massAve_EffPFHT800', nBinsMass, 0, maxMass )

	AK4HT_Brock 	= TH1F('AK4HT_Brock', 'AK4HT_Brock', 200, 0, 2000 )
	massAve_Brock 	= TH1F('massAve_Brock', 'massAve_Brock', nBinsMass, 0, maxMass )

	#### Optimization
	h_deltaEtaDijet 	= TH1F('deltaEtaDijet', 'deltaEtaDijet', 100, 0, 5. )

	h_massAveVsHT 	= TH2D('massAveVsHT', 'massAveVsHT', nBinsMass, 0, maxMass, nBinsHT, 0, maxHT )
	h_massAveVsnumJets 	= TH2D('massAveVsnumJets', 'massAveVsnumJets', nBinsMass, 0, maxMass, 10, 0, 10 )
	h_massAveVsmassAsym 	= TH2D('massAveVsmassAsym', 'massAveVsmassAsym', nBinsMass, 0, maxMass, 20, 0, 1. )
	h_massAveVscosThetaStar 	= TH2D('massAveVscosThetaStar', 'massAveVscosThetaStar', nBinsMass, 0, maxMass, 20, 0, 1. )
	h_massAveVsjet1SubjetPtRatio 	= TH2D('massAveVsjet1SubjetPtRatio', 'massAveVsjet1SubjetPtRatio', nBinsMass, 0, maxMass, 20, 0, 1. )
	h_massAveVsjet2SubjetPtRatio 	= TH2D('massAveVsjet2SubjetPtRatio', 'massAveVsjet2SubjetPtRatio', nBinsMass, 0, maxMass, 20, 0, 1. )
	h_massAveVsTau21 	= TH2D('massAveVsTau21', 'massAveVsTau21', nBinsMass, 0, maxMass, 20, 0, 1. )
	h_massAveVsTau31 	= TH2D('massAveVsTau31', 'massAveVsTau31', nBinsMass, 0, maxMass, 20, 0, 1. )
	h_massAveVsdeltaEtaDijet 	= TH2D('massAveVsdeltaEtaDijet', 'massAveVsdeltaEtaDijet', nBinsMass, 0, maxMass, 100, 0, 5. )

	h_massAsymVscosThetaStar 	= TH2D('massAsymVscosThetaStar', 'massAsymVscosThetaStar', 20, 0, 1., 20, 0, 1. )
	h_massAsymVsjet1SubjetPtRatio 	= TH2D('massAsymVsjet1SubjetPtRatio', 'massAsymVsjet1SubjetPtRatio', 20, 0, 1., 20, 0, 1. )
	h_massAsymVsjet2SubjetPtRatio 	= TH2D('massAsymVsjet2SubjetPtRatio', 'massAsymVsjet2SubjetPtRatio', 20, 0, 1., 20, 0, 1. )
	h_massAsymVsTau21 	= TH2D('massAsymVsTau21', 'massAsymVsTau21', 20, 0, 1., 20, 0, 1. )
	h_massAsymVsTau31 	= TH2D('massAsymVsTau31', 'massAsymVsTau31', 20, 0, 1., 20, 0, 1. )
	h_massAsymVsdeltaEtaDijet 	= TH2D('massAsymVsdeltaEtaDijet', 'massAsymVsdeltaEtaDijet', 20, 0, 1., 100, 0, 5. )

	h_cosThetaStarVsjet1SubjetPtRatio 	= TH2D('cosThetaStarVsjet1SubjetPtRatio', 'cosThetaStarVsjet1SubjetPtRatio', 20, 0, 1., 20, 0, 1. )
	h_cosThetaStarVsjet2SubjetPtRatio 	= TH2D('cosThetaStarVsjet2SubjetPtRatio', 'cosThetaStarVsjet2SubjetPtRatio', 20, 0, 1., 20, 0, 1. )
	h_cosThetaStarVsTau21 	= TH2D('cosThetaStarVsTau21', 'cosThetaStarVsTau21', 20, 0, 1., 20, 0, 1. )
	h_cosThetaStarVsTau31 	= TH2D('cosThetaStarVsTau31', 'cosThetaStarVsTau31', 20, 0, 1., 20, 0, 1. )
	h_cosThetaStarVsdeltaEtaDijet 	= TH2D('cosThetaStarVsdeltaEtaDijet', 'cosThetaStarVsdeltaEtaDijet', 20, 0, 1., 100, 0, 5. )

	h_jet1SubjetPtRatioVsjet2SubjetPtRatio 	= TH2D('jet1SubjetPtRatioVsjet2SubjetPtRatio', 'jet1SubjetPtRatioVsjet2SubjetPtRatio', 20, 0, 1., 20, 0, 1. )
	h_jet1SubjetPtRatioVsTau21 	= TH2D('jet1SubjetPtRatioVsTau21', 'jet1SubjetPtRatioVsTau21', 20, 0, 1., 20, 0, 1. )
	h_jet1SubjetPtRatioVsTau31 	= TH2D('jet1SubjetPtRatioVsTau31', 'jet1SubjetPtRatioVsTau31', 20, 0, 1., 20, 0, 1. )
	h_jet1SubjetPtRatioVsdeltaEtaDijet 	= TH2D('jet1SubjetPtRatioVsdeltaEtaDijet', 'jet1SubjetPtRatioVsdeltaEtaDijet', 20, 0, 1., 100, 0, 5. )

	h_jet2SubjetPtRatioVsTau21 	= TH2D('jet2SubjetPtRatioVsTau21', 'jet2SubjetPtRatioVsTau21', 20, 0, 1., 20, 0, 1. )
	h_jet2SubjetPtRatioVsTau31 	= TH2D('jet2SubjetPtRatioVsTau31', 'jet2SubjetPtRatioVsTau31', 20, 0, 1., 20, 0, 1. )
	h_jet2SubjetPtRatioVsdeltaEtaDijet 	= TH2D('jet2SubjetPtRatioVsdeltaEtaDijet', 'jet2SubjetPtRatioVsdeltaEtaDijet', 20, 0, 1., 100, 0, 5. )

	h_jet1Tau21VsdeltaEtaDijet 	= TH2D('jet1Tau21VsdeltaEtaDijet', 'jet1Tau21VsdeltaEtaDijet', 20, 0, 1., 100, 0, 5. )
	h_jet1Tau31VsdeltaEtaDijet 	= TH2D('jet1Tau31VsdeltaEtaDijet', 'jet1Tau31VsdeltaEtaDijet', 20, 0, 1., 100, 0, 5. )


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
		scale		= events.Scale
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

		#### Optimization
		deltaEtaDijet = abs( jet1Eta - jet2Eta )
		h_deltaEtaDijet.Fill( deltaEtaDijet, scale )

		h_massAveVsHT.Fill( massAve, HT, scale )
		h_massAveVsnumJets.Fill( massAve, numJets, scale )
		h_massAveVsmassAsym.Fill( massAve, massAsym, scale )
		h_massAveVscosThetaStar.Fill( massAve, cosThetaStar, scale )
		h_massAveVsjet1SubjetPtRatio.Fill( massAve, jet1SubjetPtRatio, scale )
		h_massAveVsjet2SubjetPtRatio.Fill( massAve, jet2SubjetPtRatio, scale )
		h_massAveVsTau21.Fill( massAve, jet1Tau21, scale )
		h_massAveVsTau31.Fill( massAve, jet1Tau31, scale )
		h_massAveVsdeltaEtaDijet.Fill( massAve, deltaEtaDijet, scale )

		h_massAsymVscosThetaStar.Fill( massAsym, cosThetaStar, scale )
		h_massAsymVsjet1SubjetPtRatio.Fill( massAsym, jet1SubjetPtRatio, scale )
		h_massAsymVsjet2SubjetPtRatio.Fill( massAsym, jet2SubjetPtRatio, scale )
		h_massAsymVsTau21.Fill( massAsym, jet1Tau21, scale )
		h_massAsymVsTau31.Fill( massAsym, jet1Tau31, scale )
		h_massAsymVsdeltaEtaDijet.Fill( massAsym, deltaEtaDijet, scale )

		h_cosThetaStarVsjet1SubjetPtRatio.Fill( cosThetaStar, jet1SubjetPtRatio, scale )
		h_cosThetaStarVsjet2SubjetPtRatio.Fill( cosThetaStar, jet2SubjetPtRatio, scale )
		h_cosThetaStarVsTau21.Fill( cosThetaStar, jet1Tau21, scale )
		h_cosThetaStarVsTau31.Fill( cosThetaStar, jet1Tau31, scale )
		h_cosThetaStarVsdeltaEtaDijet.Fill( cosThetaStar, deltaEtaDijet, scale )

		h_jet1SubjetPtRatioVsjet2SubjetPtRatio.Fill( jet1SubjetPtRatio, jet2SubjetPtRatio, scale )
		h_jet1SubjetPtRatioVsTau21.Fill( jet1SubjetPtRatio, jet1Tau21, scale )
		h_jet1SubjetPtRatioVsTau31.Fill( jet1SubjetPtRatio, jet1Tau31, scale )
		h_jet1SubjetPtRatioVsdeltaEtaDijet.Fill( jet1SubjetPtRatio, deltaEtaDijet, scale )

		h_jet2SubjetPtRatioVsTau21.Fill( jet2SubjetPtRatio, jet1Tau21, scale )
		h_jet2SubjetPtRatioVsTau31.Fill( jet2SubjetPtRatio, jet1Tau31, scale )
		h_jet2SubjetPtRatioVsdeltaEtaDijet.Fill( jet2SubjetPtRatio, deltaEtaDijet, scale )

		h_jet1Tau21VsdeltaEtaDijet.Fill( jet1Tau21, deltaEtaDijet, scale )
		h_jet1Tau31VsdeltaEtaDijet.Fill( jet1Tau31, deltaEtaDijet, scale )

		#### TEST
		trimmedMassVsHT.Fill( trimmedMass, HT )

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
			#print Run, Lumi, NumEvent
			massAve_Standard.Fill( massAve, newSF )
			#print AvgMass, newSF, scale

		if ( ( HT > 700 ) and ( trimmedMass > 50 ) ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
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
	parser.add_argument( '-p', '--pileup', action='store',  dest='pileup', default='Asympt25ns', help='Pileup' )
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
		inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15DR74_'+PU+'_v02p2_v06.root'
		myAnalyzer( inputFileName, couts, grooming )
	elif 'Data' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_JetHT_Asympt50ns_v01p2_v06.root'
		myAnalyzer( inputFileName, couts, grooming )
	else: 
		for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800' ]: 
			inputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15DR74_'+PU+'_v01_v06.root'
			myAnalyzer( inputFileName, couts, grooming )

