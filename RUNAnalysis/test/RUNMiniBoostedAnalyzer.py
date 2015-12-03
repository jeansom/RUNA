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
	HT_Tau21CosTheta 	= TH1F('HT_Tau21CosTheta', 'HT_Tau21CosTheta', 920, 800, 10000. )
	tmpHT_Tau21CosTheta 	= TH1F('tmpHT_Tau21CosTheta', 'tmpHT_Tau21CosTheta', 920, 800, 10000. )
	tmpHT_Tau21CosTheta2 	= TH1F('tmpHT_Tau21CosTheta2', 'tmpHT_Tau21CosTheta2', 920, 800, 10000. )
	massAve_Tau21CosThetaDEta 	= TH1F('massAve_Tau21CosThetaDEta', 'massAve_Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Tau21CosThetaDEta 	= TH1F('HT_Tau21CosThetaDEta', 'HT_Tau21CosThetaDEta', 920, 800, 10000. )

	massAve_Bkg1 	= TH1F('massAve_Bkg1', 'massAve_Bkg1', nBinsMass, 0, maxMass )
	HT_Bkg1 	= TH1F('HT_Bkg1', 'HT_Bkg1', nBinsMass, 0, maxMass )
	massAve_Bkg1Tau21 	= TH1F('massAve_Bkg1Tau21', 'massAve_Bkg1Tau21', nBinsMass, 0, maxMass )
	HT_Bkg1Tau21 	= TH1F('HT_Bkg1Tau21', 'HT_Bkg1Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg1Tau21CosTheta 	= TH1F('massAve_Bkg1Tau21CosTheta', 'massAve_Bkg1Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg1Tau21CosTheta 	= TH1F('HT_Bkg1Tau21CosTheta', 'HT_Bkg1Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg1Tau21CosThetaDEta 	= TH1F('massAve_Bkg1Tau21CosThetaDEta', 'massAve_Bkg1Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg1Tau21CosThetaDEta 	= TH1F('HT_Bkg1Tau21CosThetaDEta', 'HT_Bkg1Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg2 	= TH1F('massAve_Bkg2', 'massAve_Bkg2', nBinsMass, 0, maxMass )
	HT_Bkg2 	= TH1F('HT_Bkg2', 'HT_Bkg2', nBinsMass, 0, maxMass )
	massAve_Bkg2Tau21 	= TH1F('massAve_Bkg2Tau21', 'massAve_Bkg2Tau21', nBinsMass, 0, maxMass )
	HT_Bkg2Tau21 	= TH1F('HT_Bkg2Tau21', 'HT_Bkg2Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg2Tau21CosTheta 	= TH1F('massAve_Bkg2Tau21CosTheta', 'massAve_Bkg2Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg2Tau21CosTheta 	= TH1F('HT_Bkg2Tau21CosTheta', 'HT_Bkg2Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg2Tau21CosThetaDEta 	= TH1F('massAve_Bkg2Tau21CosThetaDEta', 'massAve_Bkg2Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg2Tau21CosThetaDEta 	= TH1F('HT_Bkg2Tau21CosThetaDEta', 'HT_Bkg2Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg3 	= TH1F('massAve_Bkg3', 'massAve_Bkg3', nBinsMass, 0, maxMass )
	HT_Bkg3 	= TH1F('HT_Bkg3', 'HT_Bkg3', nBinsMass, 0, maxMass )
	massAve_Bkg3Tau21 	= TH1F('massAve_Bkg3Tau21', 'massAve_Bkg3Tau21', nBinsMass, 0, maxMass )
	HT_Bkg3Tau21 	= TH1F('HT_Bkg3Tau21', 'HT_Bkg3Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg3Tau21CosTheta 	= TH1F('massAve_Bkg3Tau21CosTheta', 'massAve_Bkg3Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg3Tau21CosTheta 	= TH1F('HT_Bkg3Tau21CosTheta', 'HT_Bkg3Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg3Tau21CosThetaDEta 	= TH1F('massAve_Bkg3Tau21CosThetaDEta', 'massAve_Bkg3Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg3Tau21CosThetaDEta 	= TH1F('HT_Bkg3Tau21CosThetaDEta', 'HT_Bkg3Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg4 	= TH1F('massAve_Bkg4', 'massAve_Bkg4', nBinsMass, 0, maxMass )
	HT_Bkg4 	= TH1F('HT_Bkg4', 'HT_Bkg4', nBinsMass, 0, maxMass )
	massAve_Bkg4Tau21 	= TH1F('massAve_Bkg4Tau21', 'massAve_Bkg4Tau21', nBinsMass, 0, maxMass )
	HT_Bkg4Tau21 	= TH1F('HT_Bkg4Tau21', 'HT_Bkg4Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg4Tau21CosTheta 	= TH1F('massAve_Bkg4Tau21CosTheta', 'massAve_Bkg4Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg4Tau21CosTheta 	= TH1F('HT_Bkg4Tau21CosTheta', 'HT_Bkg4Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg4Tau21CosThetaDEta 	= TH1F('massAve_Bkg4Tau21CosThetaDEta', 'massAve_Bkg4Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg4Tau21CosThetaDEta 	= TH1F('HT_Bkg4Tau21CosThetaDEta', 'HT_Bkg4Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg5 	= TH1F('massAve_Bkg5', 'massAve_Bkg5', nBinsMass, 0, maxMass )
	HT_Bkg5 	= TH1F('HT_Bkg5', 'HT_Bkg5', nBinsMass, 0, maxMass )
	massAve_Bkg5Tau21 	= TH1F('massAve_Bkg5Tau21', 'massAve_Bkg5Tau21', nBinsMass, 0, maxMass )
	HT_Bkg5Tau21 	= TH1F('HT_Bkg5Tau21', 'HT_Bkg5Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg5Tau21CosTheta 	= TH1F('massAve_Bkg5Tau21CosTheta', 'massAve_Bkg5Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg5Tau21CosTheta 	= TH1F('HT_Bkg5Tau21CosTheta', 'HT_Bkg5Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg5Tau21CosThetaDEta 	= TH1F('massAve_Bkg5Tau21CosThetaDEta', 'massAve_Bkg5Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg5Tau21CosThetaDEta 	= TH1F('HT_Bkg5Tau21CosThetaDEta', 'HT_Bkg5Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg6 	= TH1F('massAve_Bkg6', 'massAve_Bkg6', nBinsMass, 0, maxMass )
	HT_Bkg6 	= TH1F('HT_Bkg6', 'HT_Bkg6', nBinsMass, 0, maxMass )
	massAve_Bkg6Tau21 	= TH1F('massAve_Bkg6Tau21', 'massAve_Bkg6Tau21', nBinsMass, 0, maxMass )
	HT_Bkg6Tau21 	= TH1F('HT_Bkg6Tau21', 'HT_Bkg6Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg6Tau21CosTheta 	= TH1F('massAve_Bkg6Tau21CosTheta', 'massAve_Bkg6Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg6Tau21CosTheta 	= TH1F('HT_Bkg6Tau21CosTheta', 'HT_Bkg6Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg6Tau21CosThetaDEta 	= TH1F('massAve_Bkg6Tau21CosThetaDEta', 'massAve_Bkg6Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg6Tau21CosThetaDEta 	= TH1F('HT_Bkg6Tau21CosThetaDEta', 'HT_Bkg6Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg7 	= TH1F('massAve_Bkg7', 'massAve_Bkg7', nBinsMass, 0, maxMass )
	HT_Bkg7 	= TH1F('HT_Bkg7', 'HT_Bkg7', nBinsMass, 0, maxMass )
	massAve_Bkg7Tau21 	= TH1F('massAve_Bkg7Tau21', 'massAve_Bkg7Tau21', nBinsMass, 0, maxMass )
	HT_Bkg7Tau21 	= TH1F('HT_Bkg7Tau21', 'HT_Bkg7Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg7Tau21CosTheta 	= TH1F('massAve_Bkg7Tau21CosTheta', 'massAve_Bkg7Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg7Tau21CosTheta 	= TH1F('HT_Bkg7Tau21CosTheta', 'HT_Bkg7Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg7Tau21CosThetaDEta 	= TH1F('massAve_Bkg7Tau21CosThetaDEta', 'massAve_Bkg7Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg7Tau21CosThetaDEta 	= TH1F('HT_Bkg7Tau21CosThetaDEta', 'HT_Bkg7Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg8 	= TH1F('massAve_Bkg8', 'massAve_Bkg8', nBinsMass, 0, maxMass )
	HT_Bkg8 	= TH1F('HT_Bkg8', 'HT_Bkg8', nBinsMass, 0, maxMass )
	massAve_Bkg8Tau21 	= TH1F('massAve_Bkg8Tau21', 'massAve_Bkg8Tau21', nBinsMass, 0, maxMass )
	HT_Bkg8Tau21 	= TH1F('HT_Bkg8Tau21', 'HT_Bkg8Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg8Tau21CosTheta 	= TH1F('massAve_Bkg8Tau21CosTheta', 'massAve_Bkg8Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg8Tau21CosTheta 	= TH1F('HT_Bkg8Tau21CosTheta', 'HT_Bkg8Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg8Tau21CosThetaDEta 	= TH1F('massAve_Bkg8Tau21CosThetaDEta', 'massAve_Bkg8Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg8Tau21CosThetaDEta 	= TH1F('HT_Bkg8Tau21CosThetaDEta', 'HT_Bkg8Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg9 	= TH1F('massAve_Bkg9', 'massAve_Bkg9', nBinsMass, 0, maxMass )
	HT_Bkg9 	= TH1F('HT_Bkg9', 'HT_Bkg9', nBinsMass, 0, maxMass )
	massAve_Bkg9Tau21 	= TH1F('massAve_Bkg9Tau21', 'massAve_Bkg9Tau21', nBinsMass, 0, maxMass )
	HT_Bkg9Tau21 	= TH1F('HT_Bkg9Tau21', 'HT_Bkg9Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg9Tau21CosTheta 	= TH1F('massAve_Bkg9Tau21CosTheta', 'massAve_Bkg9Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg9Tau21CosTheta 	= TH1F('HT_Bkg9Tau21CosTheta', 'HT_Bkg9Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg9Tau21CosThetaDEta 	= TH1F('massAve_Bkg9Tau21CosThetaDEta', 'massAve_Bkg9Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg9Tau21CosThetaDEta 	= TH1F('HT_Bkg9Tau21CosThetaDEta', 'HT_Bkg9Tau21CosThetaDEta', nBinsMass, 0, maxMass )

	massAve_Bkg10 	= TH1F('massAve_Bkg10', 'massAve_Bkg10', nBinsMass, 0, maxMass )
	HT_Bkg10 	= TH1F('HT_Bkg10', 'HT_Bkg10', nBinsMass, 0, maxMass )
	massAve_Bkg10Tau21 	= TH1F('massAve_Bkg10Tau21', 'massAve_Bkg10Tau21', nBinsMass, 0, maxMass )
	HT_Bkg10Tau21 	= TH1F('HT_Bkg10Tau21', 'HT_Bkg10Tau21', nBinsMass, 0, maxMass )
	massAve_Bkg10Tau21CosTheta 	= TH1F('massAve_Bkg10Tau21CosTheta', 'massAve_Bkg10Tau21CosTheta', nBinsMass, 0, maxMass )
	HT_Bkg10Tau21CosTheta 	= TH1F('HT_Bkg10Tau21CosTheta', 'HT_Bkg10Tau21CosTheta', nBinsMass, 0, maxMass )
	massAve_Bkg10Tau21CosThetaDEta 	= TH1F('massAve_Bkg10Tau21CosThetaDEta', 'massAve_Bkg10Tau21CosThetaDEta', nBinsMass, 0, maxMass )
	HT_Bkg10Tau21CosThetaDEta 	= TH1F('HT_Bkg10Tau21CosThetaDEta', 'HT_Bkg10Tau21CosThetaDEta', nBinsMass, 0, maxMass )
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
	'''
	massAve_NOMassAsym 	= TH1F('massAve_NOMassAsym', 'massAve_NOMassAsym', nBinsMass, 0, maxMass )
	massAve_NOMassAsym_ReScale 	= TH1F('massAve_NOMassAsym_ReScale', 'massAve_NOMassAsym_ReScale', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau21_ReScale 	= TH1F('massAve_NOMassAsymTau21_ReScale', 'massAve_NOMassAsymTau21_ReScale', nBinsMass, 0, maxMass )
	massAvevsHT_NOMassAsym 	= TH2D('massAvevsHT_NOMassAsym', 'massAvevsHT_NOMassAsym', nBinsMass, 0, maxMass, 920, 800, 10000 )
	HT_NOMassAsym 	= TH1F('HT_NOMassAsym', 'HT_NOMassAsym', 920, 800, 10000. )
	tmpHT_NOMassAsym 	= TH1F('tmpHT_NOMassAsym', 'tmpHT_NOMassAsym', 920, 800, 10000. )
	HT_NOMassAsym_ReScale 	= TH1F('HT_NOMassAsym_ReScale', 'HT_NOMassAsym_ReScale', 920, 800, 10000. )
	HT_NOMassAsymTau21 	= TH1F('HT_NOMassAsymTau21', 'HT_NOMassAsymTau21', 920, 800, 10000. )
	tmpHT_NOMassAsymTau21 	= TH1F('tmpHT_NOMassAsymTau21', 'tmpHT_NOMassAsymTau21', 920, 800, 10000. )
	HT_NOMassAsymTau21_ReScale 	= TH1F('HT_NOMassAsymTau21_ReScale', 'HT_NOMassAsymTau21_ReScale', 920, 800, 10000. )
	massAve_NOMassAsymTau21 	= TH1F('massAve_NOMassAsymTau21', 'massAve_NOMassAsymTau21', nBinsMass, 0, maxMass )
	massAvevsHT_NOMassAsymTau21 	= TH2D('massAvevsHT_NOMassAsymTau21', 'massAvevsHT_NOMassAsymTau21', nBinsMass, 0, maxMass, 920, 800, 10000 )
	massAve_NOMassAsymTau31 	= TH1F('massAve_NOMassAsymTau31', 'massAve_NOMassAsymTau31', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau31CosTheta 	= TH1F('massAve_NOMassAsymTau31CosTheta', 'massAve_NOMassAsymTau31CosTheta', nBinsMass, 0, maxMass )
	massAve_NOMassAsymTau31CosThetaDEta 	= TH1F('massAve_NOMassAsymTau31CosThetaDEta', 'massAve_NOMassAsymTau31CosThetaDEta', nBinsMass, 0, maxMass )
	
	'''
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
	'''

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
	variablesBkg = []
	variables2Bkg = []
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

		scale = 2476*puWeight*lumiWeight
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
		#trimmedMassVsHT.Fill( trimmedMass, HT )

		#### Apply standard selection
		triggerCut = ( ( HT > 700 ) and ( trimmedMass > 50 ) )  
		HTCut = ( HT > 900 )
		dijetCut =  ( numJets > 1 )
		subjetPtRatioCut = ( ( jet1SubjetPtRatio > 0.3 ) and ( jet2SubjetPtRatio > 0.3 )  )
		tau21Cut = ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) )
		tau31Cut = ( ( jet1Tau31 < 0.4 ) and ( jet2Tau31 < 0.4 ) )
		massAsymCut = ( massAsym < 0.1 ) 
		massAsymCutBkg1 = ( massAsym > 0.1 ) and ( massAsym < 0.2 ) 
		massAsymCutBkg2 = ( massAsym > 0.1 ) and ( massAsym < 0.3 ) 
		massAsymCutBkg3 = ( massAsym > 0.1 ) and ( massAsym < 0.4 ) 
		massAsymCutBkg4 = ( massAsym > 0.1 ) and ( massAsym < 0.5 ) 
		massAsymCutBkg5 = ( massAsym > 0.1 ) and ( massAsym < 0.6 ) 
		massAsymCutBkg6 = ( massAsym > 0.2 ) and ( massAsym < 0.3 ) 
		massAsymCutBkg7 = ( massAsym > 0.2 ) and ( massAsym < 0.4 ) 
		massAsymCutBkg8 = ( massAsym > 0.2 ) and ( massAsym < 0.5 ) 
		massAsymCutBkg9 = ( massAsym > 0.2 ) and ( massAsym < 0.6 ) 
		massAsymCutBkg10 = ( massAsym > 0.5 )  
		deltaEtaDijetCut = ( deltaEtaDijet < 1. ) 
		#cosThetaStarCut = ( abs( cosThetaStar ) < 0.3 ) 
		cosThetaStarCut = ( abs( J1CosThetaStar ) < 0.3 )  and ( abs( J2CosThetaStar ) < 0.3 )
		jetPtCut =  ( jet1Pt > 500 ) and ( jet2Pt > 450 )
		
		#if ( ( jet1Tau21 < 0.6 ) and ( jet2Tau21 < 0.6 ) ): massAve_Tau2106.Fill( massAve, scale )
		
		'''
		if not massAsymCut:
			massAvevsJet1Tau21_NOMasscut.Fill( massAve, jet1Tau21, scale )	
			massAvevsJet2Tau21_NOMasscut.Fill( massAve, jet2Tau21, scale )	
			massAvevsJet1Tau31_NOMasscut.Fill( massAve, jet1Tau31, scale )	
			massAvevsJet2Tau31_NOMasscut.Fill( massAve, jet2Tau31, scale )	
		'''
		#if HTCut and jetPtCut:
		if HTCut and dijetCut:
			if massAsymCut:
				'''
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
						tmpHT_Tau21CosTheta.Fill( HT, scale )
						tmpHT_Tau21CosTheta2.Fill( HT, scale )
						HT_Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Tau21CosThetaDEta.Fill( HT, scale )


			else:
				massAve_NOMassAsym.Fill( massAve, scale )
				HT_NOMassAsym.Fill( HT, scale )
				tmpHT_NOMassAsym.Fill( HT, scale )
				variablesBkg.append( [ HT, massAve, scale ] ) 
				massAvevsHT_NOMassAsym.Fill( massAve, HT, scale )
				if tau21Cut : 
					massAve_NOMassAsymTau21.Fill( massAve, scale )
					HT_NOMassAsymTau21.Fill( HT, scale )
					tmpHT_NOMassAsymTau21.Fill( HT, scale )
					variables2Bkg.append( [ HT, massAve, scale ] ) 
					massAvevsHT_NOMassAsymTau21.Fill( massAve, HT, scale )
				if tau31Cut : 
					massAve_NOMassAsymTau31.Fill( massAve, scale )
					if cosThetaStarCut: 
						massAve_NOMassAsymTau31CosTheta.Fill( massAve, scale )
						if deltaEtaDijetCut: 
							massAve_NOMassAsymTau31CosThetaDEta.Fill( massAve, scale )
			if massAsymCutBkg1:
				massAve_Bkg1.Fill( massAve, scale )
				HT_Bkg1.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg1Tau21.Fill( massAve, scale )
					HT_Bkg1Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg1Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg1Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg1Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg1Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg2:
				massAve_Bkg2.Fill( massAve, scale )
				HT_Bkg2.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg2Tau21.Fill( massAve, scale )
					HT_Bkg2Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg2Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg2Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg2Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg2Tau21CosThetaDEta.Fill( HT, scale )
	
			if massAsymCutBkg3:
				massAve_Bkg3.Fill( massAve, scale )
				HT_Bkg3.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg3Tau21.Fill( massAve, scale )
					HT_Bkg3Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg3Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg3Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg3Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg3Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg4:
				massAve_Bkg4.Fill( massAve, scale )
				HT_Bkg4.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg4Tau21.Fill( massAve, scale )
					HT_Bkg4Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg4Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg4Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg4Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg4Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg5:
				massAve_Bkg5.Fill( massAve, scale )
				HT_Bkg5.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg5Tau21.Fill( massAve, scale )
					HT_Bkg5Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg5Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg5Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg5Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg5Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg6:
				massAve_Bkg6.Fill( massAve, scale )
				HT_Bkg6.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg6Tau21.Fill( massAve, scale )
					HT_Bkg6Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg6Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg6Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg6Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg6Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg7:
				massAve_Bkg7.Fill( massAve, scale )
				HT_Bkg7.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg7Tau21.Fill( massAve, scale )
					HT_Bkg7Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg7Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg7Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg7Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg7Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg8:
				massAve_Bkg8.Fill( massAve, scale )
				HT_Bkg8.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg8Tau21.Fill( massAve, scale )
					HT_Bkg8Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg8Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg8Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg8Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg8Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg9:
				massAve_Bkg9.Fill( massAve, scale )
				HT_Bkg9.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg9Tau21.Fill( massAve, scale )
					HT_Bkg9Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg9Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg9Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg9Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg9Tau21CosThetaDEta.Fill( HT, scale )

			if massAsymCutBkg10:
				massAve_Bkg10.Fill( massAve, scale )
				HT_Bkg10.Fill( HT, scale )
				if tau21Cut:
					massAve_Bkg10Tau21.Fill( massAve, scale )
					HT_Bkg10Tau21.Fill( HT, scale )
					if cosThetaStarCut:
						massAve_Bkg10Tau21CosTheta.Fill( massAve, scale )
						HT_Bkg10Tau21CosTheta.Fill( HT, scale )
						if deltaEtaDijetCut:
							massAve_Bkg10Tau21CosThetaDEta.Fill( massAve, scale )
							HT_Bkg10Tau21CosThetaDEta.Fill( HT, scale )

	#tmpHT_Tau21CosTheta.Scale(1/tmpHT_Tau21CosTheta.Integral() )
	#tmpHT_NOMassAsym.Scale(1/tmpHT_NOMassAsym.Integral() )
	tmpHT_Tau21CosTheta.Divide( tmpHT_NOMassAsym )
	#tmpHT_NOMassAsymTau21.Scale(1/tmpHT_NOMassAsymTau21.Integral() )
	tmpHT_Tau21CosTheta2.Divide( tmpHT_NOMassAsymTau21 )

	for k in range( len( variablesBkg ) ):
		try: 
			binNewWeight = tmpHT_Tau21CosTheta.GetXaxis().FindBin( variablesBkg[k][0] )
			newScale = tmpHT_Tau21CosTheta.GetBinContent( binNewWeight ) * variablesBkg[k][2] 
		except IndexError: newScale = 0
		HT_NOMassAsym_ReScale.Fill( variablesBkg[k][0], newScale )
		massAve_NOMassAsym_ReScale.Fill( variablesBkg[k][1], newScale )

	for k in range( len( variables2Bkg ) ):
		try: 
			binNewWeight = tmpHT_Tau21CosTheta2.GetXaxis().FindBin( variables2Bkg[k][0] )
			newScale = tmpHT_Tau21CosTheta2.GetBinContent( binNewWeight ) * variables2Bkg[k][2] 
		except IndexError: newScale = 0
		HT_NOMassAsymTau21_ReScale.Fill( variables2Bkg[k][0], newScale )
		massAve_NOMassAsymTau21_ReScale.Fill( variables2Bkg[k][1], newScale )

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
		inputFileName = 'Rootfiles/RUNAnalysis_RPVSt'+str(mass)+'tojj_RunIISpring15MiniAODv2-74X_'+PU+'_v09_v01.root'
	elif 'Data' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_JetHTRun2015D-PromptReco-v4_v08_v01.root'
	elif 'Bkg' in samples: 
		inputFileName = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIISpring15MiniAODv2-74X_Asympt25ns_v03_v01.root'
		inputFileName = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600ToInf_RunIISpring15MiniAODv2-74X_Asympt25ns_v03_v01.root'
		inputFileName = 'Rootfiles/RUNAnalysis_TTJets_RunIISpring15MiniAODv2-74X_Asympt25ns_v03_v01.root'
	else: 
		#inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15MiniAODv2-74X_Asympt25ns_v08_v04.root'
		#for qcdBin in [ '170to300', '300to470', '470to600', '600to800', '800to1000', '1000to1400', '1400to1800', '1800to2400', '2400to3200', '3200toInf' ]: 
		#nputFileName = 'Rootfiles//RUNAnalysis_QCD_Pt_'+qcdBin+'_RunIISpring15MiniAODv2-74X_'+PU+'_v08_v01.root'
		inputFileName = 'Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root'

	p = Process( target=myAnalyzer, args=( inputFileName, couts, grooming ) )
	p.start()
	p.join()
