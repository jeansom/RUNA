#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time, re
from math import *
from string import *
from array import array
import argparse
from ROOT import * 
from multiprocessing import Process
import numpy as np
try: import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError: 
	sys.path.append('../python') 
	import tdrstyle as tdrstyle


TMVA.Tools.Instance()
gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

##### Support functions
def checkLumi( Run, Lumi, NumEvent):
	"""docstring for checkLumi"""
	result = False
	allEvents = 'Run: '+str(Run)+' LumiSection: '+str(Lumi)+' Event: '+str(NumEvent)
	with open('boostedEventsRPV100tojj.txt') as f:
		lines = f.readlines()
		for i in lines: 
			if allEvents == i: result = True

	return result

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin()
	return idx

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
### Main Optimization
def RUNOptimization( BkgSamples, SigSample, treename, varList, mass, window ):
	"""docstring for RUNOptimization"""
	
	outputFile = TFile( 'test.root', "RECREATE" )
	
	allHistos = {}
	for var in varList: 
		allHistos[ var[0]+'_Sig' ] = TH1F( var[0]+"_Sig", var[0]+"_Sig", var[1], var[2], var[3] )
		for bkgSample in BkgSamples: 
			allHistos[ var[0]+'_'+bkgSample ] = TH1F( var[0]+"_"+bkgSample, var[0]+"_"+bkgSample, var[1], var[2], var[3] )
			allHistos[ var[0]+"_"+bkgSample+"_BkgROC"] = TH1F( var[0]+"_"+bkgSample+"_BkgROC", var[0]+"_"+bkgSample+"_BkgROC; "+var[0], var[1], var[2], var[3] )
			allHistos[ var[0]+"_"+bkgSample+"_SigROC"] = TH1F( var[0]+"_"+bkgSample+"_SigROC", var[0]+"_"+bkgSample+"_SigROC; "+var[0], var[1], var[2], var[3] )

	print '-'*40
	print '---- Signal'
	SigFile, sigEvents = getTree( SigSample, treename )
	sigNumEntries = sigEvents.GetEntriesFast()
	for i in xrange(sigNumEntries):
		sigEvents.GetEntry(i)
		for var in varList: 
			sigMassAve = sigEvents.massAve
			if ( ( sigMassAve > int(mass)-window ) and ( sigMassAve < int(mass)+window  ) ): allHistos[ var[0]+"_Sig" ].Fill( getattr( sigEvents, var[0] ) )
	

	for bkgSample in BkgSamples: 
		print '-'*40
		print '---- ', bkgSample
		BkgFile, bkgEvents = getTree( BkgSamples[ bkgSample ], treename )
		bkgNumEntries = bkgEvents.GetEntriesFast()
		for i in xrange(bkgNumEntries):
			bkgEvents.GetEntry(i)
			for var in varList: 
				bkgMassAve = bkgEvents.massAve
				if ( ( bkgMassAve > int(mass)-window ) and ( bkgMassAve < int(mass)+window  ) ): 
					allHistos[ var[0]+"_"+bkgSample ].Fill( getattr( bkgEvents, var[0] ) )

		for var in varList:
			BkgHisto = allHistos[ var[0]+"_"+bkgSample ]
			BkgTotal = BkgHisto.Integral() 

			SigHisto = allHistos[ var[0]+"_Sig" ]
			SigTotal = SigHisto.Integral() 

			ibinCut = 0
			#if ( len( var ) > 2 ): ibinCut = SigHisto.GetXaxis().FindBin( var[2] )

			BkgROCValues = []	
			SigROCValues = []	
			SigROCBins = []	
			SigROCLowEdge = []	
			firstBin =  SigHisto.FindFirstBinAbove( 0, 1 )
			lastBin =  SigHisto.FindLastBinAbove( 0, 1 )+1 
			for ibin in range( firstBin, lastBin ):
				if var[4]:
					#print ibin, SigHisto.GetXaxis().GetBinLowEdge(ibin), SigHisto.Integral( 0, ibin ), SigHisto.Integral( firstBin, ibin ) #, SigTotal, SigHisto.Integral( 0, ibin+1 ) / SigTotal,  BkgHisto.GetXaxis().GetBinLowEdge(ibin), BkgHisto.Integral( 0, ibin+1 ) , BkgTotal, BkgHisto.Integral( 0, ibin+1 ) / BkgTotal
					effBkg = 1 - BkgHisto.Integral( firstBin, ibin ) / BkgTotal 
					allHistos[ var[0]+"_"+bkgSample+"_BkgROC" ].SetBinContent( ibin, effBkg )
					BkgROCValues.append( effBkg )

					effSig = SigHisto.Integral( firstBin, ibin ) / SigTotal 
					allHistos[ var[0]+"_"+bkgSample+"_SigROC" ].SetBinContent( ibin, effSig )
					SigROCValues.append( effSig )
					SigROCBins.append( ibin )
					SigROCLowEdge.append( SigHisto.GetXaxis().GetBinLowEdge(ibin+1) )

				else:
					effBkg = 1 - BkgHisto.Integral( ibin, lastBin ) / BkgTotal 
					allHistos[ var[0]+"_"+bkgSample+"_BkgROC" ].SetBinContent( ibin, effBkg )
					BkgROCValues.append( effBkg )

					effSig = SigHisto.Integral( ibin, lastBin ) / SigTotal 
					allHistos[ var[0]+"_"+bkgSample+"_SigROC" ].SetBinContent( ibin, effSig )
					SigROCValues.append( effSig )
					SigROCBins.append( ibin )
					SigROCLowEdge.append( SigHisto.GetXaxis().GetBinLowEdge(ibin+1) )

			BkgROCArray = np.asarray( BkgROCValues )
			SigROCArray = np.asarray( SigROCValues )
			SigROCBinsArray = np.asarray( SigROCBins )
			SigROCLowEdgeArray = np.asarray( SigROCLowEdge )
			'''
			if ( len(var) > 2 ): 
				x = find_nearest(SigROCLowEdgeArray, var[2])
				print 'For cut', var[2], 'in', var[0]+cut, 'effSig: ', SigROCArray[x], ', effBkg: ', BkgROCArray[x]
			if ( len(var) > 3 ): 
				y = find_nearest( SigROCArray, var[3] )
				print 'Optimal value for ', var[0]+cut, SigROCLowEdge[y], 'is', SigROCArray[y]
			
			'''
			ROC = TGraph( len( BkgROCArray ), SigROCArray, BkgROCArray )		
			ROC.Write(var[0]+"_"+bkgSample+"_ROC")
			#dictROC[  ] = ROC
		'''
		f1 = TF1("f1","x",0,1)
		f1.SetLineColor(1)
		f1.SetLineStyle(3)
		can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
		can.SetGrid()
		multiGraph = TMultiGraph()
		legend=TLegend(0.70,0.60,0.90,0.90)
		legend.SetFillStyle(0)
		legend.SetTextSize(0.03)
		dummyColor = 0
		for h in dictROC:
			dummyColor += 1
			if (dummyColor == 10): dummyColor = 40
			legend.AddEntry( dictROC[ h ], h, 'l' )
			dictROC[h].SetLineColor( dummyColor )
			dictROC[h].SetLineWidth( 2 )
			dictROC[h].SetMarkerStyle(4)
			multiGraph.Add( dictROC[h] )
		multiGraph.Draw("ALP")
		multiGraph.GetXaxis().SetRangeUser(-0.05,1.05)
		multiGraph.GetYaxis().SetRangeUser(-0.05,1.05)
		multiGraph.GetXaxis().SetTitle('Signal efficiency')
		multiGraph.GetYaxis().SetTitle('Bkg rejection')
		multiGraph.GetYaxis().SetTitleOffset(0.95)
		multiGraph.SetTitle('')
		f1.Draw("same")
		legend.Draw()
		can.SaveAs('Plots/'+version+'RPVSt'+mass+'_ROC'+cut+'.pdf')
		del can
		'''

	outputFile.Write()
	outputFile.Close()
	sys.exit(0)

