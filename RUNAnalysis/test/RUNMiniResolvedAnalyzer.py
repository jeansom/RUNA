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
from multiprocessing import Process
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2F, TMath, TLorentzVector, TVector3
from array import array
from RUNA.RUNAnalysis.scaleFactors import scaleFactor as SF

gROOT.SetBatch()

def assignDijets( tmpj1, tmpj2, tmpj3, tmpj4, minVarPairing ):
	"""docstring for assignDijets"""

	Pairing = False
	j1 = TLorentzVector()
	j2 = TLorentzVector()
	j3 = TLorentzVector()
	j4 = TLorentzVector()
	if( '1234' in minVarPairing ):
		if ( tmpj1.DeltaR(tmpj2) > ( tmpj3.DeltaR(tmpj4) ) ):
			j1 = tmpj1
			j2 = tmpj2
			j3 = tmpj3
			j4 = tmpj4
		else:
			j1 = tmpj3
			j2 = tmpj4
			j3 = tmpj1
			j4 = tmpj2
		Pairing = True
	elif( '1324' in minVarPairing ):
		if ( tmpj1.DeltaR(tmpj3) > ( tmpj2.DeltaR(tmpj4) ) ):
			j1 = tmpj1
			j2 = tmpj3
			j3 = tmpj2
			j4 = tmpj4
		else:
			j1 = tmpj2
			j2 = tmpj4
			j3 = tmpj1
			j4 = tmpj3
		Pairing = True
	elif( '1423' in minVarPairing ):
		if ( tmpj1.DeltaR(tmpj4) > ( tmpj2.DeltaR(tmpj3) ) ):
			j1 = tmpj1
			j2 = tmpj4
			j3 = tmpj2
			j4 = tmpj3
		else:
			j1 = tmpj2
			j2 = tmpj3
			j3 = tmpj1
			j4 = tmpj4
		Pairing = True

	return [ Pairing, j1, j2, j3, j4 ]

def DeltaRPairing( j1, j2, j3, j4, offset ):
	"""docstring for DeltaRPairing"""

	mindRDeltaRPairing = {}
	mindRDeltaRPairing[ '1234' ] = ( abs( j1.DeltaR(j2) - offset ) + abs( j3.DeltaR(j4) - offset ) )
	mindRDeltaRPairing[ '1324' ] = ( abs( j1.DeltaR(j3) - offset ) + abs( j2.DeltaR(j4) - offset ) )
	mindRDeltaRPairing[ '1423' ] = ( abs( j1.DeltaR(j4) - offset ) + abs( j2.DeltaR(j3) - offset ) )
	minDeltaRPairing = min(mindRDeltaRPairing, key=mindRDeltaRPairing.get)
	DeltaRPairing = assignDijets( j1, j2, j3, j4, minDeltaRPairing  )

	return [ DeltaRPairing[0], DeltaRPairing[1], DeltaRPairing[2], DeltaRPairing[3], DeltaRPairing[4], mindRDeltaRPairing[ minDeltaRPairing ], minDeltaRPairing ]

def MassAsyming( j1, j2, j3, j4 ):
	"""docstring for MassAsyming"""

	massAsymmetry = {}
	massAsymmetry[ '1234' ] = ( abs( j1.M() - j2.M() ) / abs( j3.M() - j4.M() ) )
	massAsymmetry[ '1324' ] = ( abs( j1.M() - j3.M() ) / abs( j2.M() - j4.M() ) )
	massAsymmetry[ '1423' ] = ( abs( j1.M() - j4.M() ) / abs( j2.M() - j3.M() ) )
	minMassAsyming = min(massAsymmetry, key=massAsymmetry.get)
	MassAsyming = assignDijets( j1, j2, j3, j4, minMassAsyming  )

	return [ MassAsyming[0], MassAsyming[1], MassAsyming[2], MassAsyming[3], MassAsyming[4], massAsymmetry[ minMassAsyming ], minMassAsyming ]

def calcCosThetaStar(j1, j2):
	"""docstring for calcCosThetaStar"""

	tmpCM1 = j1 + j2 
	tmpJ1 = TLorentzVector()
	tmpJ2 = TLorentzVector()
	tmpJ1.SetPtEtaPhiE( j1.Pt(), j1.Eta(), j1.Phi(), j1.E() )
	tmpJ2.SetPtEtaPhiE( j2.Pt(), j2.Eta(), j2.Phi(), j2.E() )
	tmpJ1.Boost( -tmpCM1.BoostVector() )
	tmpJ2.Boost( -tmpCM1.BoostVector() )
	tmpV1 = TVector3( tmpJ1.X(), tmpJ1.Y(), tmpJ1.Z() )
	tmpV2 = TVector3( tmpJ2.X(), tmpJ2.Y(), tmpJ2.Z() )
	#cosThetaStar1 = abs( ( ( pairoff08[1].Px() * pairoff08[2].Px() ) + ( pairoff08[1].Py() * pairoff08[2].Py() ) + ( pairoff08[1].Pz() * pairoff08[2].Pz() ) )  / ( pairoff08[1].E() * pairoff08[2].E() ) )
	cosThetaStar = abs( tmpV1.CosTheta() )

	return cosThetaStar

