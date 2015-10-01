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
	massAve_Tau21 	= TH1F('massAve_Tau21', 'massAve_Tau21', nBinsMass, 0, maxMass )
	massAve_Tau21CosTheta 	= TH1F('massAve_Tau21CosTheta', 'massAve_Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Tau21Tau31 	= TH1F('massAve_Tau21Tau31', 'massAve_Tau21Tau31', nBinsMass, 0, maxMass )
	massAve_Tau21Tau31CosTheta 	= TH1F('massAve_Tau21Tau31CosTheta', 'massAve_Tau21Tau31CosTheta', nBinsMass, 0, maxMass )
	massAve_Tau21CosThetaDEta 	= TH1F('massAve_Tau21CosThetaDEta', 'massAve_Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	massAve_EffStandard 	= TH1F('massAve_EffStandard', 'massAve_EffStandard', nBinsMass, 0, maxMass )
	massAve_NOMassAsym 	= TH1F('massAve_NOMassAsym', 'massAve_NOMassAsym', nBinsMass, 0, maxMass )
	massAve_NOTau21 	= TH1F('massAve_NOTau21', 'massAve_NOTau21', nBinsMass, 0, maxMass )
	massAve_MassAsymNOTau21 	= TH1F('massAve_MassAsymNOTau21', 'massAve_MassAsymNOTau21', nBinsMass, 0, maxMass )
	massAve_NOCosTheta 	= TH1F('massAve_NOCosTheta', 'massAve_NOCosTheta', nBinsMass, 0, maxMass )
	massAve_NODEta 	= TH1F('massAve_NODEta', 'massAve_NODEta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymYesCosThetaDEta 	= TH1F('massAve_NOMassAsymYesCosThetaDEta', 'massAve_NOMassAsymYesCosThetaDEta', nBinsMass, 0, maxMass )
	massAve_DEtaNOTau21 	= TH1F('massAve_DEtaNOTau21', 'massAve_DEtaNOTau21', nBinsMass, 0, maxMass )
	
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
	'''
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
	'''


	###################################### Get GenTree 
	events = inputFile.Get( 'RUNATree'+grooming+'/RUNATree' )
	numEntries = events.GetEntriesFast()

	print '------> Number of events: '+str(numEntries)
	d = 0
	eventsRaw = eventsHT = eventsPassed = eventsDijet = eventsMassAsym = eventsDEta = eventsDEtaSubjet = eventsDEtaTau21 = eventsDEtaTau31 = eventsCosTheta = eventsTau21 = eventsTau21CosTheta = eventsTau21CosThetaDEta = 0
	#scale = SF(sample)*1000
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
		jet2Tau21       = events.jet2Tau21
		jet2Tau31       = events.jet2Tau31
		jet2Tau32       = events.jet2Tau32
		cosPhi13412     = events.cosPhi13412
		cosPhi31234     = events.cosPhi31234

		#if ( jet1Mass > 400 ) or ( jet2Mass > 400 ): print 'Entry ', Run, ':', Lumi, ':', NumEvent

		
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
		J1 = TLorentzVector()
		J1.SetPtEtaPhiE( jet1Pt, jet1Eta, jet1Phi, jet1E )
		J2 = TLorentzVector()
		J2.SetPtEtaPhiE( jet2Pt, jet2Eta, jet2Phi, jet2E )
		tmpCM = J1 + J2
		J2.Boost( -tmpCM.BoostVector() )
		J2CosThetaStar = abs( ( J2.Px() * tmpCM.Px() +  J2.Py() * tmpCM.Py() + J2.Pz() * tmpCM.Pz() ) / (J2.E() * tmpCM.E() ) ) 

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )  
		HTCut = ( HT > 800 )
		dijetCut =  ( numJets > 1 )
		subjetPtRatioCut = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		tau21Cut = ( ( jet1Tau21 < 0.4 ) and ( jet2Tau21 < 0.4 ) )
		tau31Cut = ( ( jet1Tau31 < 0.3 ) and ( jet2Tau31 < 0.3 ) )
		massAsymCut = ( massAsym < 0.1 ) 
		deltaEtaDijetCut = ( deltaEtaDijet < 1. ) 
		#cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 )  and ( abs( J2CosThetaStar ) < 0.3 )
		jetPtCut =  ( jet1Pt > 200 ) and ( jet2Pt > 200 )

		if HTCut:
			eventsHT += 1
			if dijetCut:
				eventsDijet += 1
				if massAsymCut:
					eventsMassAsym += 1
					if tau21Cut: 
						eventsTau21 += 1
						massAve_Tau21.Fill( massAve, scale )
						if cosThetaStarCut:
							eventsTau21CosTheta += 1
							massAve_Tau21CosTheta.Fill( massAve, scale )
							if deltaEtaDijetCut:
								eventsTau21CosThetaDEta += 1
								massAve_Tau21CosThetaDEta.Fill( massAve, scale )
						if tau31Cut:
							massAve_Tau21Tau31.Fill( massAve, scale )
							if cosThetaStarCut:
								massAve_Tau21Tau31CosTheta.Fill( massAve, scale )
				'''
					else: 
						massAve_MassAsymNOTau21.Fill( massAve, scale )
						if cosThetaStarCut and deltaEtaDijetCut:
							massAve_DEtaNOTau21.Fill( massAve, scale )
				else:
					massAve_NOMassAsym.Fill( massAve, scale )
					if not tau21Cut: 
						massAve_NOTau21.Fill( massAve, scale )
						if not cosThetaStarCut:
							massAve_NOCosTheta.Fill( massAve, scale )
							if not deltaEtaDijetCut:
								massAve_NODEta.Fill( massAve, scale )
					elif cosThetaStarCut and deltaEtaDijetCut:
						massAve_NOMassAsymYesCosThetaDEta.Fill( massAve, scale )
				'''

		if ( ( HT > 700 ) and ( trimmedMass > 50 ) ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			massAve_EffStandard.Fill( massAve, scale )
		
		if ( AK4HT > 800 ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			AK4HT_PFHT800.Fill( AK4HT, scale )
			massAve_PFHT800.Fill( massAve, scale )

		if ( AK4HT > 900 ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			AK4HT_EffPFHT800.Fill( AK4HT, scale )
			massAve_EffPFHT800.Fill( massAve, scale )

		if ( AK4HT > 1600 ) and massAsymCut and cosThetaStarCut and subjetPtRatioCut:
			AK4HT_Brock.Fill( AK4HT, scale )
			massAve_Brock.Fill( massAve, scale )

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
		inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15DR74_'+PU+'_v03_v01p3.root'
		myAnalyzer( inputFileName, couts, grooming )
	elif 'Data' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_JetHT_Run2015C_Asympt25ns_v03_v01p3.root'
		myAnalyzer( inputFileName, couts, grooming )
	elif 'Bkg' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_TTJets_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		myAnalyzer( inputFileName, couts, grooming )
	else: 
		#for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800' ]: 
		#	inputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15DR74_'+PU+'_v01_v07.root'
		#	myAnalyzer( inputFileName, couts, grooming )
		inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15DR74_Asympt25ns_v03_v01p3.root'
		myAnalyzer( inputFileName, couts, grooming )