#----------------------------------------------------------------------
def RUNTMVATraining( BkgSample, SigSample, treename, outputFileName, variables ):

	bkgName = outputFileName.split('_')[1].replace(".root",'')

	print "\n", "="*80
	print ' ---> Running Training for', bkgName
	print "="*80

	# get signal and background data for training/testing
	sigFile, sigTree = getTree( SigSample, treename )
	bkgFile, bkgTree = getTree( BkgSample, treename )

	# everything is done via a TMVA factory
	outputFile = TFile(outputFileName, "recreate")
	#factory = TMVA.Factory("sigbkg", outputFile, "!V:Transformations=I;N;D")
	factory = TMVA.Factory( "TMVATraining"+version+bkgName+"_RPVSt"+mass, outputFile, "!V:!Silent:Transformations=I;D;P;G,D:AnalysisType=Classification")

	# define input var
	factory.AddTarget( 'massAve', 'F' )
	for k in variables: factory.AddVariable( k, "F" )

	factory.SetWeightExpression( "weight" if ( 'Mini' in inputFiles ) else 'puWeight*lumiWeight' )

	# define from which trees data are to be taken
	factory.AddSignalTree( sigTree ) 
	factory.AddBackgroundTree( bkgTree ) 

	# remove problematic events and specify how
	# many events are to be used
	# for training and testing
	if ( ('QCD' in bkgName) or ('TTJets' in bkgName)): bkgTrain = 100000
	else: bkgTrain = 0
	if ('QCD' in bkgName) : bkgTest = 100000
	else: bkgTest = 0
	sigCut = TCut("massAve>"+str(int(mass)-30)+" && massAve < "+str(int(mass)+30))
	bkgCut = TCut("massAve>"+str(int(mass)-30)+" && massAve < "+str(int(mass)+30))
	factory.PrepareTrainingAndTestTree(sigCut, bkgCut,
			#"nTrain_Signal=0:nTrain_Background=100000:SplitMode=Random:NormMode=NumEvents:!V")
			"nTrain_Background="+str(bkgTrain)+":nTest_Background="+str(bkgTest)+":SplitMode=Random:NormMode=NumEvents:!V")

	# define multivariate methods to be run
	'''
	factory.BookMethod( TMVA.Types.kCuts, 
			"Cuts", 
			"!H:!V:"\
			"FitMethod=MC:"\
			"EffSel:"\
			"SampleSize=200000:"\
			"VarProp=FSmart" )
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
	factory.BookMethod( TMVA.Types.kBDT, 
			"BDTG",
			"!H:!V:NTrees=100:"\
			"BoostType=Grad:"\
			"Shrinkage=0.30:"\
			"UseBaggedGrad:"\
			"GradBaggingFraction=0.5:"\
			"SeparationType=GiniIndex:"\
			"nCuts=20:"\
			"NNodesMax=5" )
	'''
	factory.BookMethod( TMVA.Types.kCuts, 
			"CutsGA",
			"!H:!V:"\
			"FitMethod=GA:"\
			#"CutRangeMin[0]=-1:"\
			#"CutRangeMin[1]=0:"\
			#"CutRangeMax[0]=10:"\
			#"VarProp[1]=FMax:"\  ## varProp for gaussian shape variables
			#"EffSel:Steps=30:"\  ## Default 40 
			"Cycles=3:"\
			#"PopSize=400:"\ ## Default 300
			#"SC_steps=10:"\  ## Default 10 
			#"SC_rate=5:"\  ## default 5
			#"SC_factor=0.95"  ## default
			)

	factory.TrainAllMethods()  
	factory.TestAllMethods()
	factory.EvaluateAllMethods()

	outputFile.Close()
	del factory