def dijetVar( listJets ):
	"""docstring for dijetVar"""

	dijet1 = listJets[0] + listJets[1]
	dijet2 = listJets[2] + listJets[3]
	deltaEtaDijet1 = abs( listJets[0].Eta() - listJets[1].Eta() )
	deltaEtaDijet2 = abs( listJets[2].Eta() - listJets[3].Eta() )
	deltaEtaAveDijets = ( abs( listJets[0].Eta() - listJets[1].Eta() ) + abs( listJets[2].Eta() - listJets[3].Eta()  ) ) / 2
	massAsymmetry = abs( dijet1.M() - dijet2.M() ) / ( dijet1.M() + dijet2.M() )
	deltaEtaDijets = abs( dijet1.Eta() - dijet2.Eta() )
	massAve = ( dijet1.M() + dijet2.M() ) / 2
	cosThetaStarDijet1 = calcCosThetaStar( listJets[0], listJets[1] )
	cosThetaStarDijet2 = calcCosThetaStar( listJets[2], listJets[3] )
	deltaDijet1 = ( listJets[0].Pt() + listJets[1].Pt() ) - massAve
	deltaDijet2 = ( listJets[2].Pt() + listJets[3].Pt() ) - massAve
	xi1 = ( ( max( [ listJets[0].M() , listJets[1].M() ] ) / dijet1.M() ) * listJets[0].DeltaR( listJets[1])  )
	xi2 = ( ( max( [ listJets[2].M() , listJets[3].M() ] ) / dijet2.M() ) * listJets[2].DeltaR( listJets[3])  )
	deltaRDijet1 = listJets[0].DeltaR( listJets[1] )
	deltaRDijet2 = listJets[2].DeltaR( listJets[3] )

	return [ massAve, deltaEtaDijet1, deltaEtaDijet2, deltaEtaAveDijets, deltaEtaDijets, massAsymmetry, cosThetaStarDijet1, cosThetaStarDijet2, deltaDijet1, deltaDijet2, xi1, xi2, deltaRDijet1, deltaRDijet2 ]

