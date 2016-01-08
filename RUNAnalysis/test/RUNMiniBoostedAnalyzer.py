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
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2D, TMath
from array import array
#from RUNA.RUNAnalysis.scaleFactors import scaleFactor as SF

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
	maxHT		= 2000

	'''
	massAvevsJet1Tau21_NOMasscut 	= TH2D('massAvevsJet1Tau21_NOMasscut', 'massAvevsJet1Tau21_NOMasscut', nBinsMass, 0, maxMass, 20, 0, 1 )
	massAvevsJet2Tau21_NOMasscut 	= TH2D('massAvevsJet2Tau21_NOMasscut', 'massAvevsJet2Tau21_NOMasscut', nBinsMass, 0, maxMass, 20, 0, 1 )
	massAvevsJet1Tau31_NOMasscut 	= TH2D('massAvevsJet1Tau31_NOMasscut', 'massAvevsJet1Tau31_NOMasscut', nBinsMass, 0, maxMass, 20, 0, 1 )
	massAvevsJet2Tau31_NOMasscut 	= TH2D('massAvevsJet2Tau31_NOMasscut', 'massAvevsJet2Tau31_NOMasscut', nBinsMass, 0, maxMass, 20, 0, 1 )
	'''

	#trimmedMassVsHT 	= TH2D('trimmedMassVsHT', 'trimmedMassVsHT', nBinsMass, 0, maxMass, nBinsHT, 0, maxHT )
	massAve_Tau21 	= TH1F('massAve_Tau21', 'massAve_Tau21', nBinsMass, 0, maxMass )
	massAve_Tau21CosTheta 	= TH1F('massAve_Tau21CosTheta', 'massAve_Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Tau21CosTheta 	= TH1F('HT_Tau21CosTheta', 'HT_Tau21CosTheta', 1920, 800, 20000. )
	tmpHT_Tau21CosTheta 	= TH1F('tmpHT_Tau21CosTheta', 'tmpHT_Tau21CosTheta', 1920, 800, 20000. )
	tmpHT_Tau21CosTheta2 	= TH1F('tmpHT_Tau21CosTheta2', 'tmpHT_Tau21CosTheta2', 1920, 800, 20000. )
	tmpHT_Tau21CosTheta3 	= TH1F('tmpHT_Tau21CosTheta3', 'tmpHT_Tau21CosTheta3', 1920, 800, 20000. )
	tmpHT_Tau21CosTheta4 	= TH1F('tmpHT_Tau21CosTheta4', 'tmpHT_Tau21CosTheta4', 1920, 800, 20000. )
	tmpHT_Tau21CosTheta5 	= TH1F('tmpHT_Tau21CosTheta5', 'tmpHT_Tau21CosTheta5', 1920, 800, 20000. )
	tmpHT_Tau21CosTheta6 	= TH1F('tmpHT_Tau21CosTheta6', 'tmpHT_Tau21CosTheta6', 1920, 800, 20000. )
	tmpHT_Tau21CosTheta7 	= TH1F('tmpHT_Tau21CosTheta7', 'tmpHT_Tau21CosTheta7', 1920, 800, 20000. )
	massAve_Tau21CosThetaDEta 	= TH1F('massAve_Tau21CosThetaDEta', 'massAve_Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Tau21CosThetaDEta 	= TH1F('HT_Tau21CosThetaDEta', 'HT_Tau21CosThetaDEta', 1920, 800, 20000. )

	'''
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
	massAve_NOMassAsymTau21CosThetaDEta 	= TH1F('massAve_NOMassAsymTau21CosThetaDEta', 'massAve_NOMassAsymTau21CosThetaDEta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21CosThetaDEtaSubPtRatio 	= TH1F('massAve_NOMassAsymTau21CosThetaDEtaSubPtRatio', 'massAve_NOMassAsymTau21CosThetaDEtaSubPtRatio', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOCosTheta 	= TH1F('massAve_NOMassAsymNOCosTheta', 'massAve_NOMassAsymNOCosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsym 	= TH1F('massAve_NOMassAsym', 'massAve_NOMassAsym', nBinsMass, 0, maxMass )
	massAve_NOMassAsym_ReScale 	= TH1F('massAve_NOMassAsym_ReScale', 'massAve_NOMassAsym_ReScale', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21 	= TH1F('massAve_NOMassAsymTau21', 'massAve_NOMassAsymTau21', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21_ReScale 	= TH1F('massAve_NOMassAsymTau21_ReScale', 'massAve_NOMassAsymTau21_ReScale', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21CosTheta 	= TH1F('massAve_NOMassAsymTau21CosTheta', 'massAve_NOMassAsymTau21CosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21CosTheta_ReScale 	= TH1F('massAve_NOMassAsymTau21CosTheta_ReScale', 'massAve_NOMassAsymTau21CosTheta_ReScale', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21NOCosTheta 	= TH1F('massAve_NOMassAsymTau21NOCosTheta', 'massAve_NOMassAsymTau21NOCosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21NOCosTheta_ReScale 	= TH1F('massAve_NOMassAsymTau21NOCosTheta_ReScale', 'massAve_NOMassAsymTau21NOCosTheta_ReScale', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOTau21 	= TH1F('massAve_NOMassAsymNOTau21', 'massAve_NOMassAsymNOTau21', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOTau21_ReScale 	= TH1F('massAve_NOMassAsymNOTau21_ReScale', 'massAve_NOMassAsymNOTau21_ReScale', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOTau21CosTheta 	= TH1F('massAve_NOMassAsymNOTau21CosTheta', 'massAve_NOMassAsymNOTau21CosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOTau21CosTheta_ReScale 	= TH1F('massAve_NOMassAsymNOTau21CosTheta_ReScale', 'massAve_NOMassAsymNOTau21CosTheta_ReScale', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOTau21NOCosTheta 	= TH1F('massAve_NOMassAsymNOTau21NOCosTheta', 'massAve_NOMassAsymNOTau21NOCosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymNOTau21NOCosTheta_ReScale 	= TH1F('massAve_NOMassAsymNOTau21NOCosTheta_ReScale', 'massAve_NOMassAsymNOTau21NOCosTheta_ReScale', nBinsMass, 0, maxMass )
	HT_NOMassAsym 	= TH1F('HT_NOMassAsym', 'HT_NOMassAsym', 920, 800, 10000. )
	HT_NOMassAsym_ReScale 	= TH1F('HT_NOMassAsym_ReScale', 'HT_NOMassAsym_ReScale', 920, 800, 10000. )
	HT_NOMassAsymTau21 	= TH1F('HT_NOMassAsymTau21', 'HT_NOMassAsymTau21', 920, 800, 10000. )
	HT_NOMassAsymTau21_ReScale 	= TH1F('HT_NOMassAsymTau21_ReScale', 'HT_NOMassAsymTau21_ReScale', 920, 800, 10000. )
	HT_NOMassAsymTau21CosTheta 	= TH1F('HT_NOMassAsymTau21CosTheta', 'HT_NOMassAsymTau21CosTheta', 920, 800, 10000. )
	HT_NOMassAsymTau21CosTheta_ReScale 	= TH1F('HT_NOMassAsymTau21CosTheta_ReScale', 'HT_NOMassAsymTau21CosTheta_ReScale', 920, 800, 10000. )
	HT_NOMassAsymTau21NOCosTheta 	= TH1F('HT_NOMassAsymTau21NOCosTheta', 'HT_NOMassAsymTau21NOCosTheta', 920, 800, 10000. )
	HT_NOMassAsymTau21NOCosTheta_ReScale 	= TH1F('HT_NOMassAsymTau21NOCosTheta_ReScale', 'HT_NOMassAsymTau21NOCosTheta_ReScale', 920, 800, 10000. )
	HT_NOMassAsymNOTau21 	= TH1F('HT_NOMassAsymNOTau21', 'HT_NOMassAsymNOTau21', 920, 800, 10000. )
	HT_NOMassAsymNOTau21_ReScale 	= TH1F('HT_NOMassAsymNOTau21_ReScale', 'HT_NOMassAsymNOTau21_ReScale', 920, 800, 10000. )
	HT_NOMassAsymNOTau21CosTheta 	= TH1F('HT_NOMassAsymNOTau21CosTheta', 'HT_NOMassAsymNOTau21CosTheta', 920, 800, 10000. )
	HT_NOMassAsymNOTau21CosTheta_ReScale 	= TH1F('HT_NOMassAsymNOTau21CosTheta_ReScale', 'HT_NOMassAsymNOTau21CosTheta_ReScale', 920, 800, 10000. )
	HT_NOMassAsymNOTau21NOCosTheta 	= TH1F('HT_NOMassAsymNOTau21NOCosTheta', 'HT_NOMassAsymNOTau21NOCosTheta', 920, 800, 10000. )
	HT_NOMassAsymNOTau21NOCosTheta_ReScale 	= TH1F('HT_NOMassAsymNOTau21NOCosTheta_ReScale', 'HT_NOMassAsymNOTau21NOCosTheta_ReScale', 920, 800, 10000. )
	tmpHT_NOMassAsym 	= TH1F('tmpHT_NOMassAsym', 'tmpHT_NOMassAsym', 1920, 800, 20000. )
	tmpHT_NOMassAsymTau21 	= TH1F('tmpHT_NOMassAsymTau21', 'tmpHT_NOMassAsymTau21', 1920, 800, 20000. )
	tmpHT_NOMassAsymTau21CosTheta 	= TH1F('tmpHT_NOMassAsymTau21CosTheta', 'tmpHT_NOMassAsymTau21CosTheta', 1920, 800, 20000. )
	tmpHT_NOMassAsymTau21NOCosTheta 	= TH1F('tmpHT_NOMassAsymTau21NOCosTheta', 'tmpHT_NOMassAsymTau21NOCosTheta', 1920, 800, 20000. )
	tmpHT_NOMassAsymNOTau21 	= TH1F('tmpHT_NOMassAsymNOTau21', 'tmpHT_NOMassAsymNOTau21', 1920, 800, 20000. )
	tmpHT_NOMassAsymNOTau21CosTheta 	= TH1F('tmpHT_NOMassAsymNOTau21CosTheta', 'tmpHT_NOMassAsymNOTau21CosTheta', 1920, 800, 20000. )
	tmpHT_NOMassAsymNOTau21NOCosTheta 	= TH1F('tmpHT_NOMassAsymNOTau21NOCosTheta', 'tmpHT_NOMassAsymNOTau21NOCosTheta', 1920, 800, 20000. )
	massAvevsHT_NOMassAsym 	= TH2D('massAvevsHT_NOMassAsym', 'massAvevsHT_NOMassAsym', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAvevsHT_NOMassAsymTau21 	= TH2D('massAvevsHT_NOMassAsymTau21', 'massAvevsHT_NOMassAsymTau21', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAvevsHT_NOMassAsymTau21CosTheta 	= TH2D('massAvevsHT_NOMassAsymTau21CosTheta', 'massAvevsHT_NOMassAsymTau21CosTheta', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAvevsHT_NOMassAsymTau21NOCosTheta 	= TH2D('massAvevsHT_NOMassAsymTau21NOCosTheta', 'massAvevsHT_NOMassAsymTau21NOCosTheta', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAvevsHT_NOMassAsymNOTau21 	= TH2D('massAvevsHT_NOMassAsymNOTau21', 'massAvevsHT_NOMassAsymNOTau21', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAvevsHT_NOMassAsymNOTau21CosTheta 	= TH2D('massAvevsHT_NOMassAsymNOTau21CosTheta', 'massAvevsHT_NOMassAsymNOTau21CosTheta', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAvevsHT_NOMassAsymNOTau21NOCosTheta 	= TH2D('massAvevsHT_NOMassAsymNOTau21NOCosTheta', 'massAvevsHT_NOMassAsymNOTau21NOCosTheta', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAve_NOMassAsymTau31 	= TH1F('massAve_NOMassAsymTau31', 'massAve_NOMassAsymTau31', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau31CosTheta 	= TH1F('massAve_NOMassAsymTau31CosTheta', 'massAve_NOMassAsymTau31CosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau31CosThetaDEta 	= TH1F('massAve_NOMassAsymTau31CosThetaDEta', 'massAve_NOMassAsymTau31CosThetaDEta', nBinsMass, 0, maxMass )
	'''
	
	htmpmassAve 	= TH1F('tmpmassAve', 'tmpmassAve', nBinsMass, 0, maxMass )
	hmassAve 	= TH1F('massAve', 'massAve', nBinsMass, 0, maxMass )
	hmassAsymmetry 	= TH1F('massAsymmetry', 'massAsymmetry', 20, 0, 1.)
	hdeltaEtaDijet 	= TH1F('deltaEtaDijet', 'deltaEtaDijet', 100, 0, 5.)
	hjet1Tau31 	= TH1F('jet1Tau31', 'jet1Tau31', 20, 0, 1.)
	hjet2Tau31 	= TH1F('jet2Tau31', 'jet2Tau31', 20, 0, 1.)
	hjet1Tau21 	= TH1F('jet1Tau21', 'jet1Tau21', 20, 0, 1.)
	hjet2Tau21 	= TH1F('jet2Tau21', 'jet2Tau21', 20, 0, 1.)
	hjet1Tau32 	= TH1F('jet1Tau32', 'jet1Tau32', 20, 0, 1.)
	hjet2Tau32 	= TH1F('jet2Tau32', 'jet2Tau32', 20, 0, 1.)
	hjet1CosThetaStar 	= TH1F('jet1CosThetaStar', 'jet1CosThetaStar', 20, 0, 1.)
	hjet2CosThetaStar 	= TH1F('jet2CosThetaStar', 'jet2CosThetaStar', 20, 0, 1.)
	hjet1SubjetPtRatio 	= TH1F('jet1SubjetPtRatio', 'jet1SubjetPtRatio', 20, 0, 1.)
	hjet2SubjetPtRatio 	= TH1F('jet2SubjetPtRatio', 'jet2SubjetPtRatio', 20, 0, 1.)
	
	massAve_cutTau21 	= TH1F('massAve_cutTau21', 'massAve_cutTau21', nBinsMass, 0, maxMass )
	massAsymmetry_cutTau21 	= TH1F('massAsymmetry_cutTau21', 'massAsymmetry_cutTau21', 20, 0, 1.)
	deltaEtaDijet_cutTau21 	= TH1F('deltaEtaDijet_cutTau21', 'deltaEtaDijet_cutTau21', 100, 0, 5.)
	jet1Tau31_cutTau21 	= TH1F('jet1Tau31_cutTau21', 'jet1Tau31_cutTau21', 20, 0, 1.)
	jet2Tau31_cutTau21 	= TH1F('jet2Tau31_cutTau21', 'jet2Tau31_cutTau21', 20, 0, 1.)
	jet1Tau21_cutTau21 	= TH1F('jet1Tau21_cutTau21', 'jet1Tau21_cutTau21', 20, 0, 1.)
	jet2Tau21_cutTau21 	= TH1F('jet2Tau21_cutTau21', 'jet2Tau21_cutTau21', 20, 0, 1.)
	jet1Tau32_cutTau21 	= TH1F('jet1Tau32_cutTau21', 'jet1Tau32_cutTau21', 20, 0, 1.)
	jet2Tau32_cutTau21 	= TH1F('jet2Tau32_cutTau21', 'jet2Tau32_cutTau21', 20, 0, 1.)
	jet1CosThetaStar_cutTau21 	= TH1F('jet1CosThetaStar_cutTau21', 'jet1CosThetaStar_cutTau21', 20, 0, 1.)
	jet2CosThetaStar_cutTau21 	= TH1F('jet2CosThetaStar_cutTau21', 'jet2CosThetaStar_cutTau21', 20, 0, 1.)
	jet1SubjetPtRatio_cutTau21 	= TH1F('jet1SubjetPtRatio_cutTau21', 'jet1SubjetPtRatio_cutTau21', 20, 0, 1.)
	jet2SubjetPtRatio_cutTau21 	= TH1F('jet2SubjetPtRatio_cutTau21', 'jet2SubjetPtRatio_cutTau21', 20, 0, 1.)
	massAsymVsJ1CosTheta_cutTau21 	= TH2D('massAsymVsJ1CosTheta_cutTau21', 'massAsymVsJ1CosTheta_cutTau21', 20, 0, 1., 20, 0, 1.)
	massAsymVsJ2CosTheta_cutTau21 	= TH2D('massAsymVsJ2CosTheta_cutTau21', 'massAsymVsJ2CosTheta_cutTau21', 20, 0, 1., 20, 0, 1.)
	massAsymVsCosTheta_cutTau21 	= TH2D('massAsymVsCosTheta_cutTau21', 'massAsymVsCosTheta_cutTau21', 20, 0, 1., 20, 0, 1.)

	massAve_cutTau31 	= TH1F('massAve_cutTau31', 'massAve_cutTau31', nBinsMass, 0, maxMass )
	massAsymmetry_cutTau31 	= TH1F('massAsymmetry_cutTau31', 'massAsymmetry_cutTau31', 20, 0, 1.)
	deltaEtaDijet_cutTau31 	= TH1F('deltaEtaDijet_cutTau31', 'deltaEtaDijet_cutTau31', 100, 0, 5.)
	jet1Tau31_cutTau31 	= TH1F('jet1Tau31_cutTau31', 'jet1Tau31_cutTau31', 20, 0, 1.)
	jet2Tau31_cutTau31 	= TH1F('jet2Tau31_cutTau31', 'jet2Tau31_cutTau31', 20, 0, 1.)
	jet1Tau21_cutTau31 	= TH1F('jet1Tau21_cutTau31', 'jet1Tau21_cutTau31', 20, 0, 1.)
	jet2Tau21_cutTau31 	= TH1F('jet2Tau21_cutTau31', 'jet2Tau21_cutTau31', 20, 0, 1.)
	jet1Tau32_cutTau31 	= TH1F('jet1Tau32_cutTau31', 'jet1Tau32_cutTau31', 20, 0, 1.)
	jet2Tau32_cutTau31 	= TH1F('jet2Tau32_cutTau31', 'jet2Tau32_cutTau31', 20, 0, 1.)
	jet1CosThetaStar_cutTau31 	= TH1F('jet1CosThetaStar_cutTau31', 'jet1CosThetaStar_cutTau31', 20, 0, 1.)
	jet2CosThetaStar_cutTau31 	= TH1F('jet2CosThetaStar_cutTau31', 'jet2CosThetaStar_cutTau31', 20, 0, 1.)
	jet1SubjetPtRatio_cutTau31 	= TH1F('jet1SubjetPtRatio_cutTau31', 'jet1SubjetPtRatio_cutTau31', 20, 0, 1.)
	jet2SubjetPtRatio_cutTau31 	= TH1F('jet2SubjetPtRatio_cutTau31', 'jet2SubjetPtRatio_cutTau31', 20, 0, 1.)
	massAsymVsJ1CosTheta_cutTau31 	= TH2D('massAsymVsJ1CosTheta_cutTau31', 'massAsymVsJ1CosTheta_cutTau31', 20, 0, 1., 20, 0, 1.)
	massAsymVsJ2CosTheta_cutTau31 	= TH2D('massAsymVsJ2CosTheta_cutTau31', 'massAsymVsJ2CosTheta_cutTau31', 20, 0, 1., 20, 0, 1.)
	massAsymVsCosTheta_cutTau31 	= TH2D('massAsymVsCosTheta_cutTau31', 'massAsymVsCosTheta_cutTau31', 20, 0, 1., 20, 0, 1.)

	massAve_cutTau21_A 	= TH1F('massAve_cutTau21_A', 'massAve_cutTau21_A', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21_A 	= TH2D('massAsymVsCosTheta_cutTau21_A', 'massAsymVsCosTheta_cutTau21_A', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21_B 	= TH1F('massAve_cutTau21_B', 'massAve_cutTau21_B', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21_B 	= TH2D('massAsymVsCosTheta_cutTau21_B', 'massAsymVsCosTheta_cutTau21_B', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21_C 	= TH1F('massAve_cutTau21_C', 'massAve_cutTau21_C', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21_C 	= TH2D('massAsymVsCosTheta_cutTau21_C', 'massAsymVsCosTheta_cutTau21_C', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21_D 	= TH1F('massAve_cutTau21_D', 'massAve_cutTau21_D', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21_D 	= TH2D('massAsymVsCosTheta_cutTau21_D', 'massAsymVsCosTheta_cutTau21_D', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21_Bkg 	= TH1F('massAve_cutTau21_Bkg', 'massAve_cutTau21_Bkg', nBinsMass, 0, maxMass )

	massAve_cutTau21Away_A 	= TH1F('massAve_cutTau21Away_A', 'massAve_cutTau21Away_A', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21Away_A 	= TH2D('massAsymVsCosTheta_cutTau21Away_A', 'massAsymVsCosTheta_cutTau21Away_A', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21Away_B 	= TH1F('massAve_cutTau21Away_B', 'massAve_cutTau21Away_B', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21Away_B 	= TH2D('massAsymVsCosTheta_cutTau21Away_B', 'massAsymVsCosTheta_cutTau21Away_B', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21Away_C 	= TH1F('massAve_cutTau21Away_C', 'massAve_cutTau21Away_C', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21Away_C 	= TH2D('massAsymVsCosTheta_cutTau21Away_C', 'massAsymVsCosTheta_cutTau21Away_C', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21Away_D 	= TH1F('massAve_cutTau21Away_D', 'massAve_cutTau21Away_D', nBinsMass, 0, maxMass )
	massAsymVsCosTheta_cutTau21Away_D 	= TH2D('massAsymVsCosTheta_cutTau21Away_D', 'massAsymVsCosTheta_cutTau21Away_D', 20, 0, 1., 20, 0, 1.)
	massAve_cutTau21Away_Bkg 	= TH1F('massAve_cutTau21Away_Bkg', 'massAve_cutTau21Away_Bkg', nBinsMass, 0, maxMass )


	massAve_cutCosTheta 	= TH1F('massAve_cutCosTheta', 'massAve_cutCosTheta', nBinsMass, 0, maxMass )
	massAsymmetry_cutCosTheta 	= TH1F('massAsymmetry_cutCosTheta', 'massAsymmetry_cutCosTheta', 20, 0, 1.)
	deltaEtaDijet_cutCosTheta 	= TH1F('deltaEtaDijet_cutCosTheta', 'deltaEtaDijet_cutCosTheta', 100, 0, 5.)
	jet1Tau31_cutCosTheta 	= TH1F('jet1Tau31_cutCosTheta', 'jet1Tau31_cutCosTheta', 20, 0, 1.)
	jet2Tau31_cutCosTheta 	= TH1F('jet2Tau31_cutCosTheta', 'jet2Tau31_cutCosTheta', 20, 0, 1.)
	jet1Tau21_cutCosTheta 	= TH1F('jet1Tau21_cutCosTheta', 'jet1Tau21_cutCosTheta', 20, 0, 1.)
	jet2Tau21_cutCosTheta 	= TH1F('jet2Tau21_cutCosTheta', 'jet2Tau21_cutCosTheta', 20, 0, 1.)
	jet1Tau32_cutCosTheta 	= TH1F('jet1Tau32_cutCosTheta', 'jet1Tau32_cutCosTheta', 20, 0, 1.)
	jet2Tau32_cutCosTheta 	= TH1F('jet2Tau32_cutCosTheta', 'jet2Tau32_cutCosTheta', 20, 0, 1.)
	jet1CosThetaStar_cutCosTheta 	= TH1F('jet1CosThetaStar_cutCosTheta', 'jet1CosThetaStar_cutCosTheta', 20, 0, 1.)
	jet2CosThetaStar_cutCosTheta 	= TH1F('jet2CosThetaStar_cutCosTheta', 'jet2CosThetaStar_cutCosTheta', 20, 0, 1.)
	jet1SubjetPtRatio_cutCosTheta 	= TH1F('jet1SubjetPtRatio_cutCosTheta', 'jet1SubjetPtRatio_cutCosTheta', 20, 0, 1.)
	jet2SubjetPtRatio_cutCosTheta 	= TH1F('jet2SubjetPtRatio_cutCosTheta', 'jet2SubjetPtRatio_cutCosTheta', 20, 0, 1.)
	
	massAve_cutMassAsym 	= TH1F('massAve_cutMassAsym', 'massAve_cutMassAsym', nBinsMass, 0, maxMass )
	HT_cutMassAsym 	= TH1F('HT_cutMassAsym', 'HT_cutMassAsym', 2000, 0, 20000 )
	massAsymmetry_cutMassAsym 	= TH1F('massAsymmetry_cutMassAsym', 'massAsymmetry_cutMassAsym', 20, 0, 1.)
	deltaEtaDijet_cutMassAsym 	= TH1F('deltaEtaDijet_cutMassAsym', 'deltaEtaDijet_cutMassAsym', 100, 0, 5.)
	jet1Tau31_cutMassAsym 	= TH1F('jet1Tau31_cutMassAsym', 'jet1Tau31_cutMassAsym', 20, 0, 1.)
	jet2Tau31_cutMassAsym 	= TH1F('jet2Tau31_cutMassAsym', 'jet2Tau31_cutMassAsym', 20, 0, 1.)
	jet1Tau21_cutMassAsym 	= TH1F('jet1Tau21_cutMassAsym', 'jet1Tau21_cutMassAsym', 20, 0, 1.)
	jet2Tau21_cutMassAsym 	= TH1F('jet2Tau21_cutMassAsym', 'jet2Tau21_cutMassAsym', 20, 0, 1.)
	jet1Tau32_cutMassAsym 	= TH1F('jet1Tau32_cutMassAsym', 'jet1Tau32_cutMassAsym', 20, 0, 1.)
	jet2Tau32_cutMassAsym 	= TH1F('jet2Tau32_cutMassAsym', 'jet2Tau32_cutMassAsym', 20, 0, 1.)
	jet1CosThetaStar_cutMassAsym 	= TH1F('jet1CosThetaStar_cutMassAsym', 'jet1CosThetaStar_cutMassAsym', 20, 0, 1.)
	jet2CosThetaStar_cutMassAsym 	= TH1F('jet2CosThetaStar_cutMassAsym', 'jet2CosThetaStar_cutMassAsym', 20, 0, 1.)
	jet1SubjetPtRatio_cutMassAsym 	= TH1F('jet1SubjetPtRatio_cutMassAsym', 'jet1SubjetPtRatio_cutMassAsym', 20, 0, 1.)
	jet2SubjetPtRatio_cutMassAsym 	= TH1F('jet2SubjetPtRatio_cutMassAsym', 'jet2SubjetPtRatio_cutMassAsym', 20, 0, 1.)
	massAve_cutNOMassAsym 	= TH1F('massAve_cutNOMassAsym', 'massAve_cutNOMassAsym', nBinsMass, 0, maxMass )
	massAve_cutNOCosThetaNOMassAsym 	= TH1F('massAve_cutNOCosThetaNOMassAsym', 'massAve_cutNOCosThetaNOMassAsym', nBinsMass, 0, maxMass )


	#### Optimization
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
	variablesBkg = []
	variablesBkg2 = []
	variablesBkg3 = []
	for i in xrange(numEntries):
		events.GetEntry(i)
		eventsRaw += 1

		#---- progress of the reading --------
		fraction = 10.*i/(1.*numEntries)
		if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		d = TMath.FloorNint(fraction)
		#if ( i > 500000 ): break

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
		lumiWeight           = events.lumiWeight
		puWeight           = events.puWeight
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

		if 'Data' in samples: scale = 1
		else: scale = 2476* puWeight * lumiWeight
		#if ( jet1Mass > 400 ) or ( jet2Mass > 400 ): print 'Entry ', Run, ':', Lumi, ':', NumEvent
		#if ( Lumi != tmpLumi ):
		#	newLumi += Lumi
		#	tmpLumi == Lumi
		#print Run/float(Lumi), Run, Lumi, Run/float(newLumi)
		
		deltaEtaDijet = abs( jet1Eta - jet2Eta )
		
		#### TEST
		#trimmedMassVsHT.Fill( trimmedMass, HT )

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )  
		HTCut = ( HT > 900 )
		dijetCut =  ( numJets > 1 )
		subjetPtRatioCut = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		tau21Cut = ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) )
		tau31Cut = ( ( jet1Tau31 < 0.5 ) and ( jet2Tau31 < 0.5 ) )
		massAsymCut = ( massAsym < 0.2 ) 
		massAsymCutAway = ( massAsym < 0.3 ) ## 0.2 
		deltaEtaDijetCut = ( deltaEtaDijet < 1. ) 
		#cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		cosThetaStarCut = ( abs( J1CosThetaStar ) < 0.4 )  and ( abs( J2CosThetaStar ) < 0.4 )  ## 0.2
		cosThetaStarCutAway = ( abs( J1CosThetaStar ) < 0.5 )  and ( abs( J2CosThetaStar ) < 0.5 )
		jetPtCut =  ( jet1Pt > 500 ) and ( jet2Pt > 450 )
		
		#if ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) ): massAve_Tau2106.Fill( massAve, scale )
		
		if HTCut and dijetCut and jetPtCut:
			hmassAve.Fill( massAve, scale )
			hmassAsymmetry.Fill( massAsym, scale )
			hdeltaEtaDijet.Fill( deltaEtaDijet, scale )
			hjet1Tau31.Fill( jet1Tau31, scale )
			hjet2Tau31.Fill( jet2Tau31, scale )
			hjet1Tau21.Fill( jet1Tau21, scale )
			hjet2Tau21.Fill( jet2Tau21, scale )
			hjet1Tau32.Fill( jet1Tau32, scale )
			hjet2Tau32.Fill( jet2Tau32, scale )
			hjet1CosThetaStar.Fill( J1CosThetaStar, scale )
			hjet2CosThetaStar.Fill( J2CosThetaStar, scale )
			hjet1SubjetPtRatio.Fill( jet1SubjetPtRatio, scale )
			hjet2SubjetPtRatio.Fill( jet2SubjetPtRatio, scale )

			if tau21Cut:
				massAve_cutTau21.Fill( massAve, scale )
				massAsymmetry_cutTau21.Fill( massAsym, scale )
				deltaEtaDijet_cutTau21.Fill( deltaEtaDijet, scale )
				jet1Tau31_cutTau21.Fill( jet1Tau31, scale )
				jet2Tau31_cutTau21.Fill( jet2Tau31, scale )
				jet1Tau21_cutTau21.Fill( jet1Tau21, scale )
				jet2Tau21_cutTau21.Fill( jet2Tau21, scale )
				jet1Tau32_cutTau21.Fill( jet1Tau32, scale )
				jet2Tau32_cutTau21.Fill( jet2Tau32, scale )
				jet1CosThetaStar_cutTau21.Fill( J1CosThetaStar, scale )
				jet2CosThetaStar_cutTau21.Fill( J2CosThetaStar, scale )
				jet1SubjetPtRatio_cutTau21.Fill( jet1SubjetPtRatio, scale )
				jet2SubjetPtRatio_cutTau21.Fill( jet2SubjetPtRatio, scale )
				massAsymVsJ1CosTheta_cutTau21.Fill( massAsym, J1CosThetaStar, scale )
				massAsymVsJ2CosTheta_cutTau21.Fill( massAsym, J2CosThetaStar, scale )
				massAsymVsCosTheta_cutTau21.Fill( massAsym, J1CosThetaStar, scale )
				massAsymVsCosTheta_cutTau21.Fill( massAsym, J2CosThetaStar, scale )

				if tau31Cut:
					massAve_cutTau31.Fill( massAve, scale )
					massAsymmetry_cutTau31.Fill( massAsym, scale )
					deltaEtaDijet_cutTau31.Fill( deltaEtaDijet, scale )
					jet1Tau31_cutTau31.Fill( jet1Tau31, scale )
					jet2Tau31_cutTau31.Fill( jet2Tau31, scale )
					jet1Tau21_cutTau31.Fill( jet1Tau21, scale )
					jet2Tau21_cutTau31.Fill( jet2Tau21, scale )
					jet1Tau32_cutTau31.Fill( jet1Tau32, scale )
					jet2Tau32_cutTau31.Fill( jet2Tau32, scale )
					jet1CosThetaStar_cutTau31.Fill( J1CosThetaStar, scale )
					jet2CosThetaStar_cutTau31.Fill( J2CosThetaStar, scale )
					jet1SubjetPtRatio_cutTau31.Fill( jet1SubjetPtRatio, scale )
					jet2SubjetPtRatio_cutTau31.Fill( jet2SubjetPtRatio, scale )
					massAsymVsJ1CosTheta_cutTau31.Fill( massAsym, J1CosThetaStar, scale )
					massAsymVsJ2CosTheta_cutTau31.Fill( massAsym, J2CosThetaStar, scale )
					massAsymVsCosTheta_cutTau31.Fill( massAsym, J1CosThetaStar, scale )
					massAsymVsCosTheta_cutTau31.Fill( massAsym, J2CosThetaStar, scale )

					if cosThetaStarCut and massAsymCut: 
						massAve_cutTau21_A.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21_A.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21_A.Fill( massAsym, J2CosThetaStar, scale )
					elif cosThetaStarCut and not massAsymCut: 
						massAve_cutTau21_B.Fill( massAve, scale )
						massAve_cutTau21_Bkg.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21_B.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21_B.Fill( massAsym, J2CosThetaStar, scale )
					elif not cosThetaStarCut and massAsymCut: 
						massAve_cutTau21_D.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21_D.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21_D.Fill( massAsym, J2CosThetaStar, scale )
					else:
						massAve_cutTau21_C.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21_C.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21_C.Fill( massAsym, J2CosThetaStar, scale )

					if cosThetaStarCutAway and massAsymCutAway: 
						massAve_cutTau21Away_A.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21Away_A.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21Away_A.Fill( massAsym, J2CosThetaStar, scale )
					elif cosThetaStarCutAway and not massAsymCutAway: 
						massAve_cutTau21Away_B.Fill( massAve, scale )
						massAve_cutTau21Away_Bkg.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21Away_B.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21Away_B.Fill( massAsym, J2CosThetaStar, scale )
					elif not cosThetaStarCutAway and massAsymCutAway: 
						massAve_cutTau21Away_D.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21Away_D.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21Away_D.Fill( massAsym, J2CosThetaStar, scale )
					else:
						massAve_cutTau21Away_C.Fill( massAve, scale )
						massAsymVsCosTheta_cutTau21Away_C.Fill( massAsym, J1CosThetaStar, scale )
						massAsymVsCosTheta_cutTau21Away_C.Fill( massAsym, J2CosThetaStar, scale )

					
					if cosThetaStarCut:
						massAve_cutCosTheta.Fill( massAve, scale )
						massAsymmetry_cutCosTheta.Fill( massAsym, scale )
						deltaEtaDijet_cutCosTheta.Fill( deltaEtaDijet, scale )
						jet1Tau31_cutCosTheta.Fill( jet1Tau31, scale )
						jet2Tau31_cutCosTheta.Fill( jet2Tau31, scale )
						jet1Tau21_cutCosTheta.Fill( jet1Tau21, scale )
						jet2Tau21_cutCosTheta.Fill( jet2Tau21, scale )
						jet1Tau32_cutCosTheta.Fill( jet1Tau32, scale )
						jet2Tau32_cutCosTheta.Fill( jet2Tau32, scale )
						jet1CosThetaStar_cutCosTheta.Fill( J1CosThetaStar, scale )
						jet2CosThetaStar_cutCosTheta.Fill( J2CosThetaStar, scale )
						jet1SubjetPtRatio_cutCosTheta.Fill( jet1SubjetPtRatio, scale )
						jet2SubjetPtRatio_cutCosTheta.Fill( jet2SubjetPtRatio, scale )
			
						if massAsymCut:
							massAve_cutMassAsym.Fill( massAve, scale )
							HT_cutMassAsym.Fill( HT, scale )
							#tmpHT_cutMassAsym.Fill( HT, scale )
							#tmp2HT_cutMassAsym.Fill( HT, scale )
							#tmp3HT_cutMassAsym.Fill( HT, scale )
							massAsymmetry_cutMassAsym.Fill( massAsym, scale )
							deltaEtaDijet_cutMassAsym.Fill( deltaEtaDijet, scale )
							jet1Tau31_cutMassAsym.Fill( jet1Tau31, scale )
							jet2Tau31_cutMassAsym.Fill( jet2Tau31, scale )
							jet1Tau21_cutMassAsym.Fill( jet1Tau21, scale )
							jet2Tau21_cutMassAsym.Fill( jet2Tau21, scale )
							jet1Tau32_cutMassAsym.Fill( jet1Tau32, scale )
							jet2Tau32_cutMassAsym.Fill( jet2Tau32, scale )
							jet1CosThetaStar_cutMassAsym.Fill( J1CosThetaStar, scale )
							jet2CosThetaStar_cutMassAsym.Fill( J2CosThetaStar, scale )
							jet1SubjetPtRatio_cutMassAsym.Fill( jet1SubjetPtRatio, scale )
							jet2SubjetPtRatio_cutMassAsym.Fill( jet2SubjetPtRatio, scale )

				
				
	massAve_cutTau21_Bkg.Multiply( massAve_cutTau21_D )
	massAve_cutTau21_Bkg.Divide( massAve_cutTau21_C )

	massAve_cutTau21Away_Bkg.Multiply( massAve_cutTau21Away_D )
	massAve_cutTau21Away_Bkg.Divide( massAve_cutTau21Away_C )
	'''
	tmpHT_cutCosThetaMassAsym.Divide( tmpHT_cutNOTau21 )
	tmp2HT_cutCosThetaMassAsym.Divide( tmpHT_cutNOTau21CosTheta )
	tmp3HT_cutCosThetaMassAsym.Divide( tmpHT_cutNOTau21CosThetaMassAsym )

	for k in range( len( variablesBkg ) ):
		try: 
			binNewWeight = tmpHT_cutCosThetaMassAsym.GetXaxis().FindBin( variablesBkg[k][0] )
			newScale = tmpHT_cutCosThetaMassAsym.GetBinContent( binNewWeight ) 
		except IndexError: newScale = 0
		if (newScale <= 1):
			HT_cutNOTau21_ReScale.Fill( variablesBkg[k][0], newScale )
			massAve_cutNOTau21_ReScale.Fill( variablesBkg[k][1], newScale )

	for k in range( len( variablesBkg2 ) ):
		try: 
			binNewWeight = tmp2HT_cutCosThetaMassAsym.GetXaxis().FindBin( variablesBkg2[k][0] )
			newScale = tmp2HT_cutCosThetaMassAsym.GetBinContent( binNewWeight ) 
		except IndexError: newScale = 0
		if (newScale <= 1):
			HT_cutNOTau21CosTheta_ReScale.Fill( variablesBkg2[k][0], newScale )
			massAve_cutNOTau21CosTheta_ReScale.Fill( variablesBkg2[k][1], newScale )

	for k in range( len( variablesBkg3 ) ):
		try: 
			binNewWeight = tmp2HT_cutCosThetaMassAsym.GetXaxis().FindBin( variablesBkg3[k][0] )
			newScale = tmp2HT_cutCosThetaMassAsym.GetBinContent( binNewWeight ) 
		except IndexError: newScale = 0
		if (newScale <= 1):
			HT_cutNOTau21CosThetaMassAsym_ReScale.Fill( variablesBkg3[k][0], newScale )
			massAve_cutNOTau21CosThetaMassAsym_ReScale.Fill( variablesBkg3[k][1], newScale )
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
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
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
		inputFileName = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	elif 'Data' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_JetHTRun2015D-All_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	elif 'TTJets' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	elif 'WJets' in samples:
		inputFileName = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	elif 'WW' in samples:
		inputFileName = 'Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	elif 'ZJets' in samples:
		inputFileName = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	elif 'ZZ' in samples:
		inputFileName = 'Rootfiles/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	elif 'WZ' in samples:
		inputFileName = 'Rootfiles/RUNAnalysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	else: 
		#inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15MiniAODv2-74X_Asympt25ns_v08_v04.root'
		#for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800', '1800to2400', '2400to3200', '3200toInf' ]: 
		#nputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15MiniAODv2-74X_'+PU+'_v08_v01.root'
		inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'

	p = Process( target=myAnalyzer, args=( inputFileName, couts, grooming ) )
	p.start()
	p.join()
