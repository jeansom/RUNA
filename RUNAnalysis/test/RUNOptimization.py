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
import numpy as np
from RUNA.RUNAnalysis.scaleFactors import scaleFactor as SF

gROOT.SetBatch()
range01 = np.arange(0,1.1,0.1)

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

	dictMassAsym = {}
	dictDeltaEta = {}
	dictJ1CosTheta = {}
	dictJ2CosTheta = {}
	dictJ1Tau21 = {}
	dictJ2Tau21 = {}
	dictJ1Tau31 = {}
	dictJ2Tau31 = {}
	dictJ1SubjetPtRatio = {}
	dictJ2SubjetPtRatio = {}
	
	dictMA_DeltaEta = {}
	dictMA_J1CosTheta = {}
	dictMA_J2CosTheta = {}
	dictMA_J1Tau21 = {}
	dictMA_J2Tau21 = {}
	dictMA_J1Tau31 = {}
	dictMA_J2Tau31 = {}
	dictMA_J1SubjetPtRatio = {}
	dictMA_J2SubjetPtRatio = {}
	
	dictMAT21_DeltaEta = {}
	dictMAT21_J1CosTheta = {}
	dictMAT21_J2CosTheta = {}
	dictMAT21_J1Tau31 = {}
	dictMAT21_J2Tau31 = {}
	dictMAT21_J1SubjetPtRatio = {}
	dictMAT21_J2SubjetPtRatio = {}
	
	dictMAT21CTS_DeltaEta = {}
	dictMAT21CTS_J1Tau31 = {}
	dictMAT21CTS_J2Tau31 = {}
	dictMAT21CTS_J1SubjetPtRatio = {}
	dictMAT21CTS_J2SubjetPtRatio = {}

	for i in range (0, 11):
		dictMassAsym[ i ] = 0
		dictDeltaEta[ i ] = 0
		dictJ1CosTheta[ i ] = 0
		dictJ2CosTheta[ i ] = 0
		dictJ1Tau21[ i ] = 0
		dictJ2Tau21[ i ] = 0
		dictJ1Tau31[ i ] = 0
		dictJ2Tau31[ i ] = 0
		dictJ1SubjetPtRatio[ i ] = 0
		dictJ2SubjetPtRatio[ i ] = 0

		dictMA_DeltaEta[ i ] = 0
		dictMA_J1CosTheta[ i ] = 0
		dictMA_J2CosTheta[ i ] = 0
		dictMA_J1Tau21[ i ] = 0
		dictMA_J2Tau21[ i ] = 0
		dictMA_J1Tau31[ i ] = 0
		dictMA_J2Tau31[ i ] = 0
		dictMA_J1SubjetPtRatio[ i ] = 0
		dictMA_J2SubjetPtRatio[ i ] = 0

		dictMAT21_DeltaEta[ i ] = 0
		dictMAT21_J1CosTheta[ i ] = 0
		dictMAT21_J2CosTheta[ i ] = 0
		dictMAT21_J1Tau31[ i ] = 0
		dictMAT21_J2Tau31[ i ] = 0
		dictMAT21_J1SubjetPtRatio[ i ] = 0
		dictMAT21_J2SubjetPtRatio[ i ] = 0

		dictMAT21CTS_DeltaEta[ i ] = 0
		dictMAT21CTS_J1Tau31[ i ] = 0
		dictMAT21CTS_J2Tau31[ i ] = 0
		dictMAT21CTS_J1SubjetPtRatio[ i ] = 0
		dictMAT21CTS_J2SubjetPtRatio[ i ] = 0

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
		cosThetaStar	= abs( events.cosThetaStar )
		jet1SubjetPtRatio	= events.jet1SubjetPtRatio
		jet2SubjetPtRatio	= events.jet2SubjetPtRatio
		scale		= events.Scale
#		numPV           = events.numPV
#		AK4HT           = events.AK4HT
		jet1Pt          = events.jet1Pt
		jet1Eta         = events.jet1Eta
		jet1Phi         = events.jet1Phi
		jet1E           = events.jet1E
