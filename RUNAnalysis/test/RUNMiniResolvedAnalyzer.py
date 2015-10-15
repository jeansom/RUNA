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
	massAve_DeltaEtaSubjet 	= TH1F('massAve_DeltaEtaSubjet', 'massAve_DeltaEtaSubjet', nBinsMass, 0, maxMass )
	massAve_DeltaEtaTau21 	= TH1F('massAve_DeltaEtaTau21', 'massAve_DeltaEtaTau21', nBinsMass, 0, maxMass )
	massAve_DeltaEtaTau31 	= TH1F('massAve_DeltaEtaTau31', 'massAve_DeltaEtaTau31', nBinsMass, 0, maxMass )
	massAve_MassAsym 	= TH1F('massAve_MassAsym', 'massAve_MassAsym', nBinsMass, 0, maxMass )
	massAve_Tau21 	= TH1F('massAve_Tau21', 'massAve_Tau21', nBinsMass, 0, maxMass )
	massAve_Tau21CosTheta 	= TH1F('massAve_Tau21CosTheta', 'massAve_Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Tau21Tau31 	= TH1F('massAve_Tau21Tau31', 'massAve_Tau21Tau31', nBinsMass, 0, maxMass )
	massAve_Tau21Tau31CosTheta 	= TH1F('massAve_Tau21Tau31CosTheta', 'massAve_Tau21Tau31CosTheta', nBinsMass, 0, maxMass )
	massAve_Tau21CosThetaDEta 	= TH1F('massAve_Tau21CosThetaDEta', 'massAve_Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	massAve_EffStandard 	= TH1F('massAve_EffStandard', 'massAve_EffStandard', nBinsMass, 0, maxMass )
	massAve_Tau21NOCosTheta 	= TH1F('massAve_Tau21NOCosTheta', 'massAve_Tau21NOCosTheta', nBinsMass, 0, maxMass )
	massAve_MassAsymNOTau21 	= TH1F('massAve_MassAsymNOTau21', 'massAve_MassAsymNOTau21', nBinsMass, 0, maxMass )
	massAve_CosThetaNOTau21 	= TH1F('massAve_CosThetaNOTau21', 'massAve_CosThetaNOTau21', nBinsMass, 0, maxMass )
	
	AK4HT_PFHT800 	= TH1F('AK4HT_PFHT800', 'AK4HT_PFHT800', nBinsHT, 0, maxHT )
	massAve_PFHT800 	= TH1F('massAve_PFHT800', 'massAve_PFHT800', nBinsMass, 0, maxMass )
	AK4HT_EffPFHT800 	= TH1F('AK4HT_EffPFHT800', 'AK4HT_EffPFHT800', nBinsHT, 0, maxHT )
	massAve_EffPFHT800 	= TH1F('massAve_EffPFHT800', 'massAve_EffPFHT800', nBinsMass, 0, maxMass )

	AK4HT_Brock 	= TH1F('AK4HT_Brock', 'AK4HT_Brock', 200, 0, 2000 )
	massAve_Brock 	= TH1F('massAve_Brock', 'massAve_Brock', nBinsMass, 0, maxMass )

	#### Optimization
	h_deltaEtaDijet 	= TH1F('deltaEtaDijet', 'deltaEtaDijet', 100, 0, 5. )
	h_jet2Tau21 	= TH1F('jet2Tau21', 'jet2Tau21', 10, 0, 1. )
	h_jet2Tau31 	= TH1F('jet2Tau31', 'jet2Tau31', 10, 0, 1. )
	jet1Pt_cutHT 	= TH1F('jet1Pt_cutHT', 'jet1Pt_cutHT', 100, 0, 1000. )
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
	scale = SF(sample)*149.9
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
		jet2Tau21       = events.jet2Tau21
		jet2Tau31       = events.jet2Tau31
		jet2Tau32       = events.jet2Tau32
		cosPhi13412     = events.cosPhi13412
		cosPhi31234     = events.cosPhi31234

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
		
		'''
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
		'''

		#### TEST
		trimmedMassVsHT.Fill( trimmedMass, HT )

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )  
		HTCut = ( HT > 800 )
		dijetCut =  ( numJets > 1 )
		subjetPtRatioCut = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		tau21Cut = ( ( jet1Tau21 < 0.5 ) and ( jet2Tau21 < 0.5 ) )
		tau31Cut = ( ( jet1Tau31 < 0.3 ) and ( jet2Tau31 < 0.3 ) )
		massAsymCut = ( massAsym < 0.1 ) 
		deltaEtaDijetCut = ( deltaEtaDijet < 1. ) 
		#cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		cosThetaStarCut = ( abs( J1CosThetaStar ) < 0.3 )  and ( abs( J2CosThetaStar ) < 0.3 )
		jetPtCut =  ( jet1Pt > 400 ) and ( jet2Pt > 400 )

		#if HTCut and jetPtCut:
		if jetPtCut:
			eventsHT += 1
			jet1Pt_cutHT.Fill( jet1Pt, scale )
			jet2Pt_cutHT.Fill( jet2Pt, scale )
			if dijetCut:
				eventsDijet += 1
				if massAsymCut:
					eventsMassAsym += 1
					massAve_MassAsym.Fill( massAve, scale )
					if tau21Cut: 
						eventsTau21 += 1
						massAve_Tau21.Fill( massAve, scale )
						if cosThetaStarCut:
							eventsTau21CosTheta += 1
							massAve_Tau21CosTheta.Fill( massAve, scale )
							jet1Pt_Tau21CosTheta.Fill( jet1Pt, scale )
							jet2Pt_Tau21CosTheta.Fill( jet2Pt, scale )
							if deltaEtaDijetCut:
								eventsTau21CosThetaDEta += 1
								massAve_Tau21CosThetaDEta.Fill( massAve, scale )
						else:
							massAve_Tau21NOCosTheta.Fill( massAve, scale )

					else: 
						massAve_MassAsymNOTau21.Fill( massAve, scale )
						if cosThetaStarCut:
							massAve_CosThetaNOTau21.Fill( massAve, scale )


	cutFlowStandard = [ eventsRaw, eventsHT, eventsDijet, eventsMassAsym, eventsCosTheta, eventsPassed ]
	cutFlowDEtaSubjet = [ eventsRaw, eventsHT, eventsDijet, eventsMassAsym, eventsDEta, eventsDEtaSubjet ]
	cutFlowDEtaTau21 = [ eventsRaw, eventsHT, eventsDijet, eventsMassAsym, eventsDEta, eventsDEtaTau21 ]
	cutFlowDEtaTau31 = [ eventsRaw, eventsHT, eventsDijet, eventsMassAsym, eventsDEta, eventsDEtaTau31 ]
	cutFlowMassAsymTau21CosThetaDEta = [ eventsRaw, eventsHT, eventsDijet, eventsMassAsym, eventsTau21, eventsTau21CosTheta, eventsTau21CosThetaDEta ]

	print eventsPassed
	
	hcutFlowmassStandard 	= TH1F('cutFlowStandard', 'cutFlowStandard', len(cutFlowStandard), 0, len(cutFlowStandard) )
	for i in range( len(cutFlowStandard) ): hcutFlowmassStandard.SetBinContent(i, cutFlowStandard[i])
	hcutFlowmassDEtaSubjet 	= TH1F('cutFlowDEtaSubjet', 'cutFlowDEtaSubjet', len(cutFlowDEtaSubjet), 0, len(cutFlowDEtaSubjet) )
	for i in range( len(cutFlowDEtaSubjet) ): hcutFlowmassDEtaSubjet.SetBinContent(i, cutFlowDEtaSubjet[i])
	hcutFlowmassDEtaTau21 	= TH1F('cutFlowDEtaTau21', 'cutFlowDEtaTau21', len(cutFlowDEtaTau21), 0, len(cutFlowDEtaTau21) )
	for i in range( len(cutFlowDEtaTau21) ): hcutFlowmassDEtaTau21.SetBinContent(i, cutFlowDEtaTau21[i])
	hcutFlowmassDEtaTau31 	= TH1F('cutFlowDEtaTau31', 'cutFlowDEtaTau31', len(cutFlowDEtaTau31), 0, len(cutFlowDEtaTau31) )
	for i in range( len(cutFlowDEtaTau31) ): hcutFlowmassDEtaTau31.SetBinContent(i, cutFlowDEtaTau31[i])
	hcutFlowmassMassAsymTau21CosThetaDEta 	= TH1F('cutFlowMassAsymTau21CosThetaDEta', 'cutFlowMassAsymTau21CosThetaDEta', len(cutFlowMassAsymTau21CosThetaDEta), 0, len(cutFlowMassAsymTau21CosThetaDEta) )
	for i in range( len(cutFlowMassAsymTau21CosThetaDEta) ): hcutFlowmassMassAsymTau21CosThetaDEta.SetBinContent(i, cutFlowMassAsymTau21CosThetaDEta[i])


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
		inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15DR74_'+PU+'_v06_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
	elif 'Data' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_JetHTRun2015D-PromptReco-v3_v06_v00p2.root'
		myAnalyzer( inputFileName, couts, grooming )
	elif 'Bkg' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_TTJets_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
	else: 
		for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800', '1800to2400', '2400to3200', '3200toInf' ]: 
			inputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15DR74_'+PU+'_v06p1_v01.root'
			myAnalyzer( inputFileName, couts, grooming )
		#inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15DR74_Asympt25ns_v06_v00p2.root'
		#myAnalyzer( inputFileName, couts, grooming )