def getOptimizeValues( variables, sample ):
	"""docstring for getOptimizeValues"""

	dictVariables = {}
	for k in variables: dictVariables[ k ] = array('f', [0.] )
	
	reader = TMVA.Reader( "!Color:Silent" )
	for k in variables: reader.AddVariable( k, dictVariables[k] )
	reader.BookMVA( "CutsGA method", "weights/TMVATraining"+version+sample+"_RPVSt"+mass+"_CutsGA.weights.xml" )
	#passed = reader.EvaluateMVA( "CutsGA method", 0.9 )
	mcuts = reader.FindMVA( "CutsGA method" )
	cutsMin = array( 'd', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] )        
        cutsMax = array( 'd', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] )
	finalValues = []
	for k in np.arange(0,1,0.01):
		mcuts.GetCuts( k, cutsMin, cutsMax )
		for ivar in range( len(variables) ):
			#print "... %.2g: %.5g < %s <= %.5g" % (k, cutsMin[ivar], variables[ivar], cutsMax[ivar])
			finalValues.append( [ k, variables[ivar], cutsMin[ivar], cutsMax[ivar] ] )
				
	return finalValues


def ApplicationCreateCombinedTree( variables, outputFileName, bkgSamples, SigSample, treename ):
	"""docstring for ApplicationCreateCombinedTree"""

	# Create a new root output file.
	#outfileName = TString( "tmva_example_multiple_backgrounds__applied.root" )
	outputFile = TFile( outputFileName, "RECREATE" )
	outputTree = TTree("multiBkg","multiple backgrounds tree")

	dictVariables = {}
	for k in variables:
		dictVariables[ k ] = array('f', [0.] )
		outputTree.Branch( k, dictVariables[ k ], k+'/F' )
	
	MassAve = array( 'f', [ 0.] )
	outputTree.Branch( 'massAve', MassAve, 'massAve/F' ) 
	Weight = array( 'f', [ 0.] )
	outputTree.Branch( 'weight', Weight, 'weight/F' ) 
	ClassID = array( 'f', [ 0.] )
	outputTree.Branch( 'classID', ClassID, 'classID/F' ) 
	for bkg in bkgSamples:
		dictVariables[ 'cls'+bkg ] = array('f', [0.] )
		outputTree.Branch( 'cls'+bkg, dictVariables[ 'cls'+bkg ], 'cls'+bkg+'/F' )

	# ===== create three readers for the three different signal/background classifications, .. one for each background
	readers = {}
	for bkg in bkgSamples:
		readers[ 'reader'+bkg ] = TMVA.Reader( "!Color:!Silent" )
		for k in variables: readers[ 'reader'+bkg ].AddVariable( k, dictVariables[k] )
		readers[ 'reader'+bkg ].BookMVA( "BDT method", "weights/TMVATraining"+bkg+"_BDTG.weights.xml" )

	sigFile, sigTree = getTree( SigSample, treename )
	for k in variables: sigTree.SetBranchAddress( k, dictVariables[ k ] )
	sigNumEntries = sigTree.GetEntriesFast()
	for i in xrange(sigNumEntries):
		sigTree.GetEntry(i)
		ClassID[0] = 0
		MassAve[0] = sigTree.massAve
		Weight[0] = sigTree.lumiWeight * sigTree.puWeight
		for bkg in bkgSamples:
			dictVariables[ 'cls'+bkg ][0] = readers[ 'reader'+bkg ].EvaluateMVA( 'BDT method' )
		outputTree.Fill()
	print ' ---> End of Signal Tree'


	dummyCls = 0
	for sample in bkgSamples: 
		dummyCls += 1
		bkgFile, bkgTree = getTree( bkgSamples[ sample ], treename )
		for k in variables: bkgTree.SetBranchAddress( k, dictVariables[ k ] )
		bkgNumEntries = bkgTree.GetEntriesFast()
		for i in xrange(bkgNumEntries):
			bkgTree.GetEntry(i)
			ClassID[0] = dummyCls 
			MassAve[0] = bkgTree.massAve
			Weight[0] = bkgTree.lumiWeight * bkgTree.puWeight
			for bkg in bkgSamples:
				dictVariables[ 'cls'+bkg ][0] = readers[ 'reader'+bkg ].EvaluateMVA( 'BDT method' )
			outputTree.Fill()
		print ' ---> End of', sample, 'Tree'
		
	#  write output tree
	outputFile.Write()
	outputFile.Close()

	del readers
	print "--- Created root file: ",  outputFileName, " containing the MVA output histograms."
	print "==> Application of readers is done! combined tree created"