#		jet1Mass        = events.jet1Mass
		jet2Pt          = events.jet2Pt
		jet2Eta         = events.jet2Eta
		jet2Phi         = events.jet2Phi
		jet2E           = events.jet2E
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
		J1 = TLorentzVector()
		J1.SetPtEtaPhiE( jet1Pt, jet1Eta, jet1Phi, jet1E )
		J2 = TLorentzVector()
		J2.SetPtEtaPhiE( jet2Pt, jet2Eta, jet2Phi, jet2E )
		tmpCM = J1 + J2
		J2.Boost( -tmpCM.BoostVector() )
		J2CosThetaStar = abs( ( J2.Px() * tmpCM.Px() +  J2.Py() * tmpCM.Py() + J2.Pz() * tmpCM.Pz() ) / (J2.E() * tmpCM.E() ) ) 

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )
		dijetCut = ( numJets > 1 )   
		subjetPtRatio = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		tau21Cut = ( ( jet1Tau21 < 0.4 ) and ( jet2Tau21 < 0.4 )  )
		tau31Cut = ( ( jet1Tau31 < 0.3 ) and ( jet2Tau31 < 0.3 )  )
		massAsymCut = ( massAsym < 0.1 ) 
		cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) and ( J2CosThetaStar < 0.3 )
		subjetPtRatioCut = ( subjetPtRatio ) 
		deltaEtaCut = ( deltaEtaDijet > 1.0 )


		##### For Optimization:
		eventsAfterTrigger +=1

		if dijetCut:

			if ( massAsym <= 0.0 ): dictMassAsym[ 0 ] += scale
			if ( massAsym <= 0.1 ): dictMassAsym[ 1 ] += scale
			if ( massAsym <= 0.2 ): dictMassAsym[ 2 ] += scale
			if ( massAsym <= 0.3 ): dictMassAsym[ 3 ] += scale
			if ( massAsym <= 0.4 ): dictMassAsym[ 4 ] += scale
			if ( massAsym <= 0.5 ): dictMassAsym[ 5 ] += scale
			if ( massAsym <= 0.6 ): dictMassAsym[ 6 ] += scale
			if ( massAsym <= 0.7 ): dictMassAsym[ 7 ] += scale
			if ( massAsym <= 0.8 ): dictMassAsym[ 8 ] += scale
			if ( massAsym <= 0.9 ): dictMassAsym[ 9 ] += scale
			if ( massAsym <= 1.0 ): dictMassAsym[ 10 ] += scale
		
			if ( deltaEtaDijet >= 0.0 ): dictDeltaEta[ 0 ] += scale
			if ( deltaEtaDijet >= 0.5 ): dictDeltaEta[ 1 ] += scale
			if ( deltaEtaDijet >= 1.0 ): dictDeltaEta[ 2 ] += scale
			if ( deltaEtaDijet >= 1.5 ): dictDeltaEta[ 3 ] += scale
			if ( deltaEtaDijet >= 2.0 ): dictDeltaEta[ 4 ] += scale
			if ( deltaEtaDijet >= 2.5 ): dictDeltaEta[ 5 ] += scale
			if ( deltaEtaDijet >= 3.0 ): dictDeltaEta[ 6 ] += scale
			if ( deltaEtaDijet >= 3.5 ): dictDeltaEta[ 7 ] += scale
			if ( deltaEtaDijet >= 4.0 ): dictDeltaEta[ 8 ] += scale
			if ( deltaEtaDijet >= 4.5 ): dictDeltaEta[ 9 ] += scale
			if ( deltaEtaDijet >= 5.0 ): dictDeltaEta[ 10 ] += scale
		
			if ( cosThetaStar <= 0.0 ): dictJ1CosTheta[ 0 ] += scale
			if ( cosThetaStar <= 0.1 ): dictJ1CosTheta[ 1 ] += scale
			if ( cosThetaStar <= 0.2 ): dictJ1CosTheta[ 2 ] += scale
			if ( cosThetaStar <= 0.3 ): dictJ1CosTheta[ 3 ] += scale
			if ( cosThetaStar <= 0.4 ): dictJ1CosTheta[ 4 ] += scale
			if ( cosThetaStar <= 0.5 ): dictJ1CosTheta[ 5 ] += scale
			if ( cosThetaStar <= 0.6 ): dictJ1CosTheta[ 6 ] += scale
			if ( cosThetaStar <= 0.7 ): dictJ1CosTheta[ 7 ] += scale
			if ( cosThetaStar <= 0.8 ): dictJ1CosTheta[ 8 ] += scale
			if ( cosThetaStar <= 0.9 ): dictJ1CosTheta[ 9 ] += scale
			if ( cosThetaStar <= 1.0 ): dictJ1CosTheta[ 10 ] += scale
		
			if ( J2CosThetaStar <= 0.0 ): dictJ2CosTheta[ 0 ] += scale
			if ( J2CosThetaStar <= 0.1 ): dictJ2CosTheta[ 1 ] += scale
			if ( J2CosThetaStar <= 0.2 ): dictJ2CosTheta[ 2 ] += scale
			if ( J2CosThetaStar <= 0.3 ): dictJ2CosTheta[ 3 ] += scale
			if ( J2CosThetaStar <= 0.4 ): dictJ2CosTheta[ 4 ] += scale
			if ( J2CosThetaStar <= 0.5 ): dictJ2CosTheta[ 5 ] += scale
			if ( J2CosThetaStar <= 0.6 ): dictJ2CosTheta[ 6 ] += scale
			if ( J2CosThetaStar <= 0.7 ): dictJ2CosTheta[ 7 ] += scale
			if ( J2CosThetaStar <= 0.8 ): dictJ2CosTheta[ 8 ] += scale
			if ( J2CosThetaStar <= 0.9 ): dictJ2CosTheta[ 9 ] += scale
			if ( J2CosThetaStar <= 1.0 ): dictJ2CosTheta[ 10 ] += scale
		
			if ( jet1Tau21 <= 0.0 ): dictJ1Tau21[ 0 ] += scale
			if ( jet1Tau21 <= 0.1 ): dictJ1Tau21[ 1 ] += scale
			if ( jet1Tau21 <= 0.2 ): dictJ1Tau21[ 2 ] += scale
			if ( jet1Tau21 <= 0.3 ): dictJ1Tau21[ 3 ] += scale
			if ( jet1Tau21 <= 0.4 ): dictJ1Tau21[ 4 ] += scale
			if ( jet1Tau21 <= 0.5 ): dictJ1Tau21[ 5 ] += scale
			if ( jet1Tau21 <= 0.6 ): dictJ1Tau21[ 6 ] += scale
			if ( jet1Tau21 <= 0.7 ): dictJ1Tau21[ 7 ] += scale
			if ( jet1Tau21 <= 0.8 ): dictJ1Tau21[ 8 ] += scale
			if ( jet1Tau21 <= 0.9 ): dictJ1Tau21[ 9 ] += scale
			if ( jet1Tau21 <= 1.0 ): dictJ1Tau21[ 10 ] += scale
		
			if ( jet2Tau21 <= 0.0 ): dictJ2Tau21[ 0 ] += scale
			if ( jet2Tau21 <= 0.1 ): dictJ2Tau21[ 1 ] += scale
			if ( jet2Tau21 <= 0.2 ): dictJ2Tau21[ 2 ] += scale
			if ( jet2Tau21 <= 0.3 ): dictJ2Tau21[ 3 ] += scale
			if ( jet2Tau21 <= 0.4 ): dictJ2Tau21[ 4 ] += scale
			if ( jet2Tau21 <= 0.5 ): dictJ2Tau21[ 5 ] += scale
			if ( jet2Tau21 <= 0.6 ): dictJ2Tau21[ 6 ] += scale
			if ( jet2Tau21 <= 0.7 ): dictJ2Tau21[ 7 ] += scale
			if ( jet2Tau21 <= 0.8 ): dictJ2Tau21[ 8 ] += scale
			if ( jet2Tau21 <= 0.9 ): dictJ2Tau21[ 9 ] += scale
			if ( jet2Tau21 <= 1.0 ): dictJ2Tau21[ 10 ] += scale

			if ( jet1Tau31 <= 0.0 ): dictJ1Tau31[ 0 ] += scale
			if ( jet1Tau31 <= 0.1 ): dictJ1Tau31[ 1 ] += scale
			if ( jet1Tau31 <= 0.2 ): dictJ1Tau31[ 2 ] += scale
			if ( jet1Tau31 <= 0.3 ): dictJ1Tau31[ 3 ] += scale
			if ( jet1Tau31 <= 0.4 ): dictJ1Tau31[ 4 ] += scale
			if ( jet1Tau31 <= 0.5 ): dictJ1Tau31[ 5 ] += scale
			if ( jet1Tau31 <= 0.6 ): dictJ1Tau31[ 6 ] += scale
			if ( jet1Tau31 <= 0.7 ): dictJ1Tau31[ 7 ] += scale
			if ( jet1Tau31 <= 0.8 ): dictJ1Tau31[ 8 ] += scale
			if ( jet1Tau31 <= 0.9 ): dictJ1Tau31[ 9 ] += scale
			if ( jet1Tau31 <= 1.0 ): dictJ1Tau31[ 10 ] += scale
		
			if ( jet2Tau31 <= 0.0 ): dictJ2Tau31[ 0 ] += scale
			if ( jet2Tau31 <= 0.1 ): dictJ2Tau31[ 1 ] += scale
			if ( jet2Tau31 <= 0.2 ): dictJ2Tau31[ 2 ] += scale
			if ( jet2Tau31 <= 0.3 ): dictJ2Tau31[ 3 ] += scale
			if ( jet2Tau31 <= 0.4 ): dictJ2Tau31[ 4 ] += scale
			if ( jet2Tau31 <= 0.5 ): dictJ2Tau31[ 5 ] += scale
			if ( jet2Tau31 <= 0.6 ): dictJ2Tau31[ 6 ] += scale
			if ( jet2Tau31 <= 0.7 ): dictJ2Tau31[ 7 ] += scale
			if ( jet2Tau31 <= 0.8 ): dictJ2Tau31[ 8 ] += scale
			if ( jet2Tau31 <= 0.9 ): dictJ2Tau31[ 9 ] += scale
			if ( jet2Tau31 <= 1.0 ): dictJ2Tau31[ 10 ] += scale

			if ( jet1SubjetPtRatio <= 0.0 ): dictJ1SubjetPtRatio[ 0 ] += scale
			if ( jet1SubjetPtRatio <= 0.1 ): dictJ1SubjetPtRatio[ 1 ] += scale
			if ( jet1SubjetPtRatio <= 0.2 ): dictJ1SubjetPtRatio[ 2 ] += scale
			if ( jet1SubjetPtRatio <= 0.3 ): dictJ1SubjetPtRatio[ 3 ] += scale
			if ( jet1SubjetPtRatio <= 0.4 ): dictJ1SubjetPtRatio[ 4 ] += scale
			if ( jet1SubjetPtRatio <= 0.5 ): dictJ1SubjetPtRatio[ 5 ] += scale
			if ( jet1SubjetPtRatio <= 0.6 ): dictJ1SubjetPtRatio[ 6 ] += scale
			if ( jet1SubjetPtRatio <= 0.7 ): dictJ1SubjetPtRatio[ 7 ] += scale
			if ( jet1SubjetPtRatio <= 0.8 ): dictJ1SubjetPtRatio[ 8 ] += scale
			if ( jet1SubjetPtRatio <= 0.9 ): dictJ1SubjetPtRatio[ 9 ] += scale
			if ( jet1SubjetPtRatio <= 1.0 ): dictJ1SubjetPtRatio[ 10 ] += scale
		
			if ( jet2SubjetPtRatio <= 0.0 ): dictJ2SubjetPtRatio[ 0 ] += scale
			if ( jet2SubjetPtRatio <= 0.1 ): dictJ2SubjetPtRatio[ 1 ] += scale
			if ( jet2SubjetPtRatio <= 0.2 ): dictJ2SubjetPtRatio[ 2 ] += scale
			if ( jet2SubjetPtRatio <= 0.3 ): dictJ2SubjetPtRatio[ 3 ] += scale
			if ( jet2SubjetPtRatio <= 0.4 ): dictJ2SubjetPtRatio[ 4 ] += scale
			if ( jet2SubjetPtRatio <= 0.5 ): dictJ2SubjetPtRatio[ 5 ] += scale
			if ( jet2SubjetPtRatio <= 0.6 ): dictJ2SubjetPtRatio[ 6 ] += scale
			if ( jet2SubjetPtRatio <= 0.7 ): dictJ2SubjetPtRatio[ 7 ] += scale
			if ( jet2SubjetPtRatio <= 0.8 ): dictJ2SubjetPtRatio[ 8 ] += scale
			if ( jet2SubjetPtRatio <= 0.9 ): dictJ2SubjetPtRatio[ 9 ] += scale
			if ( jet2SubjetPtRatio <= 1.0 ): dictJ2SubjetPtRatio[ 10 ] += scale

			if massAsymCut :
			
				if ( deltaEtaDijet >= 0.0 ): dictMA_DeltaEta[ 0 ] += scale
				if ( deltaEtaDijet >= 0.5 ): dictMA_DeltaEta[ 1 ] += scale
				if ( deltaEtaDijet >= 1.0 ): dictMA_DeltaEta[ 2 ] += scale
				if ( deltaEtaDijet >= 1.5 ): dictMA_DeltaEta[ 3 ] += scale
				if ( deltaEtaDijet >= 2.0 ): dictMA_DeltaEta[ 4 ] += scale
				if ( deltaEtaDijet >= 2.5 ): dictMA_DeltaEta[ 5 ] += scale
				if ( deltaEtaDijet >= 3.0 ): dictMA_DeltaEta[ 6 ] += scale
				if ( deltaEtaDijet >= 3.5 ): dictMA_DeltaEta[ 7 ] += scale
				if ( deltaEtaDijet >= 4.0 ): dictMA_DeltaEta[ 8 ] += scale
				if ( deltaEtaDijet >= 4.5 ): dictMA_DeltaEta[ 9 ] += scale
				if ( deltaEtaDijet >= 5.0 ): dictMA_DeltaEta[ 10 ] += scale
			
				if ( cosThetaStar <= 0.0 ): dictMA_J1CosTheta[ 0 ] += scale
				if ( cosThetaStar <= 0.1 ): dictMA_J1CosTheta[ 1 ] += scale
				if ( cosThetaStar <= 0.2 ): dictMA_J1CosTheta[ 2 ] += scale
				if ( cosThetaStar <= 0.3 ): dictMA_J1CosTheta[ 3 ] += scale
				if ( cosThetaStar <= 0.4 ): dictMA_J1CosTheta[ 4 ] += scale
				if ( cosThetaStar <= 0.5 ): dictMA_J1CosTheta[ 5 ] += scale
				if ( cosThetaStar <= 0.6 ): dictMA_J1CosTheta[ 6 ] += scale
				if ( cosThetaStar <= 0.7 ): dictMA_J1CosTheta[ 7 ] += scale
				if ( cosThetaStar <= 0.8 ): dictMA_J1CosTheta[ 8 ] += scale
				if ( cosThetaStar <= 0.9 ): dictMA_J1CosTheta[ 9 ] += scale
				if ( cosThetaStar <= 1.0 ): dictMA_J1CosTheta[ 10 ] += scale
			
				if ( J2CosThetaStar <= 0.0 ): dictMA_J2CosTheta[ 0 ] += scale
				if ( J2CosThetaStar <= 0.1 ): dictMA_J2CosTheta[ 1 ] += scale
				if ( J2CosThetaStar <= 0.2 ): dictMA_J2CosTheta[ 2 ] += scale
				if ( J2CosThetaStar <= 0.3 ): dictMA_J2CosTheta[ 3 ] += scale
				if ( J2CosThetaStar <= 0.4 ): dictMA_J2CosTheta[ 4 ] += scale
				if ( J2CosThetaStar <= 0.5 ): dictMA_J2CosTheta[ 5 ] += scale
				if ( J2CosThetaStar <= 0.6 ): dictMA_J2CosTheta[ 6 ] += scale
				if ( J2CosThetaStar <= 0.7 ): dictMA_J2CosTheta[ 7 ] += scale
				if ( J2CosThetaStar <= 0.8 ): dictMA_J2CosTheta[ 8 ] += scale
				if ( J2CosThetaStar <= 0.9 ): dictMA_J2CosTheta[ 9 ] += scale
				if ( J2CosThetaStar <= 1.0 ): dictMA_J2CosTheta[ 10 ] += scale
			
				if ( jet1Tau21 <= 0.0 ): dictMA_J1Tau21[ 0 ] += scale
				if ( jet1Tau21 <= 0.1 ): dictMA_J1Tau21[ 1 ] += scale
				if ( jet1Tau21 <= 0.2 ): dictMA_J1Tau21[ 2 ] += scale
				if ( jet1Tau21 <= 0.3 ): dictMA_J1Tau21[ 3 ] += scale
				if ( jet1Tau21 <= 0.4 ): dictMA_J1Tau21[ 4 ] += scale
				if ( jet1Tau21 <= 0.5 ): dictMA_J1Tau21[ 5 ] += scale
				if ( jet1Tau21 <= 0.6 ): dictMA_J1Tau21[ 6 ] += scale
				if ( jet1Tau21 <= 0.7 ): dictMA_J1Tau21[ 7 ] += scale
				if ( jet1Tau21 <= 0.8 ): dictMA_J1Tau21[ 8 ] += scale
				if ( jet1Tau21 <= 0.9 ): dictMA_J1Tau21[ 9 ] += scale
				if ( jet1Tau21 <= 1.0 ): dictMA_J1Tau21[ 10 ] += scale
			
				if ( jet2Tau21 <= 0.0 ): dictMA_J2Tau21[ 0 ] += scale
				if ( jet2Tau21 <= 0.1 ): dictMA_J2Tau21[ 1 ] += scale
				if ( jet2Tau21 <= 0.2 ): dictMA_J2Tau21[ 2 ] += scale
				if ( jet2Tau21 <= 0.3 ): dictMA_J2Tau21[ 3 ] += scale
				if ( jet2Tau21 <= 0.4 ): dictMA_J2Tau21[ 4 ] += scale
				if ( jet2Tau21 <= 0.5 ): dictMA_J2Tau21[ 5 ] += scale
				if ( jet2Tau21 <= 0.6 ): dictMA_J2Tau21[ 6 ] += scale
				if ( jet2Tau21 <= 0.7 ): dictMA_J2Tau21[ 7 ] += scale
				if ( jet2Tau21 <= 0.8 ): dictMA_J2Tau21[ 8 ] += scale
				if ( jet2Tau21 <= 0.9 ): dictMA_J2Tau21[ 9 ] += scale
				if ( jet2Tau21 <= 1.0 ): dictMA_J2Tau21[ 10 ] += scale

				if ( jet1Tau31 <= 0.0 ): dictMA_J1Tau31[ 0 ] += scale
				if ( jet1Tau31 <= 0.1 ): dictMA_J1Tau31[ 1 ] += scale
				if ( jet1Tau31 <= 0.2 ): dictMA_J1Tau31[ 2 ] += scale
				if ( jet1Tau31 <= 0.3 ): dictMA_J1Tau31[ 3 ] += scale
				if ( jet1Tau31 <= 0.4 ): dictMA_J1Tau31[ 4 ] += scale
				if ( jet1Tau31 <= 0.5 ): dictMA_J1Tau31[ 5 ] += scale
				if ( jet1Tau31 <= 0.6 ): dictMA_J1Tau31[ 6 ] += scale
				if ( jet1Tau31 <= 0.7 ): dictMA_J1Tau31[ 7 ] += scale
				if ( jet1Tau31 <= 0.8 ): dictMA_J1Tau31[ 8 ] += scale
				if ( jet1Tau31 <= 0.9 ): dictMA_J1Tau31[ 9 ] += scale
				if ( jet1Tau31 <= 1.0 ): dictMA_J1Tau31[ 10 ] += scale
			
				if ( jet2Tau31 <= 0.0 ): dictMA_J2Tau31[ 0 ] += scale
				if ( jet2Tau31 <= 0.1 ): dictMA_J2Tau31[ 1 ] += scale
				if ( jet2Tau31 <= 0.2 ): dictMA_J2Tau31[ 2 ] += scale
				if ( jet2Tau31 <= 0.3 ): dictMA_J2Tau31[ 3 ] += scale
				if ( jet2Tau31 <= 0.4 ): dictMA_J2Tau31[ 4 ] += scale
				if ( jet2Tau31 <= 0.5 ): dictMA_J2Tau31[ 5 ] += scale
				if ( jet2Tau31 <= 0.6 ): dictMA_J2Tau31[ 6 ] += scale
				if ( jet2Tau31 <= 0.7 ): dictMA_J2Tau31[ 7 ] += scale
				if ( jet2Tau31 <= 0.8 ): dictMA_J2Tau31[ 8 ] += scale
				if ( jet2Tau31 <= 0.9 ): dictMA_J2Tau31[ 9 ] += scale
				if ( jet2Tau31 <= 1.0 ): dictMA_J2Tau31[ 10 ] += scale

				if ( jet1SubjetPtRatio <= 0.0 ): dictMA_J1SubjetPtRatio[ 0 ] += scale
				if ( jet1SubjetPtRatio <= 0.1 ): dictMA_J1SubjetPtRatio[ 1 ] += scale
				if ( jet1SubjetPtRatio <= 0.2 ): dictMA_J1SubjetPtRatio[ 2 ] += scale
				if ( jet1SubjetPtRatio <= 0.3 ): dictMA_J1SubjetPtRatio[ 3 ] += scale
				if ( jet1SubjetPtRatio <= 0.4 ): dictMA_J1SubjetPtRatio[ 4 ] += scale
				if ( jet1SubjetPtRatio <= 0.5 ): dictMA_J1SubjetPtRatio[ 5 ] += scale
				if ( jet1SubjetPtRatio <= 0.6 ): dictMA_J1SubjetPtRatio[ 6 ] += scale
				if ( jet1SubjetPtRatio <= 0.7 ): dictMA_J1SubjetPtRatio[ 7 ] += scale
				if ( jet1SubjetPtRatio <= 0.8 ): dictMA_J1SubjetPtRatio[ 8 ] += scale
				if ( jet1SubjetPtRatio <= 0.9 ): dictMA_J1SubjetPtRatio[ 9 ] += scale
				if ( jet1SubjetPtRatio <= 1.0 ): dictMA_J1SubjetPtRatio[ 10 ] += scale
			
				if ( jet2SubjetPtRatio <= 0.0 ): dictMA_J2SubjetPtRatio[ 0 ] += scale
				if ( jet2SubjetPtRatio <= 0.1 ): dictMA_J2SubjetPtRatio[ 1 ] += scale
				if ( jet2SubjetPtRatio <= 0.2 ): dictMA_J2SubjetPtRatio[ 2 ] += scale
				if ( jet2SubjetPtRatio <= 0.3 ): dictMA_J2SubjetPtRatio[ 3 ] += scale
				if ( jet2SubjetPtRatio <= 0.4 ): dictMA_J2SubjetPtRatio[ 4 ] += scale
				if ( jet2SubjetPtRatio <= 0.5 ): dictMA_J2SubjetPtRatio[ 5 ] += scale
				if ( jet2SubjetPtRatio <= 0.6 ): dictMA_J2SubjetPtRatio[ 6 ] += scale
				if ( jet2SubjetPtRatio <= 0.7 ): dictMA_J2SubjetPtRatio[ 7 ] += scale
				if ( jet2SubjetPtRatio <= 0.8 ): dictMA_J2SubjetPtRatio[ 8 ] += scale
				if ( jet2SubjetPtRatio <= 0.9 ): dictMA_J2SubjetPtRatio[ 9 ] += scale
				if ( jet2SubjetPtRatio <= 1.0 ): dictMA_J2SubjetPtRatio[ 10 ] += scale

				if tau21Cut:
			
					if ( deltaEtaDijet >= 0.0 ): dictMAT21_DeltaEta[ 0 ] += scale
					if ( deltaEtaDijet >= 0.5 ): dictMAT21_DeltaEta[ 1 ] += scale
					if ( deltaEtaDijet >= 1.0 ): dictMAT21_DeltaEta[ 2 ] += scale
					if ( deltaEtaDijet >= 1.5 ): dictMAT21_DeltaEta[ 3 ] += scale
					if ( deltaEtaDijet >= 2.0 ): dictMAT21_DeltaEta[ 4 ] += scale
					if ( deltaEtaDijet >= 2.5 ): dictMAT21_DeltaEta[ 5 ] += scale
					if ( deltaEtaDijet >= 3.0 ): dictMAT21_DeltaEta[ 6 ] += scale
					if ( deltaEtaDijet >= 3.5 ): dictMAT21_DeltaEta[ 7 ] += scale
					if ( deltaEtaDijet >= 4.0 ): dictMAT21_DeltaEta[ 8 ] += scale
					if ( deltaEtaDijet >= 4.5 ): dictMAT21_DeltaEta[ 9 ] += scale
					if ( deltaEtaDijet >= 5.0 ): dictMAT21_DeltaEta[ 10 ] += scale
				
					if ( cosThetaStar <= 0.0 ): dictMAT21_J1CosTheta[ 0 ] += scale
					if ( cosThetaStar <= 0.1 ): dictMAT21_J1CosTheta[ 1 ] += scale
					if ( cosThetaStar <= 0.2 ): dictMAT21_J1CosTheta[ 2 ] += scale
					if ( cosThetaStar <= 0.3 ): dictMAT21_J1CosTheta[ 3 ] += scale
					if ( cosThetaStar <= 0.4 ): dictMAT21_J1CosTheta[ 4 ] += scale
					if ( cosThetaStar <= 0.5 ): dictMAT21_J1CosTheta[ 5 ] += scale
					if ( cosThetaStar <= 0.6 ): dictMAT21_J1CosTheta[ 6 ] += scale
					if ( cosThetaStar <= 0.7 ): dictMAT21_J1CosTheta[ 7 ] += scale
					if ( cosThetaStar <= 0.8 ): dictMAT21_J1CosTheta[ 8 ] += scale
					if ( cosThetaStar <= 0.9 ): dictMAT21_J1CosTheta[ 9 ] += scale
					if ( cosThetaStar <= 1.0 ): dictMAT21_J1CosTheta[ 10 ] += scale
				
					if ( J2CosThetaStar <= 0.0 ): dictMAT21_J2CosTheta[ 0 ] += scale
					if ( J2CosThetaStar <= 0.1 ): dictMAT21_J2CosTheta[ 1 ] += scale
					if ( J2CosThetaStar <= 0.2 ): dictMAT21_J2CosTheta[ 2 ] += scale
					if ( J2CosThetaStar <= 0.3 ): dictMAT21_J2CosTheta[ 3 ] += scale
					if ( J2CosThetaStar <= 0.4 ): dictMAT21_J2CosTheta[ 4 ] += scale
					if ( J2CosThetaStar <= 0.5 ): dictMAT21_J2CosTheta[ 5 ] += scale
					if ( J2CosThetaStar <= 0.6 ): dictMAT21_J2CosTheta[ 6 ] += scale
					if ( J2CosThetaStar <= 0.7 ): dictMAT21_J2CosTheta[ 7 ] += scale
					if ( J2CosThetaStar <= 0.8 ): dictMAT21_J2CosTheta[ 8 ] += scale
					if ( J2CosThetaStar <= 0.9 ): dictMAT21_J2CosTheta[ 9 ] += scale
					if ( J2CosThetaStar <= 1.0 ): dictMAT21_J2CosTheta[ 10 ] += scale
				
					if ( jet1Tau31 <= 0.0 ): dictMAT21_J1Tau31[ 0 ] += scale
					if ( jet1Tau31 <= 0.1 ): dictMAT21_J1Tau31[ 1 ] += scale
					if ( jet1Tau31 <= 0.2 ): dictMAT21_J1Tau31[ 2 ] += scale
					if ( jet1Tau31 <= 0.3 ): dictMAT21_J1Tau31[ 3 ] += scale
					if ( jet1Tau31 <= 0.4 ): dictMAT21_J1Tau31[ 4 ] += scale
					if ( jet1Tau31 <= 0.5 ): dictMAT21_J1Tau31[ 5 ] += scale
					if ( jet1Tau31 <= 0.6 ): dictMAT21_J1Tau31[ 6 ] += scale
					if ( jet1Tau31 <= 0.7 ): dictMAT21_J1Tau31[ 7 ] += scale
					if ( jet1Tau31 <= 0.8 ): dictMAT21_J1Tau31[ 8 ] += scale
					if ( jet1Tau31 <= 0.9 ): dictMAT21_J1Tau31[ 9 ] += scale
					if ( jet1Tau31 <= 1.0 ): dictMAT21_J1Tau31[ 10 ] += scale
				
					if ( jet2Tau31 <= 0.0 ): dictMAT21_J2Tau31[ 0 ] += scale
					if ( jet2Tau31 <= 0.1 ): dictMAT21_J2Tau31[ 1 ] += scale
					if ( jet2Tau31 <= 0.2 ): dictMAT21_J2Tau31[ 2 ] += scale
					if ( jet2Tau31 <= 0.3 ): dictMAT21_J2Tau31[ 3 ] += scale
					if ( jet2Tau31 <= 0.4 ): dictMAT21_J2Tau31[ 4 ] += scale
					if ( jet2Tau31 <= 0.5 ): dictMAT21_J2Tau31[ 5 ] += scale
					if ( jet2Tau31 <= 0.6 ): dictMAT21_J2Tau31[ 6 ] += scale
					if ( jet2Tau31 <= 0.7 ): dictMAT21_J2Tau31[ 7 ] += scale
					if ( jet2Tau31 <= 0.8 ): dictMAT21_J2Tau31[ 8 ] += scale
					if ( jet2Tau31 <= 0.9 ): dictMAT21_J2Tau31[ 9 ] += scale
					if ( jet2Tau31 <= 1.0 ): dictMAT21_J2Tau31[ 10 ] += scale

					if ( jet1SubjetPtRatio <= 0.0 ): dictMAT21_J1SubjetPtRatio[ 0 ] += scale
					if ( jet1SubjetPtRatio <= 0.1 ): dictMAT21_J1SubjetPtRatio[ 1 ] += scale
					if ( jet1SubjetPtRatio <= 0.2 ): dictMAT21_J1SubjetPtRatio[ 2 ] += scale
					if ( jet1SubjetPtRatio <= 0.3 ): dictMAT21_J1SubjetPtRatio[ 3 ] += scale
					if ( jet1SubjetPtRatio <= 0.4 ): dictMAT21_J1SubjetPtRatio[ 4 ] += scale
					if ( jet1SubjetPtRatio <= 0.5 ): dictMAT21_J1SubjetPtRatio[ 5 ] += scale
					if ( jet1SubjetPtRatio <= 0.6 ): dictMAT21_J1SubjetPtRatio[ 6 ] += scale
					if ( jet1SubjetPtRatio <= 0.7 ): dictMAT21_J1SubjetPtRatio[ 7 ] += scale
					if ( jet1SubjetPtRatio <= 0.8 ): dictMAT21_J1SubjetPtRatio[ 8 ] += scale
					if ( jet1SubjetPtRatio <= 0.9 ): dictMAT21_J1SubjetPtRatio[ 9 ] += scale
					if ( jet1SubjetPtRatio <= 1.0 ): dictMAT21_J1SubjetPtRatio[ 10 ] += scale
				
					if ( jet2SubjetPtRatio <= 0.0 ): dictMAT21_J2SubjetPtRatio[ 0 ] += scale
					if ( jet2SubjetPtRatio <= 0.1 ): dictMAT21_J2SubjetPtRatio[ 1 ] += scale
					if ( jet2SubjetPtRatio <= 0.2 ): dictMAT21_J2SubjetPtRatio[ 2 ] += scale
					if ( jet2SubjetPtRatio <= 0.3 ): dictMAT21_J2SubjetPtRatio[ 3 ] += scale
					if ( jet2SubjetPtRatio <= 0.4 ): dictMAT21_J2SubjetPtRatio[ 4 ] += scale
					if ( jet2SubjetPtRatio <= 0.5 ): dictMAT21_J2SubjetPtRatio[ 5 ] += scale
					if ( jet2SubjetPtRatio <= 0.6 ): dictMAT21_J2SubjetPtRatio[ 6 ] += scale
					if ( jet2SubjetPtRatio <= 0.7 ): dictMAT21_J2SubjetPtRatio[ 7 ] += scale
					if ( jet2SubjetPtRatio <= 0.8 ): dictMAT21_J2SubjetPtRatio[ 8 ] += scale
					if ( jet2SubjetPtRatio <= 0.9 ): dictMAT21_J2SubjetPtRatio[ 9 ] += scale
					if ( jet2SubjetPtRatio <= 1.0 ): dictMAT21_J2SubjetPtRatio[ 10 ] += scale

					if cosThetaStarCut:
				
						if ( deltaEtaDijet >= 0.0 ): dictMAT21CTS_DeltaEta[ 0 ] += scale
						if ( deltaEtaDijet >= 0.5 ): dictMAT21CTS_DeltaEta[ 1 ] += scale
						if ( deltaEtaDijet >= 1.0 ): dictMAT21CTS_DeltaEta[ 2 ] += scale
						if ( deltaEtaDijet >= 1.5 ): dictMAT21CTS_DeltaEta[ 3 ] += scale
						if ( deltaEtaDijet >= 2.0 ): dictMAT21CTS_DeltaEta[ 4 ] += scale
						if ( deltaEtaDijet >= 2.5 ): dictMAT21CTS_DeltaEta[ 5 ] += scale
						if ( deltaEtaDijet >= 3.0 ): dictMAT21CTS_DeltaEta[ 6 ] += scale
						if ( deltaEtaDijet >= 3.5 ): dictMAT21CTS_DeltaEta[ 7 ] += scale
						if ( deltaEtaDijet >= 4.0 ): dictMAT21CTS_DeltaEta[ 8 ] += scale
						if ( deltaEtaDijet >= 4.5 ): dictMAT21CTS_DeltaEta[ 9 ] += scale
						if ( deltaEtaDijet >= 5.0 ): dictMAT21CTS_DeltaEta[ 10 ] += scale
					
						if ( jet1Tau31 <= 0.0 ): dictMAT21CTS_J1Tau31[ 0 ] += scale
						if ( jet1Tau31 <= 0.1 ): dictMAT21CTS_J1Tau31[ 1 ] += scale
						if ( jet1Tau31 <= 0.2 ): dictMAT21CTS_J1Tau31[ 2 ] += scale
						if ( jet1Tau31 <= 0.3 ): dictMAT21CTS_J1Tau31[ 3 ] += scale
						if ( jet1Tau31 <= 0.4 ): dictMAT21CTS_J1Tau31[ 4 ] += scale
						if ( jet1Tau31 <= 0.5 ): dictMAT21CTS_J1Tau31[ 5 ] += scale
						if ( jet1Tau31 <= 0.6 ): dictMAT21CTS_J1Tau31[ 6 ] += scale
						if ( jet1Tau31 <= 0.7 ): dictMAT21CTS_J1Tau31[ 7 ] += scale
						if ( jet1Tau31 <= 0.8 ): dictMAT21CTS_J1Tau31[ 8 ] += scale
						if ( jet1Tau31 <= 0.9 ): dictMAT21CTS_J1Tau31[ 9 ] += scale
						if ( jet1Tau31 <= 1.0 ): dictMAT21CTS_J1Tau31[ 10 ] += scale
					
						if ( jet2Tau31 <= 0.0 ): dictMAT21CTS_J2Tau31[ 0 ] += scale
						if ( jet2Tau31 <= 0.1 ): dictMAT21CTS_J2Tau31[ 1 ] += scale
						if ( jet2Tau31 <= 0.2 ): dictMAT21CTS_J2Tau31[ 2 ] += scale
						if ( jet2Tau31 <= 0.3 ): dictMAT21CTS_J2Tau31[ 3 ] += scale
						if ( jet2Tau31 <= 0.4 ): dictMAT21CTS_J2Tau31[ 4 ] += scale
						if ( jet2Tau31 <= 0.5 ): dictMAT21CTS_J2Tau31[ 5 ] += scale
						if ( jet2Tau31 <= 0.6 ): dictMAT21CTS_J2Tau31[ 6 ] += scale
						if ( jet2Tau31 <= 0.7 ): dictMAT21CTS_J2Tau31[ 7 ] += scale
						if ( jet2Tau31 <= 0.8 ): dictMAT21CTS_J2Tau31[ 8 ] += scale
						if ( jet2Tau31 <= 0.9 ): dictMAT21CTS_J2Tau31[ 9 ] += scale
						if ( jet2Tau31 <= 1.0 ): dictMAT21CTS_J2Tau31[ 10 ] += scale

						if ( jet1SubjetPtRatio <= 0.0 ): dictMAT21CTS_J1SubjetPtRatio[ 0 ] += scale
						if ( jet1SubjetPtRatio <= 0.1 ): dictMAT21CTS_J1SubjetPtRatio[ 1 ] += scale
						if ( jet1SubjetPtRatio <= 0.2 ): dictMAT21CTS_J1SubjetPtRatio[ 2 ] += scale
						if ( jet1SubjetPtRatio <= 0.3 ): dictMAT21CTS_J1SubjetPtRatio[ 3 ] += scale
						if ( jet1SubjetPtRatio <= 0.4 ): dictMAT21CTS_J1SubjetPtRatio[ 4 ] += scale
						if ( jet1SubjetPtRatio <= 0.5 ): dictMAT21CTS_J1SubjetPtRatio[ 5 ] += scale
						if ( jet1SubjetPtRatio <= 0.6 ): dictMAT21CTS_J1SubjetPtRatio[ 6 ] += scale
						if ( jet1SubjetPtRatio <= 0.7 ): dictMAT21CTS_J1SubjetPtRatio[ 7 ] += scale
						if ( jet1SubjetPtRatio <= 0.8 ): dictMAT21CTS_J1SubjetPtRatio[ 8 ] += scale
						if ( jet1SubjetPtRatio <= 0.9 ): dictMAT21CTS_J1SubjetPtRatio[ 9 ] += scale
						if ( jet1SubjetPtRatio <= 1.0 ): dictMAT21CTS_J1SubjetPtRatio[ 10 ] += scale
					
						if ( jet2SubjetPtRatio <= 0.0 ): dictMAT21CTS_J2SubjetPtRatio[ 0 ] += scale
						if ( jet2SubjetPtRatio <= 0.1 ): dictMAT21CTS_J2SubjetPtRatio[ 1 ] += scale
						if ( jet2SubjetPtRatio <= 0.2 ): dictMAT21CTS_J2SubjetPtRatio[ 2 ] += scale
						if ( jet2SubjetPtRatio <= 0.3 ): dictMAT21CTS_J2SubjetPtRatio[ 3 ] += scale
						if ( jet2SubjetPtRatio <= 0.4 ): dictMAT21CTS_J2SubjetPtRatio[ 4 ] += scale
						if ( jet2SubjetPtRatio <= 0.5 ): dictMAT21CTS_J2SubjetPtRatio[ 5 ] += scale
						if ( jet2SubjetPtRatio <= 0.6 ): dictMAT21CTS_J2SubjetPtRatio[ 6 ] += scale
						if ( jet2SubjetPtRatio <= 0.7 ): dictMAT21CTS_J2SubjetPtRatio[ 7 ] += scale
						if ( jet2SubjetPtRatio <= 0.8 ): dictMAT21CTS_J2SubjetPtRatio[ 8 ] += scale
						if ( jet2SubjetPtRatio <= 0.9 ): dictMAT21CTS_J2SubjetPtRatio[ 9 ] += scale
						if ( jet2SubjetPtRatio <= 1.0 ): dictMAT21CTS_J2SubjetPtRatio[ 10 ] += scale

	cutDijet = [ dictMassAsym, dictDeltaEta, dictJ1CosTheta, dictJ2CosTheta, dictJ1Tau21, dictJ2Tau21, dictJ1Tau31, dictJ2Tau31, dictJ1SubjetPtRatio, dictJ2SubjetPtRatio ]
	cutMassAsym = [ dictMA_DeltaEta, dictMA_J1CosTheta, dictMA_J2CosTheta, dictMA_J1Tau21, dictMA_J2Tau21, dictMA_J1Tau31, dictMA_J2Tau31, dictMA_J1SubjetPtRatio, dictMA_J2SubjetPtRatio ]
	cutTau21 = [ dictMAT21_DeltaEta, dictMA_J1CosTheta, dictMA_J2CosTheta, dictMA_J1Tau31, dictMA_J2Tau31, dictMA_J1SubjetPtRatio, dictMA_J2SubjetPtRatio ]
	cutCosTheta = [ dictMAT21CTS_DeltaEta, dictMA_J1CosTheta, dictMA_J2CosTheta, dictMA_J1Tau31, dictMA_J2Tau31, dictMA_J1SubjetPtRatio, dictMA_J2SubjetPtRatio ]

	TOTAL1  = [ cutDijet, cutMassAsym, cutTau21, cutCosTheta ]
	print 'events after trigger', eventsAfterTrigger, 'events that pass selection', eventsPassed

	return TOTAL1


