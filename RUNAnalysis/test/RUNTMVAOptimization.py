#!/usr/bin/env python
#----------------------------------------------------------------------
# File: train.py
# Description: example of classification with TMVA
# Created: 01-June-2013 INFN SOS 2013, Vietri sul Mare, Italy, HBP
#   adapted for CMSDAS 2015 Bari HBP
#----------------------------------------------------------------------
import os, sys, re
from math import *
from string import *
from time import sleep
from array import array
#from histutil import *
from ROOT import *
from multiprocessing import Process

#----------------------------------------------------------------------
def getTree(filename, treename):
	hfile = TFile(filename)
	if not hfile.IsOpen():
		print "** can't open file %s" % filename
		sys.exit()
	tree = hfile.Get(treename)
	if tree == None:
		print "** can't find tree %s" % treename
		sys.exit()
	return (hfile, tree)
#----------------------------------------------------------------------
#----------------------------------------------------------------------
def TMVATraining():
	print "\n", "="*80
	print "\tclassification with TMVA"
	print "="*80

	treename    = "RUNAMiniTree"    
	# get signal and background data for training/testing
	sigFile, sigTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_RPVSt350tojj_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPtAllFile, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCDPtAll_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	'''
	bkgQCDPt170to300, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_170to300_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt300to470, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_300to470_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt470to600, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_470to600_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt600to800, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_600to800_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt800to1000, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_800to1000_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt1000to1400, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_1000to1400_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt1400to1800, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_1400to1800_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt1800to2400, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_1800to2400_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt2400to3200, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_2400to3200_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	bkgQCDPt3200toInf, bkgQCDPtAllTree = getTree('Rootfiles/RUNMiniResolvedAnalysis_QCD_Pt_3200toInf_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v01.root', treename)
	'''

	# everything is done via a TMVA factory
	outputFile = TFile("TMVA_AllVariables.root", "recreate")
	factory = TMVA.Factory("sigbkg", outputFile, "!V:Transformations=I;N;D")
	factory.SetWeightExpression( "weight" )
	#factory.SetSignalWeightExpression("weight");
	#factory.SetBackgroundWeightExpression("weight");

	# define input variables
	#factory.AddSpectator("weight", 'D')
	factory.AddTarget("massAve", "F")
	factory.AddVariable("j4Pt", "F")
	factory.AddVariable("ht", "F")
	factory.AddVariable("deltaR", "F")
	factory.AddVariable("deltaEtaDijet1", "F")
	factory.AddVariable("deltaEtaDijet2", "F")
	factory.AddVariable("deltaEtaAveDijets", "F")
	factory.AddVariable("deltaEtaDijets", "F")
	factory.AddVariable("massPairing", "F")
	factory.AddVariable("cosThetaStarDijet1", "F")
	factory.AddVariable("cosThetaStarDijet2", "F")
	factory.AddVariable("deltaDijet1", "F")
	factory.AddVariable("deltaDijet2", "F")
	factory.AddVariable("xi1", "F")
	factory.AddVariable("xi2", "F")

	# define from which trees data are to be taken
	factory.AddSignalTree( sigTree ) 
	factory.AddBackgroundTree( bkgQCDPtAllTree ) 
	'''
	factory.AddBackgroundTree( bkgQCDPt170to300 ) 
	factory.AddBackgroundTree( bkgQCDPt300to470 ) 
	factory.AddBackgroundTree( bkgQCDPt470to600 ) 
	factory.AddBackgroundTree( bkgQCDPt600to800 ) 
	factory.AddBackgroundTree( bkgQCDPt800to1000 ) 
	factory.AddBackgroundTree( bkgQCDPt1000to1400 ) 
	factory.AddBackgroundTree( bkgQCDPt1400to1800 ) 
	factory.AddBackgroundTree( bkgQCDPt1800to2400 ) 
	factory.AddBackgroundTree( bkgQCDPt2400to3200 ) 
	factory.AddBackgroundTree( bkgQCDPt3200toInf ) 
	'''

	# remove problematic events and specify how
	# many events are to be used
	# for training and testing
	factory.PrepareTrainingAndTestTree(TCut("ht>900"),
				       "nTrain_Signal=2000:"\
				       "nTest_Signal=3000:"\
				       "nTrain_Background=50000:"\
				       "nTest_Background=100000:"\
				       "!V" )

	# define multivariate methods to be run
	'''
	factory.BookMethod( TMVA.Types.kCuts, 
			"Cuts", 
			"!H:!V:"\
			"FitMethod=MC:"\
			"EffSel:"\
			"SampleSize=200000:"\
			"VarProp=FSmart" )
	'''
	factory.BookMethod( TMVA.Types.kMLP,
			"MLP",
			"!H:!V:"\
			"VarTransform=N:"\
			"HiddenLayers=10:"\
			"TrainingMethod=BFGS")

	factory.BookMethod( TMVA.Types.kBDT,
			"BDT",
			"!V:"\
			"BoostType=AdaBoost:"\
			"NTrees=400:"\
			"nEventsMin=100:"\
			"nCuts=50")

	factory.TrainAllMethods()  
	factory.TestAllMethods()
	factory.EvaluateAllMethods()

	outputFile.Close()
#----------------------------------------------------------------------


if __name__ == '__main__':

	try:
		p = Process( target=TMVATraining )
		p.start()
		p.join()
	except KeyboardInterrupt:
		print "\nciao"