#----------------------------------------------------------------------

#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-i', '--inputFiles', action='store',  dest='inputFiles', default='', help='From my root files: RUNMiniAnalysis or RUNAnalysis.')
	parser.add_argument( '-s', '--selection', action='store',  dest='selection', default='', help='Selection, like _cutDEta' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='Simple', help='Process: simple or TMVA' )
	parser.add_argument( '-v', '--version', action='store',  dest='version', default='Boosted', help='Variable to optimize, as histogram in rootfile.' )
	parser.add_argument( '-e', '--eff', action='store', dest='effS', type=int, default=0, help='Mass of the Stop' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	selection = args.selection
	process = args.process
	version = args.version
	inputFiles = args.inputFiles
	effS = args.effS

	bkgSamples = {}
	#bkgSamples[ 'QCDPtAll' ] = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	bkgSamples[ 'WWTo4Q' ] = 'Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#bkgSamples[ 'WJetsToQQ' ] = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#bkgSamples[ 'ZZTo4Q' ] = 'Rootfiles/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#bkgSamples[ 'ZJetsToQQ' ] = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#bkgSamples[ 'TTJets' ] = 'Rootfiles/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	bkgSamples[ 'WZ' ] = 'Rootfiles/RUNAnalysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'

	QCDSample = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	WWJetsSample = 'Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	SigSample = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	treename = "RUNATree/RUNATree" if ( 'Resolved' in version ) else 'RUNATreePruned/RUNATree'
	if 'Mini' in inputFiles:
		QCDSample = QCDSample.replace('Analysis', 'Mini'+version+'Analysis' )
		SigSample = SigSample.replace('Analysis', 'Mini'+version+'Analysis' )
		WWJetsSample = SigSample.replace('Analysis', 'Mini'+version+'Analysis' )
		treename = 'RUNAMiniTree'

	var = [
		[ 'Resolved', 'mindR', True, 1.5, 0.8 ],
		##[ 'Resolved', 'massAve', True ],
		#[ 'Resolved', 'deltaEtaDijet1', True,  ],
		#[ 'Resolved', 'deltaEtaDijet2', True,  ],
		#[ 'Resolved', 'deltaEtaAveDijets', True ],
		[ 'Resolved', 'deltaEtaDijets', True, .75, 0.65 ],
		[ 'Resolved', 'massAsymmetry', True, 0.2, 0.64 ],
		[ 'Resolved', 'cosThetaStarDijet1', True, 0.6, 0.70 ],
		[ 'Resolved', 'cosThetaStarDijet2', True, 0.6, 0.70 ],
		[ 'Resolved', 'deltaDijet1', False, 300, 0.6 ],
		[ 'Resolved', 'deltaDijet2', False, 300, 0.6 ],
		[ 'Resolved', 'xi1', True, 1, 0.6 ],
		[ 'Resolved', 'xi2', True , 1, 0.6],
		#[ 'Boosted', "HT", True ],
		#[ 'Boosted', "jet1Pt", True ],
		#[ 'Boosted', "jet2Pt", True ],
		##[ 'Boosted', "massAve", True ],
		[ 'Boosted', "massAsym", 20, 0., 1., True, 0.1, 0.40 ],
		#[ 'Boosted', "jet1CosThetaStar", True, 0.3, 0.8 ],
		[ 'Boosted', "jet2CosThetaStar", 20, 0., 1., True, 0.3, 0.8 ],
		#[ 'Boosted', "jet1Tau1", True ],
		#[ 'Boosted', "jet1Tau2", True ],
		#[ 'Boosted', "jet1Tau3", True ],
		#[ 'Boosted', "jet1Tau21", True, 1.0, 0.7 ],
		#[ 'Boosted', "jet1Tau31", True, 0.5, 0.8 ],
		#[ 'Boosted', "jet1Tau32", True ],
		#[ 'Boosted', "jet2Tau1", True ],
		#[ 'Boosted', "jet2Tau2", True ],
		#[ 'Boosted', "jet2Tau3", True ],
		[ 'Boosted', "jet2Tau21", 20, 0., 1., True, 0.5, 0.7 ],
		[ 'Boosted', "jet2Tau31", 20, 0., 1., True, 0.5, 0.6 ],
		[ 'Boosted', "jet2Tau32", 20, 0., 1., True ],
		#[ 'Boosted', "deltaEtaDijet", True, 1, 0.80 ],
		#[ 'Boosted', "jet1SubjetPtRatio", True ],
		#[ 'Boosted', "jet2SubjetPtRatio", True ],
	]

	if 'Simple' in process: 
		variables = [ x[1:] for x in var if ( version in x[0] ) ]
		p0 = Process( target=RUNOptimization, args=( bkgSamples, SigSample, treename, variables, mass, 10 ) )
		p0.start()
		p0.join()

	elif 'TMVA' in process:
		variables = [ x[1] for x in var if ( version in x[0] ) ]
		for sample in bkgSamples: 
			p0 = Process( target=RUNTMVATraining, args=( bkgSamples[ sample ], SigSample, treename, 'Rootfiles/RUNTMVATraining_'+bkgSamples[ sample ].split('_')[1]+'_RPVSt'+str(mass)+'.root', variables ) )
			p0.start()
			p0.join()
		#outputFileName = 'Rootfiles/RUN'+version+'OptimizationStudiesTMP.root'
		#p1 = Process( target=ApplicationCreateCombinedTree, args=( variables, outputFileName, bkgSamples, SigSample, treename ) )
		#p1.start()
		#p1.join()
	elif 'Print' in process:
		results = {}
		variables = [ x[1] for x in var if ( version in x[0] ) ]
		for sample in bkgSamples: 
			optValues = getOptimizeValues( variables, sample )
			results[ sample ] = optValues

		listSamples = []
		finalValues = {}
		print '\t', '\t'.join(str(p) for p in variables) 
		for k in results:
			listSamples.append( k )
			tmpMax = []
			for q in results[ k ]:
				if ( q[0] == effS/100. ): 
					for v in variables:
						if (q[1] == v ): tmpMax.append( q[3] )
			print k, '\t', '\t'.join(str(round(p, 2)) for p in tmpMax) 
				

	else:
		print 'No', process, 'in RUNOptimization. Have a nice day! :)'
