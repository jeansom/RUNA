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
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2D, TMath, TLorentzVector
from array import array
from RUNA.RUNAnalysis.scaleFactors import scaleFactor as SF

gROOT.SetBatch()

######################################
def myAnalyzer( sample, couts, grooming):


	inputFile = TFile( sample, 'read' )
	outputFileName = sample.replace('RUNAnalysis','RUNMiniBoostedAnalysis')
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
	massAve_Tau21 	= TH1F('massAve_Tau21', 'massAve_Tau21', nBinsMass, 0, maxMass )
	massAve_Tau21CosTheta 	= TH1F('massAve_Tau21CosTheta', 'massAve_Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Tau21CosThetaDEta 	= TH1F('massAve_Tau21CosThetaDEta', 'massAve_Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	massAve_Tau21CosThetaNODEta 	= TH1F('massAve_Tau21CosThetaNODEta', 'massAve_Tau21CosThetaNODEta', nBinsMass, 0, maxMass )
	massAve_Tau21NOCosTheta 	= TH1F('massAve_Tau21NOCosTheta', 'massAve_Tau21NOCosTheta', nBinsMass, 0, maxMass )
	massAve_Tau21NOCosThetaDEta 	= TH1F('massAve_Tau21NOCosThetaDEta', 'massAve_Tau21NOCosThetaDEta', nBinsMass, 0, maxMass )
	massAve_Tau21NOCosThetaNODEta 	= TH1F('massAve_Tau21NOCosThetaNODEta', 'massAve_Tau21NOCosThetaNODEta', nBinsMass, 0, maxMass )
	massAve_NOTau21 	= TH1F('massAve_NOTau21', 'massAve_NOTau21', nBinsMass, 0, maxMass )
	massAve_NOTau21Tau31 	= TH1F('massAve_NOTau21Tau31', 'massAve_NOTau21Tau31', nBinsMass, 0, maxMass )
	massAve_NOTau21Tau31CosTheta 	= TH1F('massAve_NOTau21Tau31CosTheta', 'massAve_NOTau21Tau31CosTheta', nBinsMass, 0, maxMass )
	massAve_NOTau21CosTheta 	= TH1F('massAve_NOTau21CosTheta', 'massAve_NOTau21CosTheta', nBinsMass, 0, maxMass )
	massAve_NOTau21CosThetaDEta 	= TH1F('massAve_NOTau21CosThetaDEta', 'massAve_NOTau21CosThetaDEta', nBinsMass, 0, maxMass )
	massAve_NOTau21CosThetaDEtaSubPtRatio 	= TH1F('massAve_NOTau21CosThetaDEtaSubPtRatio', 'massAve_NOTau21CosThetaDEtaSubPtRatio', nBinsMass, 0, maxMass )
	massAve_NOMassAsym 	= TH1F('massAve_NOMassAsym', 'massAve_NOMassAsym', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21CosThetaDEta 	= TH1F('massAve_NOMassAsymTau21CosThetaDEta', 'massAve_NOMassAsymTau21CosThetaDEta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21CosThetaDEtaSubPtRatio 	= TH1F('massAve_NOMassAsymTau21CosThetaDEtaSubPtRatio', 'massAve_NOMassAsymTau21CosThetaDEtaSubPtRatio', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21 	= TH1F('massAve_NOMassAsymTau21', 'massAve_NOMassAsymTau21', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOCosTheta 	= TH1F('massAve_NOMassAsymNOCosTheta', 'massAve_NOMassAsymNOCosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau31 	= TH1F('massAve_NOMassAsymTau31', 'massAve_NOMassAsymTau31', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau31CosTheta 	= TH1F('massAve_NOMassAsymTau31CosTheta', 'massAve_NOMassAsymTau31CosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau31CosThetaDEta 	= TH1F('massAve_NOMassAsymTau31CosThetaDEta', 'massAve_NOMassAsymTau31CosThetaDEta', nBinsMass, 0, maxMass )
	
	massAve_Tau2104 	= TH1F('massAve_Tau2104', 'massAve_Tau2104', nBinsMass, 0, maxMass )
	massAve_Tau2105 	= TH1F('massAve_Tau2105', 'massAve_Tau2105', nBinsMass, 0, maxMass )
	massAve_Tau2106 	= TH1F('massAve_Tau2106', 'massAve_Tau2106', nBinsMass, 0, maxMass )
	massAve_Tau2107 	= TH1F('massAve_Tau2107', 'massAve_Tau2107', nBinsMass, 0, maxMass )
	massAve_Tau3104 	= TH1F('massAve_Tau3104', 'massAve_Tau3104', nBinsMass, 0, maxMass )
	massAve_Tau3105 	= TH1F('massAve_Tau3105', 'massAve_Tau3105', nBinsMass, 0, maxMass )
	massAve_Tau3106 	= TH1F('massAve_Tau3106', 'massAve_Tau3106', nBinsMass, 0, maxMass )
	massAve_Tau3107 	= TH1F('massAve_Tau3107', 'massAve_Tau3107', nBinsMass, 0, maxMass )

	massAve_NOMATau2104 	= TH1F('massAve_NOMATau2104', 'massAve_NOMATau2104', nBinsMass, 0, maxMass )
	massAve_NOMATau2105 	= TH1F('massAve_NOMATau2105', 'massAve_NOMATau2105', nBinsMass, 0, maxMass )
	massAve_NOMATau2106 	= TH1F('massAve_NOMATau2106', 'massAve_NOMATau2106', nBinsMass, 0, maxMass )
	massAve_NOMATau2107 	= TH1F('massAve_NOMATau2107', 'massAve_NOMATau2107', nBinsMass, 0, maxMass )
	massAve_NOMATau3104 	= TH1F('massAve_NOMATau3104', 'massAve_NOMATau3104', nBinsMass, 0, maxMass )
	massAve_NOMATau3105 	= TH1F('massAve_NOMATau3105', 'massAve_NOMATau3105', nBinsMass, 0, maxMass )
	massAve_NOMATau3106 	= TH1F('massAve_NOMATau3106', 'massAve_NOMATau3106', nBinsMass, 0, maxMass )
	massAve_NOMATau3107 	= TH1F('massAve_NOMATau3107', 'massAve_NOMATau3107', nBinsMass, 0, maxMass )

	#### Optimization
	h_deltaEtaDijet 	= TH1F('deltaEtaDijet', 'deltaEtaDijet', 100, 0, 5. )
	h_jet2Tau21 	= TH1F('jet2Tau21', 'jet2Tau21', 10, 0, 1. )
	h_jet2Tau31 	= TH1F('jet2Tau31', 'jet2Tau31', 10, 0, 1. )
	jet1Pt_cutHT 	= TH1F('jet1Pt_cutHT', 'jet1Pt_cutHT', 100, 0, 1000. )
	HT_noHTCut 	= TH1F('HT_cutHT', 'HT_cutHT', 100, 0, 2000. )
	jet2Pt_cutHT 	= TH1F('jet2Pt_cutHT', 'jet2Pt_cutHT', 100, 0, 1000. )
	jet1Pt_Tau21CosTheta 	= TH1F('jet1Pt_Tau21CosTheta', 'jet1Pt_Tau21CosTheta', 100, 0, 1000. )
	jet2Pt_Tau21CosTheta 	= TH1F('jet2Pt_Tau21CosTheta', 'jet2Pt_Tau21CosTheta', 100, 0, 1000. )



	###################################### Get GenTree 
	events = inputFile.Get( 'RUNATree'+grooming+'/RUNATree' )
	numEntries = events.GetEntriesFast()

	print '------> Number of events: '+str(numEntries)
	d = 0
	newLumi = 0
	tmpLumi = 0
	eventsRaw = eventsHT = eventsPassed = eventsDijet = eventsMassAsym = eventsDEta = eventsDEtaSubjet = eventsDEtaTau21 = eventsDEtaTau31 = eventsCosTheta = eventsTau21 = eventsTau21CosTheta = eventsTau21CosThetaDEta = 0
	for i in xrange(numEntries):
		events.GetEntry(i)
		eventsRaw += 1

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
		J1CosThetaStar	= events.jet1CosThetaStar
		J2CosThetaStar	= events.jet2CosThetaStar
		jet1SubjetPtRatio	= events.jet1SubjetPtRatio
		jet2SubjetPtRatio	= events.jet2SubjetPtRatio
		puWeight	= events.puWeight
		lumiWeight	= events.lumiWeight
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
		jet1Tau32       = events.jet1Tau32
		jet2Tau21       = events.jet2Tau21
		jet2Tau31       = events.jet2Tau31
		jet2Tau32       = events.jet2Tau32
		cosPhi13412     = events.cosPhi13412
		cosPhi31234     = events.cosPhi31234

		scale = 1265*puWeight*lumiWeight
		#if ( jet1Mass > 400 ) or ( jet2Mass > 400 ): print 'Entry ', Run, ':', Lumi, ':', NumEvent
		#if ( Lumi != tmpLumi ):
		#	newLumi += Lumi
		#	tmpLumi == Lumi
		#print Run/float(Lumi), Run, Lumi, Run/float(newLumi)
		
		#### Optimization
		deltaEtaDijet = abs( jet1Eta - jet2Eta )
		h_deltaEtaDijet.Fill( deltaEtaDijet, scale )
		
		h_jet2Tau21.Fill( jet2Tau21, scale )
		h_jet2Tau31.Fill( jet2Tau31, scale )
		
		#### TEST
		trimmedMassVsHT.Fill( trimmedMass, HT )

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )  
		HTCut = ( HT > 900 )
		dijetCut =  ( numJets > 1 )
		subjetPtRatioCut = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		tau21Cut = ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) )
		tau31Cut = ( ( jet1Tau31 < 0.4 ) and ( jet2Tau31 < 0.4 ) )
		massAsymCut = ( massAsym < 0.1 ) 
		deltaEtaDijetCut = ( deltaEtaDijet < 1. ) 
		#cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		cosThetaStarCut = ( abs( J1CosThetaStar ) < 0.3 )  and ( abs( J2CosThetaStar ) < 0.3 )
		jetPtCut =  ( jet1Pt > 500 ) and ( jet2Pt > 450 )
		
		if ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) ): massAve_Tau2106.Fill( massAve, scale )

		#if HTCut and jetPtCut:
		if HTCut and dijetCut:
			if massAsymCut:
				if ( ( jet1Tau21 < 0.4 ) and ( jet2Tau21 < 0.4 ) ): massAve_Tau2104.Fill( massAve, scale )
				if ( ( jet1Tau21 < 0.5 ) and ( jet2Tau21 < 0.5 ) ): massAve_Tau2105.Fill( massAve, scale )
				if ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) ): massAve_Tau2106.Fill( massAve, scale )
				if ( ( jet1Tau21 < 0.7 ) and ( jet2Tau21 < 0.7 ) ): massAve_Tau2107.Fill( massAve, scale )
				if ( ( jet1Tau31 < 0.4 ) and ( jet2Tau31 < 0.4 ) ): massAve_Tau3104.Fill( massAve, scale )
				if ( ( jet1Tau31 < 0.5 ) and ( jet2Tau31 < 0.5 ) ): massAve_Tau3105.Fill( massAve, scale )
				if ( ( jet1Tau31 < 0.6 ) and ( jet2Tau31 < 0.6 ) ): massAve_Tau3106.Fill( massAve, scale )
				if ( ( jet1Tau31 < 0.7 ) and ( jet2Tau31 < 0.7 ) ): massAve_Tau3107.Fill( massAve, scale )
			else:
				if ( ( jet1Tau21 < 0.4 ) and ( jet2Tau21 < 0.4 ) ): massAve_NOMATau2104.Fill( massAve, scale )
				if ( ( jet1Tau21 < 0.5 ) and ( jet2Tau21 < 0.5 ) ): massAve_NOMATau2105.Fill( massAve, scale )
				if ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) ): massAve_NOMATau2106.Fill( massAve, scale )
				if ( ( jet1Tau21 < 0.7 ) and ( jet2Tau21 < 0.7 ) ): massAve_NOMATau2107.Fill( massAve, scale )

				if ( ( jet1Tau31 < 0.4 ) and ( jet2Tau31 < 0.4 ) ): massAve_NOMATau3104.Fill( massAve, scale )
				if ( ( jet1Tau31 < 0.5 ) and ( jet2Tau31 < 0.5 ) ): massAve_NOMATau3105.Fill( massAve, scale )
				if ( ( jet1Tau31 < 0.6 ) and ( jet2Tau31 < 0.6 ) ): massAve_NOMATau3106.Fill( massAve, scale )
				if ( ( jet1Tau31 < 0.7 ) and ( jet2Tau31 < 0.7 ) ): massAve_NOMATau3107.Fill( massAve, scale )
		'''		
				if tau21Cut:
					massAve_Tau21.Fill( massAve, scale )
					if cosThetaStarCut:
						massAve_Tau21CosTheta.Fill( massAve, scale )
						if deltaEtaDijetCut:
							massAve_Tau21CosThetaDEta.Fill( massAve, scale )
						else:
							massAve_Tau21CosThetaNODEta.Fill( massAve, scale )

					else: 
						massAve_Tau21NOCosTheta.Fill( massAve, scale )
						if deltaEtaDijetCut:
							massAve_Tau21NOCosThetaDEta.Fill( massAve, scale )
						else:
							massAve_Tau21NOCosThetaNODEta.Fill( massAve, scale )
				else:
					massAve_NOTau21.Fill( massAve, scale )
					if tau31Cut:
						massAve_NOTau21Tau31.Fill( massAve, scale )
						if cosThetaStarCut:
							massAve_NOTau21Tau31CosTheta.Fill( massAve, scale )
					if cosThetaStarCut:
						massAve_NOTau21CosTheta.Fill( massAve, scale )
						if deltaEtaDijetCut:
							massAve_NOTau21CosThetaDEta.Fill( massAve, scale )
							if subjetPtRatioCut:
								massAve_NOTau21CosThetaDEtaSubPtRatio.Fill( massAve, scale )
			else:
				massAve_NOMassAsym.Fill( massAve, scale )
				if tau21Cut and cosThetaStarCut and deltaEtaDijetCut: massAve_NOMassAsymTau21CosThetaDEta.Fill( massAve, scale )
				if tau21Cut and cosThetaStarCut and deltaEtaDijetCut and subjetPtRatioCut: massAve_NOMassAsymTau21CosThetaDEtaSubPtRatio.Fill( massAve, scale )
				if tau21Cut : massAve_NOMassAsymTau21.Fill( massAve, scale )
				if cosThetaStarCut: massAve_NOMassAsymNOCosTheta.Fill( massAve, scale )
				if tau31Cut : 
					massAve_NOMassAsymTau31.Fill( massAve, scale )
					if cosThetaStarCut: 
						massAve_NOMassAsymTau31CosTheta.Fill( massAve, scale )
						if deltaEtaDijetCut: 
							massAve_NOMassAsymTau31CosThetaDEta.Fill( massAve, scale )
		'''



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
		inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15MiniAODv2-74X_'+PU+'_v08_v02.root'
		myAnalyzer( inputFileName, couts, grooming )
	elif 'Data' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_JetHTRun2015D-PromptReco-v4_v08_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
	elif 'Bkg' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIISpring15MiniAODv2-74X_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600ToInf_RunIISpring15MiniAODv2-74X_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_TTJets_RunIISpring15MiniAODv2-74X_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
	else: 
		#for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800', '1800to2400', '2400to3200', '3200toInf' ]: 
		#nputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15MiniAODv2-74X_'+PU+'_v08_v01.root'
		#myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15MiniAODv2-74X_Asympt25ns_v08_v02.root'
		myAnalyzer( inputFileName, couts, grooming )

