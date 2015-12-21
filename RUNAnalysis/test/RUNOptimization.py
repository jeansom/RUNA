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
def RUNOptimization( QCDSample, SigSample, folder, listOfHist, cuts, mass ):
	"""docstring for RUNOptimization"""
	

	QCDFile = TFile( QCDSample, 'read' )
	SigFile = TFile( SigSample, 'read' )

	for cut in cuts:
		dictROC = {}
		f1 = TF1("f1","x",0,1)
		f1.SetLineColor(1)
		f1.SetLineStyle(3)
		for hist in listOfHist:
			QCDHisto = QCDFile.Get( folder+hist[0]+cut )
			QCDTotal = QCDHisto.Integral() 

			SigHisto = SigFile.Get( folder+hist[0]+cut )
			SigTotal = SigHisto.Integral() 

			ibinCut = 0
			if ( len( hist ) > 2 ): ibinCut = SigHisto.GetXaxis().FindBin( hist[2] )

			numBins = QCDHisto.GetNbinsX()
			minBin = QCDHisto.GetXaxis().GetXmin()
			maxBin = QCDHisto.GetXaxis().GetXmax()
			QCDEffHisto = TH1F(hist[0]+cut+"_QCDROC", hist[0]+cut+"_QCDROC; "+hist[0]+cut, numBins, minBin, maxBin )
			SigEffHisto = TH1F(hist[0]+cut+"_SigROC", hist[0]+cut+"_SigROC; "+hist[0]+cut, numBins, minBin, maxBin )
			SigAxis = TGaxis(0, 1.1, 1, 1.1, minBin, maxBin, 510,"-")
			QCDAxis = TGaxis(1.1, 1, 1.099, 0, minBin, maxBin, 510,"-")

			QCDROCValues = []	
			SigROCValues = []	
			SigROCBins = []	
			SigROCLowEdge = []	
			firstBin =  SigHisto.FindFirstBinAbove( 0, 1 )
			lastBin =  SigHisto.FindLastBinAbove( 0, 1 )+1 
			for ibin in range( firstBin, lastBin ):
				if hist[1]:
					#print ibin, SigHisto.GetXaxis().GetBinLowEdge(ibin), SigHisto.Integral( 0, ibin ), SigHisto.Integral( firstBin, ibin ) #, SigTotal, SigHisto.Integral( 0, ibin+1 ) / SigTotal,  QCDHisto.GetXaxis().GetBinLowEdge(ibin), QCDHisto.Integral( 0, ibin+1 ) , QCDTotal, QCDHisto.Integral( 0, ibin+1 ) / QCDTotal
					effQCD = 1 - QCDHisto.Integral( firstBin, ibin ) / QCDTotal 
					QCDEffHisto.SetBinContent( ibin, effQCD )
					QCDROCValues.append( effQCD )

					effSig = SigHisto.Integral( firstBin, ibin ) / SigTotal 
					SigEffHisto.SetBinContent( ibin, effSig )
					SigROCValues.append( effSig )
					SigROCBins.append( ibin )
					SigROCLowEdge.append( SigHisto.GetXaxis().GetBinLowEdge(ibin+1) )
					SigAxis = TGaxis(0, 1.1, 1, 1.1, minBin, maxBin, 510,"-")
					QCDAxis = TGaxis(1.1, 1, 1.099, 0, minBin, maxBin, 510,"-")

				else:
					effQCD = 1 - QCDHisto.Integral( ibin, lastBin ) / QCDTotal 
					QCDEffHisto.SetBinContent( ibin, effQCD )
					QCDROCValues.append( effQCD )

					effSig = SigHisto.Integral( ibin, lastBin ) / SigTotal 
					SigEffHisto.SetBinContent( ibin, effSig )
					SigROCValues.append( effSig )
					SigROCBins.append( ibin )
					SigROCLowEdge.append( SigHisto.GetXaxis().GetBinLowEdge(ibin+1) )
					SigAxis = TGaxis(1, 1.099, 0, 1.1, minBin, maxBin, 510,"")
					QCDAxis = TGaxis(1.1, 0, 1.1, 1, minBin, maxBin, 510,"+L")

			QCDROCArray = np.asarray( QCDROCValues )
			SigROCArray = np.asarray( SigROCValues )
			SigROCBinsArray = np.asarray( SigROCBins )
			SigROCLowEdgeArray = np.asarray( SigROCLowEdge )
			if ( len(hist) > 2 ): 
				x = find_nearest(SigROCLowEdgeArray, hist[2])
				print 'For cut', hist[2], 'in', hist[0]+cut, 'effSig: ', SigROCArray[x], ', effQCD: ', QCDROCArray[x]
			if ( len(hist) > 3 ): 
				y = find_nearest( SigROCArray, hist[3] )
				print 'Optimal value for ', hist[0]+cut, SigROCLowEdge[y], 'is', SigROCArray[y]
			
			ROC = TGraph( len( QCDROCArray ), SigROCArray, QCDROCArray )		
			dictROC[ hist[0] ] = ROC

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
	factory = TMVA.Factory( "TMVATraining"+bkgName, outputFile, "!V:!Silent:Transformations=I;D;P;G,D:AnalysisType=Classification")

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
	sigCut = TCut("massAve>"+str(int(mass)-30)+" && massAve < "+str(int(mass)+30))
	bkgCut = TCut("")
	factory.PrepareTrainingAndTestTree(sigCut, bkgCut,
			"nTrain_Signal=0:nTrain_Background=100000:SplitMode=Random:NormMode=NumEvents:!V")

	# define multivariate methods to be run
	'''
	factory.BookMethod( TMVA.Types.kCuts, 
			"Cuts", 
			"!H:!V:"\
			"FitMethod=MC:"\
			"EffSel:"\
			"SampleSize=200000:"\
			"VarProp=FSmart" )
	factory.BookMethod( TMVA.Types.kCuts, 
			"CutsGA",
			"H:!V:"\
			"FitMethod=GA:"\
			#"CutRangeMin[0]=-10:"\
			#"CutRangeMax[0]=10:"\
			#"VarProp[1]=FMax:"\  ## varProp for gaussian shape variables
			#"EffSel:Steps=30:"\  ## Default 40 
			"Cycles=3:"\
			#"PopSize=400:"\ ## Default 300
			#"SC_steps=10:"\  ## Default 10 
			#"SC_rate=5:"\  ## default 5
			#"SC_factor=0.95"  ## default
			)
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
	'''
	factory.BookMethod( TMVA.Types.kBDT, 
			"BDTG",
			"!H:!V:NTrees=1000:"\
			"BoostType=Grad:"\
			"Shrinkage=0.30:"\
			"UseBaggedGrad:"\
			"GradBaggingFraction=0.5:"\
			"SeparationType=GiniIndex:"\
			"nCuts=20:"\
			"NNodesMax=5" )

	factory.TrainAllMethods()  
	factory.TestAllMethods()
	factory.EvaluateAllMethods()

	outputFile.Close()
	del factory

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
	parser.add_argument( '-i', '--inputFiles', action='store',  dest='inputFiles', default='Mini', help='From my root files: RUNMiniAnalysis or RUNAnalysis.' )
	parser.add_argument( '-s', '--selection', action='store',  dest='selection', default='', help='Selection, like _cutDEta' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='Simple', help='Process: simple or TMVA' )
	parser.add_argument( '-v', '--version', action='store',  dest='version', default='Boosted', help='Variable to optimize, as histogram in rootfile.' )

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

	bkgSamples = {}
	#bkgSamples[ 'QCDPtAll' ] = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	bkgSamples[ 'WWTo4Q' ] = 'Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	bkgSamples[ 'WJetsToQQ' ] = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	#bkgSamples[ 'ZZTo4Q' ] = 'Rootfiles/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	#bkgSamples[ 'ZJetsToQQ' ] = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	#bkgSamples[ 'TTJets' ] = 'Rootfiles/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'

	QCDSample = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	WWJetsSample = 'Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
	SigSample = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root'
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
		#[ 'Boosted', "massAve", True ],
		[ 'Boosted', "massAsym", True, 0.1, 0.40 ],
		[ 'Boosted', "jet1CosThetaStar", True, 0.3, 0.8 ],
		[ 'Boosted', "jet2CosThetaStar", True, 0.3, 0.8 ],
		#[ 'Boosted', "jet1Tau1", True ],
		#[ 'Boosted', "jet1Tau2", True ],
		#[ 'Boosted', "jet1Tau3", True ],
		[ 'Boosted', "jet1Tau21", True, 1.0, 0.7 ],
		[ 'Boosted', "jet1Tau31", True, 0.5, 0.8 ],
		[ 'Boosted', "jet1Tau32", True ],
		#[ 'Boosted', "jet2Tau1", True ],
		#[ 'Boosted', "jet2Tau2", True ],
		#[ 'Boosted', "jet2Tau3", True ],
		[ 'Boosted', "jet2Tau21", True, 0.5, 0.7 ],
		[ 'Boosted', "jet2Tau31", True, 0.5, 0.6 ],
		[ 'Boosted', "jet2Tau32", True ],
		[ 'Boosted', "deltaEtaDijet", True, 1, 0.80 ],
		[ 'Boosted', "jet1SubjetPtRatio", True ],
		[ 'Boosted', "jet2SubjetPtRatio", True ],
	]

	if 'Simple' in process: 
		
		if 'all' in selection: 
			if 'Boosted' in version: cuts = [ '_cutDijet', '_cutMassAsym', '_cutTau21', '_cutCosTheta' ]
			elif 'Resolved' in version: cuts = [ '', '_cutMassPair', '_cutDEta' ]
		else:
			cuts = [ selection ]

		if 'Resolved' in version: 
			folder = ''
			variables = [ x[1:] for x in var if ( 'Resolved' in x[0] ) ]
		else: 
			folder = '' #version+'AnalysisPlotsPruned/'
			variables = [ x[1:] for x in var if ( 'Boosted' in x[0] ) ]

		RUNOptimization( QCDSample, SigSample, folder, variables, cuts, str(mass) )

	elif 'TMVA' in process:
		variables = [ x[1] for x in var if ( version in x[0] ) ]
		outputFileName = 'Rootfiles/RUN'+version+'OptimizationStudiesTMP.root'
		#for sample in bkgSamples: 
			#p0 = Process( target=RUNTMVATraining, args=( bkgSamples[ sample ], SigSample, treename, 'Rootfiles/RUNTMVATraining_'+bkgSamples[ sample ].split('_')[1]+'.root', variables ) )
			#p0.start()
			#p0.join()
		p1 = Process( target=ApplicationCreateCombinedTree, args=( variables, outputFileName, bkgSamples, SigSample, treename ) )
		p1.start()
		p1.join()

	else:
		print 'No', process, 'in RUNOptimization. Have a nice day! :)'