def optimization( mass, PU, grooming, outputFileName ):
	"""docstring for optimization"""

	inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15DR74_'+PU+'_v03_v01p3.root'
	signalTotal = calcOpt( inputFileName, grooming )
	signalMassAsym 		= signalTotal[0][0]
	signalDeltaEta 		= signalTotal[0][1]
	signalJ1CosTheta 	= signalTotal[0][2]
	signalJ2CosTheta 	= signalTotal[0][3]
	signalJ1Tau21 		= signalTotal[0][4]
	signalJ2Tau21 		= signalTotal[0][5]
	signalJ1Tau31 		= signalTotal[0][6]
	signalJ2Tau31 		= signalTotal[0][7]
	signalJ1SubjetPtRatio 	= signalTotal[0][8]
	signalJ2SubjetPtRatio 	= signalTotal[0][9]

	signalMA_DeltaEta 		= signalTotal[1][0]
	signalMA_J1CosTheta	 	= signalTotal[1][1]
	signalMA_J2CosTheta 		= signalTotal[1][2]
	signalMA_J1Tau21 		= signalTotal[1][3]
	signalMA_J2Tau21 		= signalTotal[1][4]
	signalMA_J1Tau31 		= signalTotal[1][5]
	signalMA_J2Tau31 		= signalTotal[1][6]
	signalMA_J1SubjetPtRatio 	= signalTotal[1][7]
	signalMA_J2SubjetPtRatio 	= signalTotal[1][8]

	signalMAT21_DeltaEta 		= signalTotal[2][0]
	signalMAT21_J1CosTheta 	= signalTotal[2][1]
	signalMAT21_J2CosTheta	= signalTotal[2][2]
	signalMAT21_J1Tau31 		= signalTotal[2][3]
	signalMAT21_J2Tau31 		= signalTotal[2][4]
	signalMAT21_J1SubjetPtRatio 	= signalTotal[2][5]
	signalMAT21_J2SubjetPtRatio 	= signalTotal[2][6]

	signalMAT21CTS_DeltaEta 	= signalTotal[0][0]
	signalMAT21CTS_J1Tau31 		= signalTotal[0][1]
	signalMAT21CTS_J2Tau31 		= signalTotal[0][2]
	signalMAT21CTS_J1SubjetPtRatio 	= signalTotal[0][3]
	signalMAT21CTS_J2SubjetPtRatio 	= signalTotal[0][4]

	'''
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
	'''
	inputQCDFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15DR74_Asympt25ns_v03_v01p3.root'
	qcdTotal = calcOpt( inputQCDFileName, grooming )
	qcdMassAsym 		= qcdTotal[0][0]
	qcdDeltaEta 		= qcdTotal[0][1]
	qcdJ1CosTheta 		= qcdTotal[0][2]
	qcdJ2CosTheta 		= qcdTotal[0][3]
	qcdJ1Tau21 		= qcdTotal[0][4]
	qcdJ2Tau21 		= qcdTotal[0][5]
	qcdJ1Tau31 		= qcdTotal[0][6]
	qcdJ2Tau31 		= qcdTotal[0][7]
	qcdJ1SubjetPtRatio 	= qcdTotal[0][8]
	qcdJ2SubjetPtRatio 	= qcdTotal[0][9]

	qcdMA_DeltaEta 		= qcdTotal[1][0]
	qcdMA_J1CosTheta	 	= qcdTotal[1][1]
	qcdMA_J2CosTheta 		= qcdTotal[1][2]
	qcdMA_J1Tau21 		= qcdTotal[1][3]
	qcdMA_J2Tau21 		= qcdTotal[1][4]
	qcdMA_J1Tau31 		= qcdTotal[1][5]
	qcdMA_J2Tau31 		= qcdTotal[1][6]
	qcdMA_J1SubjetPtRatio 	= qcdTotal[1][7]
	qcdMA_J2SubjetPtRatio 	= qcdTotal[1][8]

	qcdMAT21_DeltaEta 		= qcdTotal[2][0]
	qcdMAT21_J1CosTheta 	= qcdTotal[2][1]
	qcdMAT21_J2CosTheta	= qcdTotal[2][2]
	qcdMAT21_J1Tau31 		= qcdTotal[2][3]
	qcdMAT21_J2Tau31 		= qcdTotal[2][4]
	qcdMAT21_J1SubjetPtRatio 	= qcdTotal[2][5]
	qcdMAT21_J2SubjetPtRatio 	= qcdTotal[2][6]

	qcdMAT21CTS_DeltaEta 	= qcdTotal[0][0]
	qcdMAT21CTS_J1Tau31 		= qcdTotal[0][1]
	qcdMAT21CTS_J2Tau31 		= qcdTotal[0][2]
	qcdMAT21CTS_J1SubjetPtRatio 	= qcdTotal[0][3]
	qcdMAT21CTS_J2SubjetPtRatio 	= qcdTotal[0][4]

	'''
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
	'''

	inputFileNameWJets = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01p3.root'
	WJetsTotal = calcOpt( inputFileNameWJets, grooming )
	WJetsMassAsym 		= WJetsTotal[0][0]
	WJetsDeltaEta 		= WJetsTotal[0][1]
	WJetsJ1CosTheta 	= WJetsTotal[0][2]
	WJetsJ2CosTheta 	= WJetsTotal[0][3]
	WJetsJ1Tau21 		= WJetsTotal[0][4]
	WJetsJ2Tau21 		= WJetsTotal[0][5]
	WJetsJ1Tau31 		= WJetsTotal[0][6]
	WJetsJ2Tau31 		= WJetsTotal[0][7]
	WJetsJ1SubjetPtRatio 	= WJetsTotal[0][8]
	WJetsJ2SubjetPtRatio 	= WJetsTotal[0][9]

	WJetsMA_DeltaEta 		= WJetsTotal[1][0]
	WJetsMA_J1CosTheta	 	= WJetsTotal[1][1]
	WJetsMA_J2CosTheta 		= WJetsTotal[1][2]
	WJetsMA_J1Tau21 		= WJetsTotal[1][3]
	WJetsMA_J2Tau21 		= WJetsTotal[1][4]
	WJetsMA_J1Tau31 		= WJetsTotal[1][5]
	WJetsMA_J2Tau31 		= WJetsTotal[1][6]
	WJetsMA_J1SubjetPtRatio 	= WJetsTotal[1][7]
	WJetsMA_J2SubjetPtRatio 	= WJetsTotal[1][8]

	WJetsMAT21_DeltaEta 		= WJetsTotal[2][0]
	WJetsMAT21_J1CosTheta 	= WJetsTotal[2][1]
	WJetsMAT21_J2CosTheta	= WJetsTotal[2][2]
	WJetsMAT21_J1Tau31 		= WJetsTotal[2][3]
	WJetsMAT21_J2Tau31 		= WJetsTotal[2][4]
	WJetsMAT21_J1SubjetPtRatio 	= WJetsTotal[2][5]
	WJetsMAT21_J2SubjetPtRatio 	= WJetsTotal[2][6]

	WJetsMAT21CTS_DeltaEta 	= WJetsTotal[0][0]
	WJetsMAT21CTS_J1Tau31 		= WJetsTotal[0][1]
	WJetsMAT21CTS_J2Tau31 		= WJetsTotal[0][2]
	WJetsMAT21CTS_J1SubjetPtRatio 	= WJetsTotal[0][3]
	WJetsMAT21CTS_J2SubjetPtRatio 	= WJetsTotal[0][4]

	inputFileNameZJets = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01p3.root'
	ZJetsTotal = calcOpt( inputFileNameZJets, grooming )
	ZJetsMassAsym 		= ZJetsTotal[0][0]
	ZJetsDeltaEta 		= ZJetsTotal[0][1]
	ZJetsJ1CosTheta 	= ZJetsTotal[0][2]
	ZJetsJ2CosTheta 	= ZJetsTotal[0][3]
	ZJetsJ1Tau21 		= ZJetsTotal[0][4]
	ZJetsJ2Tau21 		= ZJetsTotal[0][5]
	ZJetsJ1Tau31 		= ZJetsTotal[0][6]
	ZJetsJ2Tau31 		= ZJetsTotal[0][7]
	ZJetsJ1SubjetPtRatio 	= ZJetsTotal[0][8]
	ZJetsJ2SubjetPtRatio 	= ZJetsTotal[0][9]

	ZJetsMA_DeltaEta 		= ZJetsTotal[1][0]
	ZJetsMA_J1CosTheta	 	= ZJetsTotal[1][1]
	ZJetsMA_J2CosTheta 		= ZJetsTotal[1][2]
	ZJetsMA_J1Tau21 		= ZJetsTotal[1][3]
	ZJetsMA_J2Tau21 		= ZJetsTotal[1][4]
	ZJetsMA_J1Tau31 		= ZJetsTotal[1][5]
	ZJetsMA_J2Tau31 		= ZJetsTotal[1][6]
	ZJetsMA_J1SubjetPtRatio 	= ZJetsTotal[1][7]
	ZJetsMA_J2SubjetPtRatio 	= ZJetsTotal[1][8]

	ZJetsMAT21_DeltaEta 		= ZJetsTotal[2][0]
	ZJetsMAT21_J1CosTheta 	= ZJetsTotal[2][1]
	ZJetsMAT21_J2CosTheta	= ZJetsTotal[2][2]
	ZJetsMAT21_J1Tau31 		= ZJetsTotal[2][3]
	ZJetsMAT21_J2Tau31 		= ZJetsTotal[2][4]
	ZJetsMAT21_J1SubjetPtRatio 	= ZJetsTotal[2][5]
	ZJetsMAT21_J2SubjetPtRatio 	= ZJetsTotal[2][6]

	ZJetsMAT21CTS_DeltaEta 	= ZJetsTotal[0][0]
	ZJetsMAT21CTS_J1Tau31 		= ZJetsTotal[0][1]
	ZJetsMAT21CTS_J2Tau31 		= ZJetsTotal[0][2]
	ZJetsMAT21CTS_J1SubjetPtRatio 	= ZJetsTotal[0][3]
	ZJetsMAT21CTS_J2SubjetPtRatio 	= ZJetsTotal[0][4]
	
	outputFile = TFile( outputFileName, 'RECREATE' )

	massAsymOpt	 	= TH1F('massAsym', 'massAsym; Mass Asymmetry Optimization', len(qcdMassAsym)-1, 0., 1. )
	deltaEtaOpt 		= TH1F('deltaEta', 'deltaEta; Delta Eta Dijet Optimization', len(qcdDeltaEta)-1, 0., 1. )
	J1CosThetaOpt 		= TH1F('J1CosTheta', 'J1CosTheta; jet1 Cos Theta Star Optimization', len(qcdJ1CosTheta)-1, 0., 1. )
	J2CosThetaOpt 		= TH1F('J2CosTheta', 'J2CosTheta; jet2 Cos Theta Star Optimization', len(qcdJ2CosTheta)-1, 0., 1. )
	J1Tau21Opt 		= TH1F('J1Tau21', 'J1Tau21; J1 Tau21 Optimization', len(qcdJ1Tau21)-1, 0., 1. )
	J2Tau21Opt 		= TH1F('J2Tau21', 'J2Tau21; J2 Tau21 Optimization', len(qcdJ2Tau21)-1, 0., 1. )
	J1Tau31Opt 		= TH1F('J1Tau31', 'J1Tau31; J1 Tau31 Optimization', len(qcdJ1Tau31)-1, 0., 1. )
	J2Tau31Opt 		= TH1F('J2Tau31', 'J2Tau31; J2 Tau31 Optimization', len(qcdJ2Tau31)-1, 0., 1. )
	J1SubjetPtRatioOpt 	= TH1F('J1SubjetPtRatio', 'J1SubjetPtRatio; J1 Subjet Pt Ratio Optimization', len(qcdJ1SubjetPtRatio)-1, 0., 1. )
	J2SubjetPtRatioOpt 	= TH1F('J2SubjetPtRatio', 'J2SubjetPtRatio; J2 Subjet Pt Ratio Optimization', len(qcdJ2SubjetPtRatio)-1, 0., 1. )

	MA_deltaEtaOpt 		= TH1F('MA_deltaEta', 'MA_deltaEta; Delta Eta Dijet Optimization', len(qcdDeltaEta)-1, 0., 1. )
	MA_J1CosThetaOpt 	= TH1F('MA_J1CosTheta', 'MA_J1CosTheta; jet1 Cos Theta Star Optimization', len(qcdJ1CosTheta)-1, 0., 1. )
	MA_J2CosThetaOpt 	= TH1F('MA_J2CosTheta', 'MA_J2CosTheta; jet2 Cos Theta Star Optimization', len(qcdJ2CosTheta)-1, 0., 1. )
	MA_J1Tau21Opt 		= TH1F('MA_J1Tau21', 'MA_J1Tau21; J1 Tau21 Optimization', len(qcdJ1Tau21)-1, 0., 1. )
	MA_J2Tau21Opt 		= TH1F('MA_J2Tau21', 'MA_J2Tau21; J2 Tau21 Optimization', len(qcdJ2Tau21)-1, 0., 1. )
	MA_J1Tau31Opt 		= TH1F('MA_J1Tau31', 'MA_J1Tau31; J1 Tau31 Optimization', len(qcdJ1Tau31)-1, 0., 1. )
	MA_J2Tau31Opt 		= TH1F('MA_J2Tau31', 'MA_J2Tau31; J2 Tau31 Optimization', len(qcdJ2Tau31)-1, 0., 1. )
	MA_J1SubjetPtRatioOpt 	= TH1F('MA_J1SubjetPtRatio', 'MA_J1SubjetPtRatio; J1 Subjet Pt Ratio Optimization', len(qcdJ1SubjetPtRatio)-1, 0., 1. )
	MA_J2SubjetPtRatioOpt 	= TH1F('MA_J2SubjetPtRatio', 'MA_J2SubjetPtRatio; J2 Subjet Pt Ratio Optimization', len(qcdJ2SubjetPtRatio)-1, 0., 1. )

	MAT21_deltaEtaOpt 		= TH1F('MAT21_deltaEta', 'MAT21_deltaEta; Delta Eta Dijet Optimization', len(qcdDeltaEta)-1, 0., 1. )
	MAT21_J1CosThetaOpt 	= TH1F('MAT21_J1CosTheta', 'MAT21_J1CosTheta; jet1 Cos Theta Star Optimization', len(qcdJ1CosTheta)-1, 0., 1. )
	MAT21_J2CosThetaOpt 	= TH1F('MAT21_J2CosTheta', 'MAT21_J2CosTheta; jet2 Cos Theta Star Optimization', len(qcdJ2CosTheta)-1, 0., 1. )
	MAT21_J1Tau31Opt 		= TH1F('MAT21_J1Tau31', 'MAT21_J1Tau31; J1 Tau31 Optimization', len(qcdJ1Tau31)-1, 0., 1. )
	MAT21_J2Tau31Opt 		= TH1F('MAT21_J2Tau31', 'MAT21_J2Tau31; J2 Tau31 Optimization', len(qcdJ2Tau31)-1, 0., 1. )
	MAT21_J1SubjetPtRatioOpt 	= TH1F('MAT21_J1SubjetPtRatio', 'MAT21_J1SubjetPtRatio; J1 Subjet Pt Ratio Optimization', len(qcdJ1SubjetPtRatio)-1, 0., 1. )
	MAT21_J2SubjetPtRatioOpt 	= TH1F('MAT21_J2SubjetPtRatio', 'MAT21_J2SubjetPtRatio; J2 Subjet Pt Ratio Optimization', len(qcdJ2SubjetPtRatio)-1, 0., 1. )

	MAT21CTS_deltaEtaOpt 		= TH1F('MAT21CTS_deltaEta', 'MAT21CTS_deltaEta; Delta Eta Dijet Optimization', len(qcdDeltaEta)-1, 0., 1. )
	MAT21CTS_J1CosThetaOpt 	= TH1F('MAT21CTS_J1CosTheta', 'MAT21CTS_J1CosTheta; jet1 Cos Theta Star Optimization', len(qcdJ1CosTheta)-1, 0., 1. )
	MAT21CTS_J2CosThetaOpt 	= TH1F('MAT21CTS_J2CosTheta', 'MAT21CTS_J2CosTheta; jet2 Cos Theta Star Optimization', len(qcdJ2CosTheta)-1, 0., 1. )
	MAT21CTS_J1Tau31Opt 		= TH1F('MAT21CTS_J1Tau31', 'MAT21CTS_J1Tau31; J1 Tau31 Optimization', len(qcdJ1Tau31)-1, 0., 1. )
	MAT21CTS_J2Tau31Opt 		= TH1F('MAT21CTS_J2Tau31', 'MAT21CTS_J2Tau31; J2 Tau31 Optimization', len(qcdJ2Tau31)-1, 0., 1. )
	MAT21CTS_J1SubjetPtRatioOpt 	= TH1F('MAT21CTS_J1SubjetPtRatio', 'MAT21CTS_J1SubjetPtRatio; J1 Subjet Pt Ratio Optimization', len(qcdJ1SubjetPtRatio)-1, 0., 1. )
	MAT21CTS_J2SubjetPtRatioOpt 	= TH1F('MAT21CTS_J2SubjetPtRatio', 'MAT21CTS_J2SubjetPtRatio; J2 Subjet Pt Ratio Optimization', len(qcdJ2SubjetPtRatio)-1, 0., 1. )

	for i in range( len( signalMassAsym ) ): 
		#try: valueMassAsym = signalMassAsym[i]/ TMath.Sqrt( qcdMassAsym[i] + TTJetsMassAsym[i] + WJetsMassAsym[i] + ZJetsMassAsym[i] + signalMassAsym[i] )
		try: valueMassAsym = signalMassAsym[i]/ TMath.Sqrt( qcdMassAsym[i] + WJetsMassAsym[i] + ZJetsMassAsym[i] + signalMassAsym[i] )
		except ZeroDivisionError: valueMassAsym = 0
		massAsymOpt.SetBinContent( i, valueMassAsym )

		#try: valueDeltaEta = signalDeltaEta[i]/ TMath.Sqrt( qcdDeltaEta[i] + TTJetsDeltaEta[i] + WJetsDeltaEta[i] + ZJetsDeltaEta[i] + signalDeltaEta[i] )
		try: valueDeltaEta = signalDeltaEta[i]/ TMath.Sqrt( qcdDeltaEta[i] + WJetsDeltaEta[i] + ZJetsDeltaEta[i] + signalDeltaEta[i] )
		except ZeroDivisionError: valueDeltaEta = 0
		deltaEtaOpt.SetBinContent( i, valueDeltaEta )

		#try: value = signalJ1CosTheta[i]/ TMath.Sqrt( qcdJ1CosTheta[i] + TTJetsJ1CosTheta[i] + WJetsJ1CosTheta[i] + ZJetsJ1CosTheta[i] + signalJ1CosTheta[i] )
		try: valueJ1CosTheta = signalJ1CosTheta[i]/ TMath.Sqrt( qcdJ1CosTheta[i] + WJetsJ1CosTheta[i] + ZJetsJ1CosTheta[i] + signalJ1CosTheta[i] )
		except ZeroDivisionError: valueJ1CosTheta = 0
		J1CosThetaOpt.SetBinContent( i, valueJ1CosTheta )

		#try: value = signalJ2CosTheta[i]/ TMath.Sqrt( qcdJ2CosTheta[i] + TTJetsJ2CosTheta[i] + WJetsJ2CosTheta[i] + ZJetsJ2CosTheta[i] + signalJ2CosTheta[i] )
		try: valueJ2CosTheta = signalJ2CosTheta[i]/ TMath.Sqrt( qcdJ2CosTheta[i] + WJetsJ2CosTheta[i] + ZJetsJ2CosTheta[i] + signalJ2CosTheta[i] )
		except ZeroDivisionError: valueJ2CosTheta = 0
		J2CosThetaOpt.SetBinContent( i, valueJ2CosTheta )

		#try: valueJ1Tau21 = signalJ1Tau21[i]/ TMath.Sqrt( qcdJ1Tau21[i] + TTJetsJ1Tau21[i] + WJetsJ1Tau21[i] + ZJetsJ1Tau21[i] + signalJ1Tau21[i] )
		try: valueJ1Tau21 = signalJ1Tau21[i]/ TMath.Sqrt( qcdJ1Tau21[i] + WJetsJ1Tau21[i] + ZJetsJ1Tau21[i] + signalJ1Tau21[i] )
		except ZeroDivisionError: valueJ1Tau21 = 0
		J1Tau21Opt.SetBinContent( i, valueJ1Tau21 )

		#try: valueJ2Tau21 = signalJ2Tau21[i]/ TMath.Sqrt( qcdJ2Tau21[i] + TTJetsJ2Tau21[i] + WJetsJ2Tau21[i] + ZJetsJ2Tau21[i] + signalJ2Tau21[i] )
		try: valueJ2Tau21 = signalJ2Tau21[i]/ TMath.Sqrt( qcdJ2Tau21[i] + WJetsJ2Tau21[i] + ZJetsJ2Tau21[i] + signalJ2Tau21[i] )
		except ZeroDivisionError: valueJ2Tau21 = 0
		J2Tau21Opt.SetBinContent( i, valueJ2Tau21 )

		#try: valueJ1Tau31 = signalJ1Tau31[i]/ TMath.Sqrt( qcdJ1Tau31[i] + TTJetsJ1Tau31[i] + WJetsJ1Tau31[i] + ZJetsJ1Tau31[i] + signalJ1Tau31[i] )
		try: valueJ1Tau31 = signalJ1Tau31[i]/ TMath.Sqrt( qcdJ1Tau31[i] + WJetsJ1Tau31[i] + ZJetsJ1Tau31[i] + signalJ1Tau31[i] )
		except ZeroDivisionError: valueJ1Tau31 = 0
		J1Tau31Opt.SetBinContent( i, valueJ1Tau31 )

		#try: valueJ2Tau31 = signalJ2Tau31[i]/ TMath.Sqrt( qcdJ2Tau31[i] + TTJetsJ2Tau31[i] + WJetsJ2Tau31[i] + ZJetsJ2Tau31[i] + signalJ2Tau31[i] )
		try: valueJ2Tau31 = signalJ2Tau31[i]/ TMath.Sqrt( qcdJ2Tau31[i] + WJetsJ2Tau31[i] + ZJetsJ2Tau31[i] + signalJ2Tau31[i] )
		except ZeroDivisionError: valueJ2Tau31 = 0
		J2Tau31Opt.SetBinContent( i, valueJ2Tau31 )

		#try: valueJ1SubjetPtRatio = signalJ1SubjetPtRatio[i]/ TMath.Sqrt( qcdJ1SubjetPtRatio[i] + TTJetsJ1SubjetPtRatio[i] + WJetsJ1SubjetPtRatio[i] + ZJetsJ1SubjetPtRatio[i] + signalJ1SubjetPtRatio[i] )
		try: valueJ1SubjetPtRatio = signalJ1SubjetPtRatio[i]/ TMath.Sqrt( qcdJ1SubjetPtRatio[i] + WJetsJ1SubjetPtRatio[i] + ZJetsJ1SubjetPtRatio[i] + signalJ1SubjetPtRatio[i] )
		except ZeroDivisionError: valueJ1SubjetPtRatio = 0
		J1SubjetPtRatioOpt.SetBinContent( i, valueJ1SubjetPtRatio )
	
		#try: valueJ2SubjetPtRatio = signalJ2SubjetPtRatio[i]/ TMath.Sqrt( qcdJ2SubjetPtRatio[i] + TTJetsJ2SubjetPtRatio[i] + WJetsJ2SubjetPtRatio[i] + ZJetsJ2SubjetPtRatio[i] + signalJ2SubjetPtRatio[i] )
		try: valueJ2SubjetPtRatio = signalJ2SubjetPtRatio[i]/ TMath.Sqrt( qcdJ2SubjetPtRatio[i] + WJetsJ2SubjetPtRatio[i] + ZJetsJ2SubjetPtRatio[i] + signalJ2SubjetPtRatio[i] )
		except ZeroDivisionError: valueJ2SubjetPtRatio = 0
		J2SubjetPtRatioOpt.SetBinContent( i, valueJ2SubjetPtRatio )

		#try: valueMA_DeltaEta = signalMA_DeltaEta[i]/ TMath.Sqrt( qcdMA_DeltaEta[i] + TTJetsMA_DeltaEta[i] + WJetsMA_DeltaEta[i] + ZJetsMA_DeltaEta[i] + signalMA_DeltaEta[i] )
		try: valueMA_DeltaEta = signalMA_DeltaEta[i]/ TMath.Sqrt( qcdMA_DeltaEta[i] + WJetsMA_DeltaEta[i] + ZJetsMA_DeltaEta[i] + signalMA_DeltaEta[i] )
		except ZeroDivisionError: valueMA_DeltaEta = 0
		MA_deltaEtaOpt.SetBinContent( i, valueMA_DeltaEta )

		#try: value = signalMA_J1CosTheta[i]/ TMath.Sqrt( qcdMA_J1CosTheta[i] + TTMA_JetsMA_J1CosTheta[i] + WJetsMA_J1CosTheta[i] + ZJetsMA_J1CosTheta[i] + signalMA_J1CosTheta[i] )
		try: valueMA_J1CosTheta = signalMA_J1CosTheta[i]/ TMath.Sqrt( qcdMA_J1CosTheta[i] + WJetsMA_J1CosTheta[i] + ZJetsMA_J1CosTheta[i] + signalMA_J1CosTheta[i] )
		except ZeroDivisionError: valueMA_J1CosTheta = 0
		MA_J1CosThetaOpt.SetBinContent( i, valueMA_J1CosTheta )

		#try: value = signalMA_J2CosTheta[i]/ TMath.Sqrt( qcdMA_J2CosTheta[i] + TTMA_JetsMA_J2CosTheta[i] + WJetsMA_J2CosTheta[i] + ZJetsMA_J2CosTheta[i] + signalMA_J2CosTheta[i] )
		try: valueMA_J2CosTheta = signalMA_J2CosTheta[i]/ TMath.Sqrt( qcdMA_J2CosTheta[i] + WJetsMA_J2CosTheta[i] + ZJetsMA_J2CosTheta[i] + signalMA_J2CosTheta[i] )
		except ZeroDivisionError: valueMA_J2CosTheta = 0
		MA_J2CosThetaOpt.SetBinContent( i, valueMA_J2CosTheta )

		#try: valueMA_J1Tau21 = signalMA_J1Tau21[i]/ TMath.Sqrt( qcdMA_J1Tau21[i] + TTMA_JetsMA_J1Tau21[i] + WJetsMA_J1Tau21[i] + ZJetsMA_J1Tau21[i] + signalMA_J1Tau21[i] )
		try: valueMA_J1Tau21 = signalMA_J1Tau21[i]/ TMath.Sqrt( qcdMA_J1Tau21[i] + WJetsMA_J1Tau21[i] + ZJetsMA_J1Tau21[i] + signalMA_J1Tau21[i] )
		except ZeroDivisionError: valueMA_J1Tau21 = 0
		MA_J1Tau21Opt.SetBinContent( i, valueMA_J1Tau21 )

		#try: valueMA_J2Tau21 = signalMA_J2Tau21[i]/ TMath.Sqrt( qcdMA_J2Tau21[i] + TTMA_JetsMA_J2Tau21[i] + WJetsMA_J2Tau21[i] + ZJetsMA_J2Tau21[i] + signalMA_J2Tau21[i] )
		try: valueMA_J2Tau21 = signalMA_J2Tau21[i]/ TMath.Sqrt( qcdMA_J2Tau21[i] + WJetsMA_J2Tau21[i] + ZJetsMA_J2Tau21[i] + signalMA_J2Tau21[i] )
		except ZeroDivisionError: valueMA_J2Tau21 = 0
		MA_J2Tau21Opt.SetBinContent( i, valueMA_J2Tau21 )

		#try: valueMA_J1Tau31 = signalMA_J1Tau31[i]/ TMath.Sqrt( qcdMA_J1Tau31[i] + TTMA_JetsMA_J1Tau31[i] + WJetsMA_J1Tau31[i] + ZJetsMA_J1Tau31[i] + signalMA_J1Tau31[i] )
		try: valueMA_J1Tau31 = signalMA_J1Tau31[i]/ TMath.Sqrt( qcdMA_J1Tau31[i] + WJetsMA_J1Tau31[i] + ZJetsMA_J1Tau31[i] + signalMA_J1Tau31[i] )
		except ZeroDivisionError: valueMA_J1Tau31 = 0
		MA_J1Tau31Opt.SetBinContent( i, valueMA_J1Tau31 )

		#try: valueMA_J2Tau31 = signalMA_J2Tau31[i]/ TMath.Sqrt( qcdMA_J2Tau31[i] + TTMA_JetsMA_J2Tau31[i] + WJetsMA_J2Tau31[i] + ZJetsMA_J2Tau31[i] + signalMA_J2Tau31[i] )
		try: valueMA_J2Tau31 = signalMA_J2Tau31[i]/ TMath.Sqrt( qcdMA_J2Tau31[i] + WJetsMA_J2Tau31[i] + ZJetsMA_J2Tau31[i] + signalMA_J2Tau31[i] )
		except ZeroDivisionError: valueMA_J2Tau31 = 0
		MA_J2Tau31Opt.SetBinContent( i, valueMA_J2Tau31 )

		#try: valueMA_J1SubjetPtRatio = signalMA_J1SubjetPtRatio[i]/ TMath.Sqrt( qcdMA_J1SubjetPtRatio[i] + TTMA_JetsMA_J1SubjetPtRatio[i] + WJetsMA_J1SubjetPtRatio[i] + ZJetsMA_J1SubjetPtRatio[i] + signalMA_J1SubjetPtRatio[i] )
		try: valueMA_J1SubjetPtRatio = signalMA_J1SubjetPtRatio[i]/ TMath.Sqrt( qcdMA_J1SubjetPtRatio[i] + WJetsMA_J1SubjetPtRatio[i] + ZJetsMA_J1SubjetPtRatio[i] + signalMA_J1SubjetPtRatio[i] )
		except ZeroDivisionError: valueMA_J1SubjetPtRatio = 0
		MA_J1SubjetPtRatioOpt.SetBinContent( i, valueMA_J1SubjetPtRatio )
	
		#try: valueMA_J2SubjetPtRatio = signalMA_J2SubjetPtRatio[i]/ TMath.Sqrt( qcdMA_J2SubjetPtRatio[i] + TTMA_JetsMA_J2SubjetPtRatio[i] + WJetsMA_J2SubjetPtRatio[i] + ZJetsMA_J2SubjetPtRatio[i] + signalMA_J2SubjetPtRatio[i] )
		try: valueMA_J2SubjetPtRatio = signalMA_J2SubjetPtRatio[i]/ TMath.Sqrt( qcdMA_J2SubjetPtRatio[i] + WJetsMA_J2SubjetPtRatio[i] + ZJetsMA_J2SubjetPtRatio[i] + signalMA_J2SubjetPtRatio[i] )
		except ZeroDivisionError: valueMA_J2SubjetPtRatio = 0
		MA_J2SubjetPtRatioOpt.SetBinContent( i, valueMA_J2SubjetPtRatio )
	

		#try: valueMAT21_DeltaEta = signalMAT21_DeltaEta[i]/ TMath.Sqrt( qcdMAT21_DeltaEta[i] + TTJetsMAT21_DeltaEta[i] + WJetsMAT21_DeltaEta[i] + ZJetsMAT21_DeltaEta[i] + signalMAT21_DeltaEta[i] )
		try: valueMAT21_DeltaEta = signalMAT21_DeltaEta[i]/ TMath.Sqrt( qcdMAT21_DeltaEta[i] + WJetsMAT21_DeltaEta[i] + ZJetsMAT21_DeltaEta[i] + signalMAT21_DeltaEta[i] )
		except ZeroDivisionError: valueMAT21_DeltaEta = 0
		MAT21_deltaEtaOpt.SetBinContent( i, valueMAT21_DeltaEta )

		#try: value = signalMAT21_J1CosTheta[i]/ TMath.Sqrt( qcdMAT21_J1CosTheta[i] + TTMAT21_JetsMAT21_J1CosTheta[i] + WJetsMAT21_J1CosTheta[i] + ZJetsMAT21_J1CosTheta[i] + signalMAT21_J1CosTheta[i] )
		try: valueMAT21_J1CosTheta = signalMAT21_J1CosTheta[i]/ TMath.Sqrt( qcdMAT21_J1CosTheta[i] + WJetsMAT21_J1CosTheta[i] + ZJetsMAT21_J1CosTheta[i] + signalMAT21_J1CosTheta[i] )
		except ZeroDivisionError: valueMAT21_J1CosTheta = 0
		MAT21_J1CosThetaOpt.SetBinContent( i, valueMAT21_J1CosTheta )

		#try: value = signalMAT21_J2CosTheta[i]/ TMath.Sqrt( qcdMAT21_J2CosTheta[i] + TTMAT21_JetsMAT21_J2CosTheta[i] + WJetsMAT21_J2CosTheta[i] + ZJetsMAT21_J2CosTheta[i] + signalMAT21_J2CosTheta[i] )
		try: valueMAT21_J2CosTheta = signalMAT21_J2CosTheta[i]/ TMath.Sqrt( qcdMAT21_J2CosTheta[i] + WJetsMAT21_J2CosTheta[i] + ZJetsMAT21_J2CosTheta[i] + signalMAT21_J2CosTheta[i] )
		except ZeroDivisionError: valueMAT21_J2CosTheta = 0
		MAT21_J2CosThetaOpt.SetBinContent( i, valueMAT21_J2CosTheta )

		#try: valueMAT21_J1Tau31 = signalMAT21_J1Tau31[i]/ TMath.Sqrt( qcdMAT21_J1Tau31[i] + TTMAT21_JetsMAT21_J1Tau31[i] + WJetsMAT21_J1Tau31[i] + ZJetsMAT21_J1Tau31[i] + signalMAT21_J1Tau31[i] )
		try: valueMAT21_J1Tau31 = signalMAT21_J1Tau31[i]/ TMath.Sqrt( qcdMAT21_J1Tau31[i] + WJetsMAT21_J1Tau31[i] + ZJetsMAT21_J1Tau31[i] + signalMAT21_J1Tau31[i] )
		except ZeroDivisionError: valueMAT21_J1Tau31 = 0
		MAT21_J1Tau31Opt.SetBinContent( i, valueMAT21_J1Tau31 )

		#try: valueMAT21_J2Tau31 = signalMAT21_J2Tau31[i]/ TMath.Sqrt( qcdMAT21_J2Tau31[i] + TTMAT21_JetsMAT21_J2Tau31[i] + WJetsMAT21_J2Tau31[i] + ZJetsMAT21_J2Tau31[i] + signalMAT21_J2Tau31[i] )
		try: valueMAT21_J2Tau31 = signalMAT21_J2Tau31[i]/ TMath.Sqrt( qcdMAT21_J2Tau31[i] + WJetsMAT21_J2Tau31[i] + ZJetsMAT21_J2Tau31[i] + signalMAT21_J2Tau31[i] )
		except ZeroDivisionError: valueMAT21_J2Tau31 = 0
		MAT21_J2Tau31Opt.SetBinContent( i, valueMAT21_J2Tau31 )

		#try: valueMAT21_J1SubjetPtRatio = signalMAT21_J1SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21_J1SubjetPtRatio[i] + TTMAT21_JetsMAT21_J1SubjetPtRatio[i] + WJetsMAT21_J1SubjetPtRatio[i] + ZJetsMAT21_J1SubjetPtRatio[i] + signalMAT21_J1SubjetPtRatio[i] )
		try: valueMAT21_J1SubjetPtRatio = signalMAT21_J1SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21_J1SubjetPtRatio[i] + WJetsMAT21_J1SubjetPtRatio[i] + ZJetsMAT21_J1SubjetPtRatio[i] + signalMAT21_J1SubjetPtRatio[i] )
		except ZeroDivisionError: valueMAT21_J1SubjetPtRatio = 0
		MAT21_J1SubjetPtRatioOpt.SetBinContent( i, valueMAT21_J1SubjetPtRatio )
	
		#try: valueMAT21_J2SubjetPtRatio = signalMAT21_J2SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21_J2SubjetPtRatio[i] + TTMAT21_JetsMAT21_J2SubjetPtRatio[i] + WJetsMAT21_J2SubjetPtRatio[i] + ZJetsMAT21_J2SubjetPtRatio[i] + signalMAT21_J2SubjetPtRatio[i] )
		try: valueMAT21_J2SubjetPtRatio = signalMAT21_J2SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21_J2SubjetPtRatio[i] + WJetsMAT21_J2SubjetPtRatio[i] + ZJetsMAT21_J2SubjetPtRatio[i] + signalMAT21_J2SubjetPtRatio[i] )
		except ZeroDivisionError: valueMAT21_J2SubjetPtRatio = 0
		MAT21_J2SubjetPtRatioOpt.SetBinContent( i, valueMAT21_J2SubjetPtRatio )

		#try: valueMAT21CTS_DeltaEta = signalMAT21CTS_DeltaEta[i]/ TMath.Sqrt( qcdMAT21CTS_DeltaEta[i] + TTJetsMAT21CTS_DeltaEta[i] + WJetsMAT21CTS_DeltaEta[i] + ZJetsMAT21CTS_DeltaEta[i] + signalMAT21CTS_DeltaEta[i] )
		try: valueMAT21CTS_DeltaEta = signalMAT21CTS_DeltaEta[i]/ TMath.Sqrt( qcdMAT21CTS_DeltaEta[i] + WJetsMAT21CTS_DeltaEta[i] + ZJetsMAT21CTS_DeltaEta[i] + signalMAT21CTS_DeltaEta[i] )
		except ZeroDivisionError: valueMAT21CTS_DeltaEta = 0
		MAT21CTS_deltaEtaOpt.SetBinContent( i, valueMAT21CTS_DeltaEta )

		#try: valueMAT21CTS_J1Tau31 = signalMAT21CTS_J1Tau31[i]/ TMath.Sqrt( qcdMAT21CTS_J1Tau31[i] + TTMAT21CTS_JetsMAT21CTS_J1Tau31[i] + WJetsMAT21CTS_J1Tau31[i] + ZJetsMAT21CTS_J1Tau31[i] + signalMAT21CTS_J1Tau31[i] )
		try: valueMAT21CTS_J1Tau31 = signalMAT21CTS_J1Tau31[i]/ TMath.Sqrt( qcdMAT21CTS_J1Tau31[i] + WJetsMAT21CTS_J1Tau31[i] + ZJetsMAT21CTS_J1Tau31[i] + signalMAT21CTS_J1Tau31[i] )
		except ZeroDivisionError: valueMAT21CTS_J1Tau31 = 0
		MAT21CTS_J1Tau31Opt.SetBinContent( i, valueMAT21CTS_J1Tau31 )

		#try: valueMAT21CTS_J2Tau31 = signalMAT21CTS_J2Tau31[i]/ TMath.Sqrt( qcdMAT21CTS_J2Tau31[i] + TTMAT21CTS_JetsMAT21CTS_J2Tau31[i] + WJetsMAT21CTS_J2Tau31[i] + ZJetsMAT21CTS_J2Tau31[i] + signalMAT21CTS_J2Tau31[i] )
		try: valueMAT21CTS_J2Tau31 = signalMAT21CTS_J2Tau31[i]/ TMath.Sqrt( qcdMAT21CTS_J2Tau31[i] + WJetsMAT21CTS_J2Tau31[i] + ZJetsMAT21CTS_J2Tau31[i] + signalMAT21CTS_J2Tau31[i] )
		except ZeroDivisionError: valueMAT21CTS_J2Tau31 = 0
		MAT21CTS_J2Tau31Opt.SetBinContent( i, valueMAT21CTS_J2Tau31 )

		#try: valueMAT21CTS_J1SubjetPtRatio = signalMAT21CTS_J1SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21CTS_J1SubjetPtRatio[i] + TTMAT21CTS_JetsMAT21CTS_J1SubjetPtRatio[i] + WJetsMAT21CTS_J1SubjetPtRatio[i] + ZJetsMAT21CTS_J1SubjetPtRatio[i] + signalMAT21CTS_J1SubjetPtRatio[i] )
		try: valueMAT21CTS_J1SubjetPtRatio = signalMAT21CTS_J1SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21CTS_J1SubjetPtRatio[i] + WJetsMAT21CTS_J1SubjetPtRatio[i] + ZJetsMAT21CTS_J1SubjetPtRatio[i] + signalMAT21CTS_J1SubjetPtRatio[i] )
		except ZeroDivisionError: valueMAT21CTS_J1SubjetPtRatio = 0
		MAT21CTS_J1SubjetPtRatioOpt.SetBinContent( i, valueMAT21CTS_J1SubjetPtRatio )
	
		#try: valueMAT21CTS_J2SubjetPtRatio = signalMAT21CTS_J2SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21CTS_J2SubjetPtRatio[i] + TTMAT21CTS_JetsMAT21CTS_J2SubjetPtRatio[i] + WJetsMAT21CTS_J2SubjetPtRatio[i] + ZJetsMAT21CTS_J2SubjetPtRatio[i] + signalMAT21CTS_J2SubjetPtRatio[i] )
		try: valueMAT21CTS_J2SubjetPtRatio = signalMAT21CTS_J2SubjetPtRatio[i]/ TMath.Sqrt( qcdMAT21CTS_J2SubjetPtRatio[i] + WJetsMAT21CTS_J2SubjetPtRatio[i] + ZJetsMAT21CTS_J2SubjetPtRatio[i] + signalMAT21CTS_J2SubjetPtRatio[i] )
		except ZeroDivisionError: valueMAT21CTS_J2SubjetPtRatio = 0
		MAT21CTS_J2SubjetPtRatioOpt.SetBinContent( i, valueMAT21CTS_J2SubjetPtRatio )



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