######################################
def myAnalyzer( sample, couts ):


	inputFile = TFile( sample, 'read' )
	outputFileName = sample.replace('RUNAnalysis','RUNMiniResolvedAnalysis')
	outputFile = TFile( outputFileName, 'RECREATE' )
	#outputFile = TFile( 'test.root', 'RECREATE' )

	###################################### output Tree
	tree = TTree('RUNAMiniTree', 'RUNAMiniTree')
	weight = array( 'f', [ 0. ] )
	dijet1Mass = array( 'f', [ 0. ] )
	dijet2Mass = array( 'f', [ 0. ] )
	dijet1sPt = array( 'f', [ 0. ] )
	dijet2sPt = array( 'f', [ 0. ] )
	massAve = array( 'f', [ 0. ] )
	j4Pt = array( 'f', [ 0. ] )
	ht = array( 'f', [ 0. ] )
	mindR = array( 'f', [ 0. ] )
	deltaEtaDijet1 = array( 'f', [ 0. ] )
	deltaEtaDijet2 = array( 'f', [ 0. ] )
	deltaEtaAveDijets = array( 'f', [ 0. ] )
	deltaEtaDijets = array( 'f', [ 0. ] )
	massAsymmetry = array( 'f', [ 0. ] )
	cosThetaStarDijet1 = array( 'f', [ 0. ] )
	cosThetaStarDijet2 = array( 'f', [ 0. ] )
	deltaDijet1 = array( 'f', [ 0. ] )
	deltaDijet2 = array( 'f', [ 0. ] )
	xi1 = array( 'f', [ 0. ] )
	xi2 = array( 'f', [ 0. ] )
	deltaRDijet1 = array( 'f', [ 0. ] )
	deltaRDijet2 = array( 'f', [ 0. ] )
	tree.Branch( 'weight', weight, 'weight/F' )
	tree.Branch( 'massAve', massAve, 'massAve/F' )
	tree.Branch( 'dijet1Mass', dijet1Mass, 'dijet1Mass/F' )
	tree.Branch( 'dijet2Mass', dijet2Mass, 'dijet2Mass/F' )
	tree.Branch( 'dijet1sPt', dijet1sPt, 'dijet1sPt/F' )
	tree.Branch( 'dijet2sPt', dijet2sPt, 'dijet2sPt/F' )
	tree.Branch( 'mindR', mindR, 'mindR/F' )
	tree.Branch( 'ht', ht, 'ht/F' )
	tree.Branch( 'j4Pt', j4Pt, 'j4Pt/F' )
	tree.Branch( 'deltaEtaDijet1', deltaEtaDijet1, 'deltaEtaDijet1/F' )
	tree.Branch( 'deltaEtaDijet2', deltaEtaDijet2, 'deltaEtaDijet2/F' )
	tree.Branch( 'deltaEtaAveDijets', deltaEtaAveDijets, 'deltaEtaAveDijets/F' )
	tree.Branch( 'deltaEtaDijets', deltaEtaDijets, 'deltaEtaDijets/F' )
	tree.Branch( 'massAsymmetry', massAsymmetry, 'massAsymmetry/F' )
	tree.Branch( 'cosThetaStarDijet1', cosThetaStarDijet1, 'cosThetaStarDijet1/F' )
	tree.Branch( 'cosThetaStarDijet2', cosThetaStarDijet2, 'cosThetaStarDijet2/F' )
	tree.Branch( 'deltaDijet1', deltaDijet1, 'deltaDijet1/F' )
	tree.Branch( 'deltaDijet2', deltaDijet2, 'deltaDijet2/F' )
	tree.Branch( 'xi1', xi1, 'xi1/F' )
	tree.Branch( 'xi2', xi2, 'xi2/F' )
	tree.Branch( 'deltaRDijet1', deltaRDijet1, 'deltaRDijet1/F' )
	tree.Branch( 'deltaRDijet2', deltaRDijet2, 'deltaRDijet2/F' )


	################################################################################################## Trigger Histos
	nBinsMass	= 200
	maxMass		= 2000
	nBinsHT		= 150
	maxHT		= 1500


	hmindR 		= TH1F('mindR', 'mindR', 100, 0, 5. )
	hmassAve 	= TH1F('massAve', 'massAve', nBinsMass, 0, maxMass )
	hdeltaEtaDijet1 	= TH1F('deltaEtaDijet1', 'deltaEtaDijet1', 100, 0, 5. )
	hdeltaEtaDijet2 	= TH1F('deltaEtaDijet2', 'deltaEtaDijet2', 100, 0, 5. )
	hdeltaEtaAveDijets 	= TH1F('deltaEtaAveDijets', 'deltaEtaAveDijets', 100, 0, 5. )
	hdeltaEtaDijets 	= TH1F('deltaEtaDijets', 'deltaEtaDijets', 100, 0, 5. )
	hmassAsymmetry 	= TH1F('massAsymmetry', 'massAsymmetry', 20, 0, 1. )
	hcosThetaStarDijet1 	= TH1F('cosThetaStarDijet1', 'cosThetaStarDijet1', 20, 0, 1. )
	hcosThetaStarDijet2 	= TH1F('cosThetaStarDijet2', 'cosThetaStarDijet2', 20, 0, 1. )
	hdeltaDijet1 	= TH1F('deltaDijet1', 'deltaDijet1', 1000, -1000, 1000. )
	hdeltaDijet2 	= TH1F('deltaDijet2', 'deltaDijet2', 1000, -1000, 1000. )
	hxi1 		= TH1F('xi1', 'xi1', 50, 0, 5. )
	hxi2 		= TH1F('xi2', 'xi2', 50, 0, 5. )
	hdeltaRDijet1 		= TH1F('deltaRDijet1', 'deltaRDijet1', 50, 0, 5. )
	hdeltaRDijet2 		= TH1F('deltaRDijet2', 'deltaRDijet2', 50, 0, 5. )
	massAveVsDijet1sPt 	= TH2F('massAveVsDijet1sPt', 'massAveVsDijet1sPt', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsDijet2sPt 	= TH2F('massAveVsDijet2sPt', 'massAveVsDijet2sPt', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsdeltaDijet1 	= TH2F('massAveVsdeltaDijet1', 'massAveVsdeltaDijet1', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsdeltaDijet2 	= TH2F('massAveVsdeltaDijet2', 'massAveVsdeltaDijet2', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsmindR 	= TH2F('massAveVsmindR', 'massAveVsmindR', nBinsMass, 0, maxMass, 100, 0, 5 )
	massAveVsdeltaRDijet1 	= TH2F('massAveVsdeltaRDijet1', 'massAveVsdeltaRDijet1', nBinsMass, 0, maxMass, 50, 0, 5 )
	massAveVsdeltaRDijet2 	= TH2F('massAveVsdeltaRDijet2', 'massAveVsdeltaRDijet2', nBinsMass, 0, maxMass, 50, 0, 5 )


	mindR_cutMassAsym 		= TH1F('mindR_cutMassAsym', 'mindR_cutMassAsym', 100, 0, 5. )
	massAve_cutMassAsym 	= TH1F('massAve_cutMassAsym', 'massAve_cutMassAsym', nBinsMass, 0, maxMass )
	deltaEtaDijet1_cutMassAsym 	= TH1F('deltaEtaDijet1_cutMassAsym', 'deltaEtaDijet1_cutMassAsym', 100, 0, 5. )
	deltaEtaDijet2_cutMassAsym 	= TH1F('deltaEtaDijet2_cutMassAsym', 'deltaEtaDijet2_cutMassAsym', 100, 0, 5. )
	deltaEtaAveDijets_cutMassAsym 	= TH1F('deltaEtaAveDijets_cutMassAsym', 'deltaEtaAveDijets_cutMassAsym', 100, 0, 5. )
	deltaEtaDijets_cutMassAsym 	= TH1F('deltaEtaDijets_cutMassAsym', 'deltaEtaDijets_cutMassAsym', 100, 0, 5. )
	massAsymmetry_cutMassAsym 	= TH1F('massAsymmetry_cutMassAsym', 'massAsymmetry_cutMassAsym', 20, 0, 1. )
	cosThetaStarDijet1_cutMassAsym 	= TH1F('cosThetaStarDijet1_cutMassAsym', 'cosThetaStarDijet1_cutMassAsym', 20, 0, 1. )
	cosThetaStarDijet2_cutMassAsym 	= TH1F('cosThetaStarDijet2_cutMassAsym', 'cosThetaStarDijet2_cutMassAsym', 20, 0, 1. )
	deltaDijet1_cutMassAsym 	= TH1F('deltaDijet1_cutMassAsym', 'deltaDijet1_cutMassAsym', 1000, -1000, 1000. )
	deltaDijet2_cutMassAsym 	= TH1F('deltaDijet2_cutMassAsym', 'deltaDijet2_cutMassAsym', 1000, -1000, 1000. )
	xi1_cutMassAsym 		= TH1F('xi1_cutMassAsym', 'xi1_cutMassAsym', 20, 0, 1. )
	xi2_cutMassAsym 		= TH1F('xi2_cutMassAsym', 'xi2_cutMassAsym', 20, 0, 1. )
	deltaRDijet1_cutMassAsym 		= TH1F('deltaRDijet1_cutMassAsym', 'deltaRDijet1_cutMassAsym', 50, 0, 5. )
	deltaRDijet2_cutMassAsym 		= TH1F('deltaRDijet2_cutMassAsym', 'deltaRDijet2_cutMassAsym', 50, 0, 5. )
	massAveVsDijet1sPt_cutMassAsym 	= TH2F('massAveVsDijet1sPt_cutMassAsym', 'massAveVsDijet1sPt_cutMassAsym', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsDijet2sPt_cutMassAsym 	= TH2F('massAveVsDijet2sPt_cutMassAsym', 'massAveVsDijet2sPt_cutMassAsym', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsdeltaDijet1_cutMassAsym 	= TH2F('massAveVsdeltaDijet1_cutMassAsym', 'massAveVsdeltaDijet1_cutMassAsym', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsdeltaDijet2_cutMassAsym 	= TH2F('massAveVsdeltaDijet2_cutMassAsym', 'massAveVsdeltaDijet2_cutMassAsym', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsmindR_cutMassAsym 	= TH2F('massAveVsmindR_cutMassAsym', 'massAveVsmindR_cutMassAsym', nBinsMass, 0, maxMass, 100, 0, 5 )
	massAveVsdeltaRDijet1_cutMassAsym 	= TH2F('massAveVsdeltaRDijet1_cutMassAsym', 'massAveVsdeltaRDijet1_cutMassAsym', nBinsMass, 0, maxMass, 50, 0, 5 )
	massAveVsdeltaRDijet2_cutMassAsym 	= TH2F('massAveVsdeltaRDijet2_cutMassAsym', 'massAveVsdeltaRDijet2_cutMassAsym', nBinsMass, 0, maxMass, 50, 0, 5 )


	mindR_cutDEta 		= TH1F('mindR_cutDEta', 'mindR_cutDEta', 100, 0, 5. )
	massAve_cutDEta 	= TH1F('massAve_cutDEta', 'massAve_cutDEta', nBinsMass, 0, maxMass )
	deltaEtaDijet1_cutDEta 	= TH1F('deltaEtaDijet1_cutDEta', 'deltaEtaDijet1_cutDEta', 100, 0, 5. )
	deltaEtaDijet2_cutDEta 	= TH1F('deltaEtaDijet2_cutDEta', 'deltaEtaDijet2_cutDEta', 100, 0, 5. )
	deltaEtaAveDijets_cutDEta 	= TH1F('deltaEtaAveDijets_cutDEta', 'deltaEtaAveDijets_cutDEta', 100, 0, 5. )
	deltaEtaDijets_cutDEta 	= TH1F('deltaEtaDijets_cutDEta', 'deltaEtaDijets_cutDEta', 100, 0, 5. )
	massAsymmetry_cutDEta 	= TH1F('massAsymmetry_cutDEta', 'massAsymmetry_cutDEta', 20, 0, 1. )
	cosThetaStarDijet1_cutDEta 	= TH1F('cosThetaStarDijet1_cutDEta', 'cosThetaStarDijet1_cutDEta', 20, 0, 1. )
	cosThetaStarDijet2_cutDEta 	= TH1F('cosThetaStarDijet2_cutDEta', 'cosThetaStarDijet2_cutDEta', 20, 0, 1. )
	deltaDijet1_cutDEta 	= TH1F('deltaDijet1_cutDEta', 'deltaDijet1_cutDEta', 1000, -1000, 1000. )
	deltaDijet2_cutDEta 	= TH1F('deltaDijet2_cutDEta', 'deltaDijet2_cutDEta', 1000, -1000, 1000. )
	xi1_cutDEta 		= TH1F('xi1_cutDEta', 'xi1_cutDEta', 20, 0, 1. )
	xi2_cutDEta 		= TH1F('xi2_cutDEta', 'xi2_cutDEta', 20, 0, 1. )
	deltaRDijet1_cutDEta 		= TH1F('deltaRDijet1_cutDEta', 'deltaRDijet1_cutDEta', 50, 0, 5. )
	deltaRDijet2_cutDEta 		= TH1F('deltaRDijet2_cutDEta', 'deltaRDijet2_cutDEta', 50, 0, 5. )
	massAveVsDijet1sPt_cutDEta 	= TH2F('massAveVsDijet1sPt_cutDEta', 'massAveVsDijet1sPt_cutDEta', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsDijet2sPt_cutDEta 	= TH2F('massAveVsDijet2sPt_cutDEta', 'massAveVsDijet2sPt_cutDEta', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsdeltaDijet1_cutDEta 	= TH2F('massAveVsdeltaDijet1_cutDEta', 'massAveVsdeltaDijet1_cutDEta', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsdeltaDijet2_cutDEta 	= TH2F('massAveVsdeltaDijet2_cutDEta', 'massAveVsdeltaDijet2_cutDEta', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsmindR_cutDEta 	= TH2F('massAveVsmindR_cutDEta', 'massAveVsmindR_cutDEta', nBinsMass, 0, maxMass, 100, 0, 5 )
	massAveVsdeltaRDijet1_cutDEta 	= TH2F('massAveVsdeltaRDijet1_cutDEta', 'massAveVsdeltaRDijet1_cutDEta', nBinsMass, 0, maxMass, 50, 0, 5 )
	massAveVsdeltaRDijet2_cutDEta 	= TH2F('massAveVsdeltaRDijet2_cutDEta', 'massAveVsdeltaRDijet2_cutDEta', nBinsMass, 0, maxMass, 50, 0, 5 )

	mindR_cutDelta 		= TH1F('mindR_cutDelta', 'mindR_cutDelta', 100, 0, 5. )
	massAve_cutDelta 	= TH1F('massAve_cutDelta', 'massAve_cutDelta', nBinsMass, 0, maxMass )
	massAve_cutDelta240 	= TH1F('massAve_cutDelta240', 'massAve_cutDelta240', nBinsMass, 0, maxMass )
	massAve_cutDelta220 	= TH1F('massAve_cutDelta220', 'massAve_cutDelta220', nBinsMass, 0, maxMass )
	massAve_cutDelta180 	= TH1F('massAve_cutDelta180', 'massAve_cutDelta180', nBinsMass, 0, maxMass )
	massAve_cutDelta160 	= TH1F('massAve_cutDelta160', 'massAve_cutDelta160', nBinsMass, 0, maxMass )
	deltaEtaDijet1_cutDelta 	= TH1F('deltaEtaDijet1_cutDelta', 'deltaEtaDijet1_cutDelta', 100, 0, 5. )
	deltaEtaDijet2_cutDelta 	= TH1F('deltaEtaDijet2_cutDelta', 'deltaEtaDijet2_cutDelta', 100, 0, 5. )
	deltaEtaAveDijets_cutDelta 	= TH1F('deltaEtaAveDijets_cutDelta', 'deltaEtaAveDijets_cutDelta', 100, 0, 5. )
	deltaEtaDijets_cutDelta 	= TH1F('deltaEtaDijets_cutDelta', 'deltaEtaDijets_cutDelta', 100, 0, 5. )
	massAsymmetry_cutDelta 	= TH1F('massAsymmetry_cutDelta', 'massAsymmetry_cutDelta', 20, 0, 1. )
	cosThetaStarDijet1_cutDelta 	= TH1F('cosThetaStarDijet1_cutDelta', 'cosThetaStarDijet1_cutDelta', 20, 0, 1. )
	cosThetaStarDijet2_cutDelta 	= TH1F('cosThetaStarDijet2_cutDelta', 'cosThetaStarDijet2_cutDelta', 20, 0, 1. )
	deltaDijet1_cutDelta 	= TH1F('deltaDijet1_cutDelta', 'deltaDijet1_cutDelta', 1000, -1000, 1000. )
	deltaDijet2_cutDelta 	= TH1F('deltaDijet2_cutDelta', 'deltaDijet2_cutDelta', 1000, -1000, 1000. )
	xi1_cutDelta 		= TH1F('xi1_cutDelta', 'xi1_cutDelta', 20, 0, 1. )
	xi2_cutDelta 		= TH1F('xi2_cutDelta', 'xi2_cutDelta', 20, 0, 1. )
	deltaRDijet1_cutDelta 		= TH1F('deltaRDijet1_cutDelta', 'deltaRDijet1_cutDelta', 50, 0, 5. )
	deltaRDijet2_cutDelta 		= TH1F('deltaRDijet2_cutDelta', 'deltaRDijet2_cutDelta', 50, 0, 5. )
	massAveVsDijet1sPt_cutDelta 	= TH2F('massAveVsDijet1sPt_cutDelta', 'massAveVsDijet1sPt_cutDelta', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsDijet2sPt_cutDelta 	= TH2F('massAveVsDijet2sPt_cutDelta', 'massAveVsDijet2sPt_cutDelta', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsdeltaDijet1_cutDelta 	= TH2F('massAveVsdeltaDijet1_cutDelta', 'massAveVsdeltaDijet1_cutDelta', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsdeltaDijet2_cutDelta 	= TH2F('massAveVsdeltaDijet2_cutDelta', 'massAveVsdeltaDijet2_cutDelta', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsmindR_cutDelta 	= TH2F('massAveVsmindR_cutDelta', 'massAveVsmindR_cutDelta', nBinsMass, 0, maxMass, 100, 0, 5 )
	massAveVsdeltaRDijet1_cutDelta 	= TH2F('massAveVsdeltaRDijet1_cutDelta', 'massAveVsdeltaRDijet1_cutDelta', nBinsMass, 0, maxMass, 50, 0, 5 )
	massAveVsdeltaRDijet2_cutDelta 	= TH2F('massAveVsdeltaRDijet2_cutDelta', 'massAveVsdeltaRDijet2_cutDelta', nBinsMass, 0, maxMass, 50, 0, 5 )

	mindR_cutCosTheta 		= TH1F('mindR_cutCosTheta', 'mindR_cutCosTheta', 100, 0, 5. )
	massAve_cutCosTheta 	= TH1F('massAve_cutCosTheta', 'massAve_cutCosTheta', nBinsMass, 0, maxMass )
	massAve_cutCosTheta65 	= TH1F('massAve_cutCosTheta65', 'massAve_cutCosTheta65', nBinsMass, 0, maxMass )
	massAve_cutCosTheta55 	= TH1F('massAve_cutCosTheta55', 'massAve_cutCosTheta55', nBinsMass, 0, maxMass )
	deltaEtaDijet1_cutCosTheta 	= TH1F('deltaEtaDijet1_cutCosTheta', 'deltaEtaDijet1_cutCosTheta', 100, 0, 5. )
	deltaEtaDijet2_cutCosTheta 	= TH1F('deltaEtaDijet2_cutCosTheta', 'deltaEtaDijet2_cutCosTheta', 100, 0, 5. )
	deltaEtaAveDijets_cutCosTheta 	= TH1F('deltaEtaAveDijets_cutCosTheta', 'deltaEtaAveDijets_cutCosTheta', 100, 0, 5. )
	deltaEtaDijets_cutCosTheta 	= TH1F('deltaEtaDijets_cutCosTheta', 'deltaEtaDijets_cutCosTheta', 100, 0, 5. )
	massAsymmetry_cutCosTheta 	= TH1F('massAsymmetry_cutCosTheta', 'massAsymmetry_cutCosTheta', 20, 0, 1. )
	cosThetaStarDijet1_cutCosTheta 	= TH1F('cosThetaStarDijet1_cutCosTheta', 'cosThetaStarDijet1_cutCosTheta', 20, 0, 1. )
	cosThetaStarDijet2_cutCosTheta 	= TH1F('cosThetaStarDijet2_cutCosTheta', 'cosThetaStarDijet2_cutCosTheta', 20, 0, 1. )
	deltaDijet1_cutCosTheta 	= TH1F('deltaDijet1_cutCosTheta', 'deltaDijet1_cutCosTheta', 1000, -1000, 1000. )
	deltaDijet2_cutCosTheta 	= TH1F('deltaDijet2_cutCosTheta', 'deltaDijet2_cutCosTheta', 1000, -1000, 1000. )
	xi1_cutCosTheta 		= TH1F('xi1_cutCosTheta', 'xi1_cutCosTheta', 20, 0, 1. )
	xi2_cutCosTheta 		= TH1F('xi2_cutCosTheta', 'xi2_cutCosTheta', 20, 0, 1. )
	deltaRDijet1_cutCosTheta 		= TH1F('deltaRDijet1_cutCosTheta', 'deltaRDijet1_cutCosTheta', 50, 0, 5. )
	deltaRDijet2_cutCosTheta 		= TH1F('deltaRDijet2_cutCosTheta', 'deltaRDijet2_cutCosTheta', 50, 0, 5. )
	massAveVsDijet1sPt_cutCosTheta 	= TH2F('massAveVsDijet1sPt_cutCosTheta', 'massAveVsDijet1sPt_cutCosTheta', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsDijet2sPt_cutCosTheta 	= TH2F('massAveVsDijet2sPt_cutCosTheta', 'massAveVsDijet2sPt_cutCosTheta', nBinsMass, 0, maxMass, 100, 0, 1000 )
	massAveVsdeltaDijet1_cutCosTheta 	= TH2F('massAveVsdeltaDijet1_cutCosTheta', 'massAveVsdeltaDijet1_cutCosTheta', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsdeltaDijet2_cutCosTheta 	= TH2F('massAveVsdeltaDijet2_cutCosTheta', 'massAveVsdeltaDijet2_cutCosTheta', nBinsMass, 0, maxMass, 1000, -1000, 1000 )
	massAveVsmindR_cutCosTheta 	= TH2F('massAveVsmindR_cutCosTheta', 'massAveVsmindR_cutCosTheta', nBinsMass, 0, maxMass, 100, 0, 5 )
	massAveVsdeltaRDijet1_cutCosTheta 	= TH2F('massAveVsdeltaRDijet1_cutCosTheta', 'massAveVsdeltaRDijet1_cutCosTheta', nBinsMass, 0, maxMass, 50, 0, 5 )
	massAveVsdeltaRDijet2_cutCosTheta 	= TH2F('massAveVsdeltaRDijet2_cutCosTheta', 'massAveVsdeltaRDijet2_cutCosTheta', nBinsMass, 0, maxMass, 50, 0, 5 )



	###################################### Get GenTree 
	events = inputFile.Get( 'RUNATree/RUNATree' )
	numEntries = events.GetEntriesFast()

	print '------> Number of events: '+str(numEntries)
	d = 0
	newLumi = 0
	tmpLumi = 0
	eventsRaw = eventsHT = eventsPassed = eventsDijet = eventsMassAsym = eventsDEta = eventsDEtaSubjet = eventsDEtaTau21 = eventsDEtaTau31 = eventsCosTheta = eventsTau21 = eventsTau21CosTheta = eventsTau21CosThetaDEta = 0
	for i in xrange(numEntries):
		events.GetEntry(i)
		eventsRaw += 1
		#if eventsRaw > 2000: break

		#---- progress of the reading --------
		fraction = 10.*i/(1.*numEntries)
		if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		d = TMath.FloorNint(fraction)

		#---- progress of the reading --------
		Run      = events.run
		Lumi     = events.lumi
		NumEvent = events.event
		#print 'Entry ', Run, ':', Lumi, ':', NumEvent

		HT		= events.HT
		numJets		= events.numJets
		numPV           = events.numPV
		puWeight	 = events.puWeight
		lumiWeight	 = events.lumiWeight
		HT		 = events.HT
		mass1		 = events.mass1
		mass2		 = events.mass2
		avgMass		 = events.avgMass
		delta1		 = events.delta1
		delta2		 = events.delta2
		massRes		 = events.massRes
		eta1		 = events.eta1
		eta2		 = events.eta2
		deltaEta	 = events.deltaEta
		jetsPt		 = events.jetsPt
		jetsEta		 = events.jetsEta
		jetsPhi		 = events.jetsPhi
		jetsE		 = events.jetsE

		if 'Data' in samples: scale = 1
		else: scale = 2476* puWeight * lumiWeight
		j1 = TLorentzVector()
		j2 = TLorentzVector()
		j3 = TLorentzVector()
		j4 = TLorentzVector()
		
		jet4Pt = min( [ jetsPt[0], jetsPt[1], jetsPt[2], jetsPt[3] ] )
		if (len(jetsPt) == 4 ) and (jet4Pt > 80):

			j1.SetPtEtaPhiE( jetsPt[0], jetsEta[0], jetsPhi[0], jetsE[0] )
			j2.SetPtEtaPhiE( jetsPt[1], jetsEta[1], jetsPhi[1], jetsE[1] )
			j3.SetPtEtaPhiE( jetsPt[2], jetsEta[2], jetsPhi[2], jetsE[2] )
			j4.SetPtEtaPhiE( jetsPt[3], jetsEta[3], jetsPhi[3], jetsE[3] )

			pairMass = MassAsyming( j1, j2, j3, j4 )
			pairoff08 = DeltaRPairing( j1, j2, j3, j4, 0.8 )
			
			if pairoff08[0]: 
				variables = dijetVar( pairoff08[1:5] )
				j4Pt[0] = jet4Pt
				ht[0] = HT
				weight[0] = scale
				mindR[0] = mindRpair08 =  pairoff08[5]
				dijet1Mass[0] = dijet1Masspair08 = ( pairoff08[1] + pairoff08[2] ).M()
				dijet1sPt[0] = dijet1sPtpair08 = pairoff08[1].Pt() + pairoff08[2].Pt()
				dijet2Mass[0] = dijet2Masspair08 = ( pairoff08[3] + pairoff08[4] ).M()
				dijet2sPt[0] = dijet2sPtpair08 = pairoff08[3].Pt() + pairoff08[4].Pt()
				massAve[0] = massAvepair08 = variables[0]
				deltaEtaDijet1[0] = deltaEtaDijet1pair08 = variables[1]
				deltaEtaDijet2[0] = deltaEtaDijet2pair08 = variables[2]
				deltaEtaAveDijets[0] = deltaEtaAveDijetspair08 = variables[3]
				deltaEtaDijets[0] = deltaEtaDijetspair08 = variables[4]
				massAsymmetry[0] = massAsymmetrypair08 = variables[5]
				cosThetaStarDijet1[0] = cosThetaStarDijet1pair08 = variables[6]
				cosThetaStarDijet2[0] = cosThetaStarDijet2pair08 = variables[7]
				deltaDijet1[0] = deltaDijet1pair08 = variables[8]
				deltaDijet2[0] = deltaDijet2pair08 = variables[9]
				xi1[0] = xi1pair08 = variables[10]
				xi2[0] = xi2pair08 = variables[11]
				deltaRDijet1[0] = deltaRDijet1pair08 = variables[12]
				deltaRDijet2[0] = deltaRDijet2pair08 = variables[13]

				hmindR.Fill( mindRpair08, scale )
				hmassAve.Fill( massAvepair08, scale )
				hdeltaEtaDijet1.Fill( deltaEtaDijet1pair08, scale )
				hdeltaEtaDijet2.Fill( deltaEtaDijet2pair08, scale )
				hdeltaEtaDijets.Fill( deltaEtaDijetspair08, scale )
				hdeltaEtaAveDijets.Fill( deltaEtaAveDijetspair08, scale )
				hmassAsymmetry.Fill( massAsymmetrypair08, scale )
				hcosThetaStarDijet1.Fill( cosThetaStarDijet1pair08, scale )
				hcosThetaStarDijet2.Fill( cosThetaStarDijet2pair08, scale )
				hdeltaDijet1.Fill( deltaDijet1pair08, scale )
				hdeltaDijet2.Fill( deltaDijet2pair08, scale )
				hxi1.Fill( xi1pair08, scale )
				hxi2.Fill( xi2pair08, scale )
				hdeltaRDijet1.Fill( deltaRDijet1pair08, scale )
				hdeltaRDijet2.Fill( deltaRDijet2pair08, scale )

				massAveVsDijet1sPt.Fill( massAvepair08, dijet1sPtpair08, scale )
				massAveVsDijet2sPt.Fill( massAvepair08, dijet2sPtpair08, scale )
				massAveVsdeltaDijet1.Fill( massAvepair08, deltaDijet1pair08, scale )
				massAveVsdeltaDijet2.Fill( massAvepair08, deltaDijet2pair08, scale )
				massAveVsmindR.Fill( massAvepair08, mindRpair08, scale )
				massAveVsdeltaRDijet1.Fill( massAvepair08, deltaRDijet1pair08, scale )
				massAveVsdeltaRDijet2.Fill( massAvepair08, deltaRDijet2pair08, scale )

				if ( massAsymmetrypair08 < 0.2 ):  

					mindR_cutMassAsym.Fill( mindRpair08, scale )
					massAve_cutMassAsym.Fill( massAvepair08, scale )
					deltaEtaDijet1_cutMassAsym.Fill( deltaEtaDijet1pair08, scale )
					deltaEtaDijet2_cutMassAsym.Fill( deltaEtaDijet2pair08, scale )
					deltaEtaDijets_cutMassAsym.Fill( deltaEtaDijetspair08, scale )
					deltaEtaAveDijets_cutMassAsym.Fill( deltaEtaAveDijetspair08, scale )
					massAsymmetry_cutMassAsym.Fill( massAsymmetrypair08, scale )
					cosThetaStarDijet1_cutMassAsym.Fill( cosThetaStarDijet1pair08, scale )
					cosThetaStarDijet2_cutMassAsym.Fill( cosThetaStarDijet2pair08, scale )
					deltaDijet1_cutMassAsym.Fill( deltaDijet1pair08, scale )
					deltaDijet2_cutMassAsym.Fill( deltaDijet2pair08, scale )
					xi1_cutMassAsym.Fill( xi1pair08, scale )
					xi2_cutMassAsym.Fill( xi2pair08, scale )
					deltaRDijet1_cutMassAsym.Fill( deltaRDijet1pair08, scale )
					deltaRDijet2_cutMassAsym.Fill( deltaRDijet2pair08, scale )

					massAveVsDijet1sPt_cutMassAsym.Fill( massAvepair08, dijet1sPtpair08, scale )
					massAveVsDijet2sPt_cutMassAsym.Fill( massAvepair08, dijet2sPtpair08, scale )
					massAveVsdeltaDijet1_cutMassAsym.Fill( massAvepair08, deltaDijet1pair08, scale )
					massAveVsdeltaDijet2_cutMassAsym.Fill( massAvepair08, deltaDijet2pair08, scale )
					massAveVsmindR_cutMassAsym.Fill( massAvepair08, mindRpair08, scale )
					massAveVsdeltaRDijet1_cutMassAsym.Fill( massAvepair08, deltaRDijet1pair08, scale )
					massAveVsdeltaRDijet2_cutMassAsym.Fill( massAvepair08, deltaRDijet2pair08, scale )

					if ( deltaEtaDijetspair08 < 0.75 ):

						mindR_cutDEta.Fill( mindRpair08, scale )
						massAve_cutDEta.Fill( massAvepair08, scale )
						deltaEtaDijet1_cutDEta.Fill( deltaEtaDijet1pair08, scale )
						deltaEtaDijet2_cutDEta.Fill( deltaEtaDijet2pair08, scale )
						deltaEtaDijets_cutDEta.Fill( deltaEtaDijetspair08, scale )
						deltaEtaAveDijets_cutDEta.Fill( deltaEtaAveDijetspair08, scale )
						massAsymmetry_cutDEta.Fill( massAsymmetrypair08, scale )
						cosThetaStarDijet1_cutDEta.Fill( cosThetaStarDijet1pair08, scale )
						cosThetaStarDijet2_cutDEta.Fill( cosThetaStarDijet2pair08, scale )
						deltaDijet1_cutDEta.Fill( deltaDijet1pair08, scale )
						deltaDijet2_cutDEta.Fill( deltaDijet2pair08, scale )
						xi1_cutDEta.Fill( xi1pair08, scale )
						xi2_cutDEta.Fill( xi2pair08, scale )
						deltaRDijet1_cutDEta.Fill( deltaRDijet1pair08, scale )
						deltaRDijet2_cutDEta.Fill( deltaRDijet2pair08, scale )

						massAveVsDijet1sPt_cutDEta.Fill( massAvepair08, dijet1sPtpair08, scale )
						massAveVsDijet2sPt_cutDEta.Fill( massAvepair08, dijet2sPtpair08, scale )
						massAveVsdeltaDijet1_cutDEta.Fill( massAvepair08, deltaDijet1pair08, scale )
						massAveVsdeltaDijet2_cutDEta.Fill( massAvepair08, deltaDijet2pair08, scale )
						massAveVsmindR_cutDEta.Fill( massAvepair08, mindRpair08, scale )
						massAveVsdeltaRDijet1_cutDEta.Fill( massAvepair08, deltaRDijet1pair08, scale )
						massAveVsdeltaRDijet2_cutDEta.Fill( massAvepair08, deltaRDijet2pair08, scale )
					
						if ( (deltaDijet1pair08 > 180) and ( deltaDijet2pair08 > 180 ) ):

							mindR_cutDelta.Fill( mindRpair08, scale )
							massAve_cutDelta.Fill( massAvepair08, scale )
							deltaEtaDijet1_cutDelta.Fill( deltaEtaDijet1pair08, scale )
							deltaEtaDijet2_cutDelta.Fill( deltaEtaDijet2pair08, scale )
							deltaEtaDijets_cutDelta.Fill( deltaEtaDijetspair08, scale )
							deltaEtaAveDijets_cutDelta.Fill( deltaEtaAveDijetspair08, scale )
							massAsymmetry_cutDelta.Fill( massAsymmetrypair08, scale )
							cosThetaStarDijet1_cutDelta.Fill( cosThetaStarDijet1pair08, scale )
							cosThetaStarDijet2_cutDelta.Fill( cosThetaStarDijet2pair08, scale )
							deltaDijet1_cutDelta.Fill( deltaDijet1pair08, scale )
							deltaDijet2_cutDelta.Fill( deltaDijet2pair08, scale )
							xi1_cutDelta.Fill( xi1pair08, scale )
							xi2_cutDelta.Fill( xi2pair08, scale )
							deltaRDijet1_cutDelta.Fill( deltaRDijet1pair08, scale )
							deltaRDijet2_cutDelta.Fill( deltaRDijet2pair08, scale )

							massAveVsDijet1sPt_cutDelta.Fill( massAvepair08, dijet1sPtpair08, scale )
							massAveVsDijet2sPt_cutDelta.Fill( massAvepair08, dijet2sPtpair08, scale )
							massAveVsdeltaDijet1_cutDelta.Fill( massAvepair08, deltaDijet1pair08, scale )
							massAveVsdeltaDijet2_cutDelta.Fill( massAvepair08, deltaDijet2pair08, scale )
							massAveVsmindR_cutDelta.Fill( massAvepair08, mindRpair08, scale )
							massAveVsdeltaRDijet1_cutDelta.Fill( massAvepair08, deltaRDijet1pair08, scale )
							massAveVsdeltaRDijet2_cutDelta.Fill( massAvepair08, deltaRDijet2pair08, scale )

						
						if ( (cosThetaStarDijet1pair08 < .60 ) and ( cosThetaStarDijet2pair08 < .60 ) ):

							mindR_cutCosTheta.Fill( mindRpair08, scale )
							massAve_cutCosTheta.Fill( massAvepair08, scale )
							deltaEtaDijet1_cutCosTheta.Fill( deltaEtaDijet1pair08, scale )
							deltaEtaDijet2_cutCosTheta.Fill( deltaEtaDijet2pair08, scale )
							deltaEtaDijets_cutCosTheta.Fill( deltaEtaDijetspair08, scale )
							deltaEtaAveDijets_cutCosTheta.Fill( deltaEtaAveDijetspair08, scale )
							massAsymmetry_cutCosTheta.Fill( massAsymmetrypair08, scale )
							cosThetaStarDijet1_cutCosTheta.Fill( cosThetaStarDijet1pair08, scale )
							cosThetaStarDijet2_cutCosTheta.Fill( cosThetaStarDijet2pair08, scale )
							deltaDijet1_cutCosTheta.Fill( deltaDijet1pair08, scale )
							deltaDijet2_cutCosTheta.Fill( deltaDijet2pair08, scale )
							xi1_cutCosTheta.Fill( xi1pair08, scale )
							xi2_cutCosTheta.Fill( xi2pair08, scale )
							deltaRDijet1_cutCosTheta.Fill( deltaRDijet1pair08, scale )
							deltaRDijet2_cutCosTheta.Fill( deltaRDijet2pair08, scale )

							massAveVsDijet1sPt_cutCosTheta.Fill( massAvepair08, dijet1sPtpair08, scale )
							massAveVsDijet2sPt_cutCosTheta.Fill( massAvepair08, dijet2sPtpair08, scale )
							massAveVsdeltaDijet1_cutCosTheta.Fill( massAvepair08, deltaDijet1pair08, scale )
							massAveVsdeltaDijet2_cutCosTheta.Fill( massAvepair08, deltaDijet2pair08, scale )
							massAveVsmindR_cutCosTheta.Fill( massAvepair08, mindRpair08, scale )
							massAveVsdeltaRDijet1_cutCosTheta.Fill( massAvepair08, deltaRDijet1pair08, scale )
							massAveVsdeltaRDijet2_cutCosTheta.Fill( massAvepair08, deltaRDijet2pair08, scale )

						if ( (cosThetaStarDijet1pair08 < .65 ) and ( cosThetaStarDijet2pair08 < .65 ) ): massAve_cutCosTheta65.Fill( massAvepair08, scale )
						if ( (cosThetaStarDijet1pair08 < .55 ) and ( cosThetaStarDijet2pair08 < .55 ) ): massAve_cutCosTheta55.Fill( massAvepair08, scale )


		tree.Fill()
	outputFile.Write()

	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Close()



#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default='350', help='Mass of the Stop' )
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
	samples = args.samples

	if 'RPV' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+mass+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	elif 'Data' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_JetHTRun2015D-All_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
		'''
	elif 'Bkg' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		inputFileName = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600ToInf_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		inputFileName = 'Rootfiles/RUNAnalysis_TTJets_RunIISpring15DR74_Asympt25ns_v03_v01.root'
		'''
	else: 
		#for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800', '1800to2400', '2400to3200', '3200toInf' ]: 
		#	inputFileName = 'Rootfiles//RUNAnalysis_QCD_cutPt_'+qcdBin+'_RunIISpring15MiniAODv2-74X_'+PU+'_v08_v02.root'
		#	myAnalyzer( inputFileName, couts )
		inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	p = Process( target=myAnalyzer, args=( inputFileName, couts ) )
	p.start()
	p.join()

