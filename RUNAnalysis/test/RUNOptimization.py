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
from collections import OrderedDict
from multiprocessing import Process
import numpy as np
try: 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
	from RUNA.RUNAnalysis.commonFunctions import *
except ImportError: 
	sys.path.append('../python') 
	import tdrstyle as tdrstyle
	from commonFunctions import *


TMVA.Tools.Instance()
gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)


#----------------------------------------------------------------------
### Main Optimization
def calcROCs( BkgSamples, SigSamples, treename, varList, mass, window, cutsList ):
	"""docstring for calcROCs"""
	
	outputFile = TFile( 'test.root', "RECREATE" )
	
	allHistos = {}
	allSumw2 = {}
	for var in varList: 
		allHistos[ var[0]+"_Sig" ] = TH1F( var[0]+"_Sig", var[0]+"_Sig", var[1], var[2], var[3] )
		allHistos[ var[0]+"_Sig" ].Sumw2()
		allSumw2[ var[0]+"_Sig" ] = 0
		for bkgSample in BkgSamples: 
			allHistos[ var[0]+'_'+bkgSample ] = TH1F( var[0]+"_"+bkgSample, var[0]+"_"+bkgSample, var[1], var[2], var[3] )
			allHistos[ var[0]+'_'+bkgSample ].Sumw2()
			allSumw2[ var[0]+"_"+bkgSample  ] = 0
			allHistos[ var[0]+"_"+bkgSample+"_BkgROC"] = TH1F( var[0]+"_"+bkgSample+"_BkgROC", var[0]+"_"+bkgSample+"_BkgROC; "+var[0], var[1], var[2], var[3] )
			allHistos[ var[0]+"_"+bkgSample+"_SigROC"] = TH1F( var[0]+"_"+bkgSample+"_SigROC", var[0]+"_"+bkgSample+"_SigROC; "+var[0], var[1], var[2], var[3] )

	signalName = ''
	for sigSample in SigSamples: 
		SigFile, sigEvents, sigNumEntries = getTree( SigSamples[ sigSample ], treename )
		signalName = sigSample
		d = 0
		print '-'*40
		print '---- Signal ', signalName
		for i in xrange(sigNumEntries):
			sigEvents.GetEntry(i)
			#---- progress of the reading --------
			fraction = 10.*i/(1.*sigNumEntries)
			if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
			d = TMath.FloorNint(fraction)
			sigCutsList = []
			sigSF = sigEvents.lumiWeight * sigEvents.puWeight
			sigMassAve = ( sigEvents.prunedMassAve if 'Boosted' in version else sigEvents.avgMass  )
			if ( ( sigMassAve > int(mass)-window ) and ( sigMassAve < int(mass)+window  ) ): 
				if len(cutsList) > 0:
					for cutVar in cutsList: 
						if cutVar[4]: sigCutsList.append( True ) if ( getattr( sigEvents, cutVar[0] ) < cutVar[5] ) else sigCutsList.append( False )
						else: sigCutsList.append( True ) if ( getattr( sigEvents, cutVar[0] ) > cutVar[5] ) else sigCutsList.append( False )
				if all( sigCutsList ): 
					signalW2 = 0
					for sigVar in varList: 
						allHistos[ sigVar[0]+"_Sig" ].Fill( getattr( sigEvents, sigVar[0] ), sigSF )
						allSumw2[ sigVar[0]+"_Sig" ] += sigSF*sigSF
		

	allROCs = {}
	for bkgSample in BkgSamples: 
		print '-'*40
		print '---- ', bkgSample
		BkgFile, bkgEvents, bkgNumEntries = getTree( BkgSamples[ bkgSample ][0], treename )
		print '---- ', bkgNumEntries
		d = 0
		tmpBkgSF = 0
		for i in xrange(bkgNumEntries):
			bkgEvents.GetEntry(i)
			#---- progress of the reading --------
			fraction = 10.*i/(1.*bkgNumEntries)
			if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
			d = TMath.FloorNint(fraction)
			#if i > 10000: break

			bkgCutsList = []
			bkgSF = bkgEvents.lumiWeight * bkgEvents.puWeight
			bkgMassAve = ( bkgEvents.prunedMassAve if 'Boosted' in version else bkgEvents.avgMass  )
			if ( ( bkgMassAve > int(mass)-window ) and ( bkgMassAve < int(mass)+window  ) ): 
				if len(cutsList) > 0:
					for cutVar in cutsList: 
						if cutVar[4]: bkgCutsList.append( True ) if ( getattr( bkgEvents, cutVar[0] ) < cutVar[5] ) else bkgCutsList.append( False )
						else: bkgCutsList.append( True ) if ( getattr( bkgEvents, cutVar[0] ) > cutVar[5] ) else bkgCutsList.append( False )
				if all( bkgCutsList ): 
					for bkgVar in varList: 
						allHistos[ bkgVar[0]+'_'+bkgSample ].Fill( getattr( bkgEvents, bkgVar[0] ), bkgSF )
						allSumw2[ bkgVar[0]+"_"+bkgSample ] += bkgSF*bkgSF
		
		for var in varList:
			BkgHisto = allHistos[ var[0]+"_"+bkgSample ]
			BkgTotal = BkgHisto.Integral() 

			SigHisto = allHistos[ var[0]+"_Sig" ]
			SigTotal = SigHisto.Integral() 

			ibinCut = 0
			#if ( len( var ) > 2 ): ibinCut = SigHisto.GetXaxis().FindBin( var[2] )

			BkgROCValues = []	
			BkgNumValues = []	
			BkgErrValues = []	
			SigROCValues = []	
			SigNumValues = []	
			SigErrValues = []	
			SigROCBins = []	
			SigROCLowEdge = []	
			firstBin =  SigHisto.FindFirstBinAbove( 0, 1 )
			lastBin =  SigHisto.FindLastBinAbove( 0, 1 )+1 
			#print 'Bfore', allSumw2[ bkgVar[0]+"_"+bkgSample ], TMath.Sqrt( allSumw2[ bkgVar[0]+"_"+bkgSample ] )
			#errorVal = Double(0)
			#ingral = BkgHisto.IntegralAndError( 0, 1, errorVal )
			#print '0'*10, ingral, errorVal
			for ibin in range( firstBin, lastBin ):
				if var[4]:
					#print ibin, SigHisto.GetXaxis().GetBinLowEdge(ibin), SigHisto.Integral( 0, ibin ), SigHisto.Integral( firstBin, ibin ) #, SigTotal, SigHisto.Integral( 0, ibin+1 ) / SigTotal,  BkgHisto.GetXaxis().GetBinLowEdge(ibin), BkgHisto.Integral( 0, ibin+1 ) , BkgTotal, BkgHisto.Integral( 0, ibin+1 ) / BkgTotal
					try: effBkg = 1 - BkgHisto.Integral( firstBin, ibin ) / BkgTotal 
					except ZeroDivisionError: effBkg = 1
					allHistos[ var[0]+"_"+bkgSample+"_BkgROC" ].SetBinContent( ibin, effBkg )
					BkgROCValues.append( effBkg )
					bkgErrorInt = Double(0)
					bkgIntegral = BkgHisto.IntegralAndError( firstBin, ibin, bkgErrorInt )
					BkgNumValues.append( bkgIntegral )
					BkgErrValues.append( TMath.Sqrt( bkgErrorInt ) )
					#print '1'*10, ingral, errorVal
					#print BkgHisto.GetSumOfWeights()
					#for i in BkgHisto.GetSumw2(): print i
					#print allSumw2[ var[0]+"_"+bkgSample ], TMath.Sqrt( allSumw2[ var[0]+"_"+bkgSample ] )

					try: effSig = SigHisto.Integral( firstBin, ibin ) / SigTotal 
					except ZeroDivisionError: effSig = 0
					allHistos[ var[0]+"_"+bkgSample+"_SigROC" ].SetBinContent( ibin, effSig )
					SigROCValues.append( effSig )
					SigROCBins.append( ibin )
					SigROCLowEdge.append( SigHisto.GetXaxis().GetBinLowEdge(ibin+1) )
					#SigNumValues.append( SigHisto.Integral( firstBin, ibin ) )
					sigErrorInt = Double(0)
					sigIntegral = SigHisto.IntegralAndError( firstBin, ibin, sigErrorInt )
					SigNumValues.append( sigIntegral )
					SigErrValues.append( TMath.Sqrt( sigErrorInt ) )

				else:
					effBkg = 1 - BkgHisto.Integral( ibin, lastBin ) / BkgTotal 
					allHistos[ var[0]+"_"+bkgSample+"_BkgROC" ].SetBinContent( ibin, effBkg )
					BkgROCValues.append( effBkg )
					#BkgNumValues.append( BkgHisto.Integral( ibin, lastBin ) )
					bkgErrorInt = Double(0)
					bkgIntegral = BkgHisto.IntegralAndError( ibin, lastBin, bkgErrorInt )
					BkgNumValues.append( bkgIntegral )
					BkgErrValues.append( TMath.Sqrt( bkgErrorInt ) )

					effSig = SigHisto.Integral( ibin, lastBin ) / SigTotal 
					allHistos[ var[0]+"_"+bkgSample+"_SigROC" ].SetBinContent( ibin, effSig )
					SigROCValues.append( effSig )
					SigROCBins.append( ibin )
					SigROCLowEdge.append( SigHisto.GetXaxis().GetBinLowEdge(ibin+1) )
					#SigNumValues.append( SigHisto.Integral( ibin, lastBin ) )
					sigErrorInt = Double(0)
					sigIntegral = SigHisto.IntegralAndError( ibin, lastBin, sigErrorInt )
					SigNumValues.append( sigIntegral )
					SigErrValues.append( TMath.Sqrt( sigErrorInt) )

			allROCs[ var[0]+"_"+bkgSample+"_ROC" ] = [ BkgROCValues, SigROCValues, SigROCBins, SigROCLowEdge, BkgNumValues, SigNumValues, BkgErrValues, SigErrValues ]

	outputTextFile = 'ROCfiles/ROC'+version+'Values_QCD'+qcd+'_'+signalName+'_cut'+str(len(cuts))+'_v1.txt'
	print '--- Creating ', outputTextFile 
	print >> open(outputTextFile, 'w+'), allROCs
	outputFile.Write()
	outputFile.Close()

def makeROCs( textFile, variables, bkgSamples, perVariable, cutsList, printValue, printVar, returnSOB='' ):
	"""docstring for makeROCs"""

	f = open( textFile, 'r' )
	tmpDictVar = eval( f.read() )

	dictVar = OrderedDict()
	for q in tmpDictVar:
		for tmpVar in variables:
			if tmpVar[0] in q: 
				dictVar[ q ] = tmpDictVar[ q ]

	dictROC = OrderedDict()
	dictNumEvents = {}
	for varROC in dictVar:
		BkgROCArray = np.asarray( dictVar[ varROC ][0] )
		SigROCArray = np.asarray( dictVar[ varROC ][1] )
		SigROCBinsArray = np.asarray( dictVar[ varROC ][2] )
		SigROCLowEdgeArray = np.asarray( dictVar[ varROC ][3] )
		BkgNumArray = np.asarray( dictVar[ varROC ][4] )
		SigNumArray = np.asarray( dictVar[ varROC ][5] )
		BkgErrArray = np.asarray( dictVar[ varROC ][6] )
		SigErrArray = np.asarray( dictVar[ varROC ][7] )
		ROC = TGraph( len( BkgROCArray ), SigROCArray, BkgROCArray )		
		dictROC[ varROC ] = ROC
		dictNumEvents[ varROC ] = [ BkgNumArray, SigNumArray, SigROCLowEdgeArray, BkgErrArray, SigErrArray ]
		if (printValue and ( printVar in varROC )):
			'''
			if var[0] in varROC:
				x = find_nearest(SigROCLowEdgeArray, var[6] )
				print 'For cut', var[6], 'in', var[0], 'effSig: ', SigROCArray[x], ', effBkg: ', BkgROCArray[x]
			'''
			for Cut in cutsList:
				if printVar in Cut[0]:
					y = find_nearest( SigROCArray, Cut[6] )
					print 'Optimal value for ', varROC, SigROCLowEdgeArray[y], 'is', SigROCArray[y], 'bkgRej = ', BkgROCArray[y]

	if not printValue:
		if perVariable:
			dictNumVar = OrderedDict()
			for var in variables:
				dictVariables = { rocs: dictROC[ rocs ] for rocs in dictROC if var[0] in rocs }
				#plotROC( var[0], var[0], dictVariables, len(cutsList), True, False )
				dictVariablesNum = { rocs: dictNumEvents[ rocs ] for rocs in dictNumEvents if var[0] in rocs }

				totalSig = dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][1]*args.lumi
				#totalSigErr = np.sqrt( np.multiply( totalSig, dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][4] ) ) 
				totalSigErr = np.power( dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][4], 2 ) * args.lumi ### it is power because I sqrt the error

				totalBkg = np.zeros( len( dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][1] ) )
				totalBkgErr = np.zeros( len( dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][1] ) )
				for bkg in dictVariablesNum: 
					totalBkg += dictVariablesNum[ bkg ][0]*args.lumi
					totalBkgErr += np.power( dictVariablesNum[ bkg ][3], 4 )   ### it is power because I sqrt the error
				totalBkgErr = np.sqrt( totalBkgErr )*args.lumi

				sqrtSigBkg = np.sqrt( np.add(totalSig, totalBkg ) )
				sigOverSqrtSigBkg = np.divide( totalSig, sqrtSigBkg )

				sigBkgErr = np.sqrt( np.add( np.power( totalSigErr, 2 ), np.power( totalBkgErr, 2 ) ) )
				sqrtSigBkgErr = np.divide( sigBkgErr, 2*sqrtSigBkg )
				totalErrSigOverSqrtSigBkg = np.sqrt( np.add( np.power( np.divide( totalSigErr, totalSig ), 2), np.power( np.divide( sqrtSigBkgErr, sqrtSigBkg ), 2) ) )
				#print args.mass, sigOverSqrtSigBkg
				#print totalErrSigOverSqrtSigBkg
				sigOverSqrtSigBkg = np.divide( totalSig, np.sqrt(totalBkg) ) 
				#sigOverSqrtSigBkg = np.sqrt( 2*( (totalSig+totalBkg)*np.log( 1 + np.divide( totalSig, totalBkg ) ) - totalSig ) )
				#SOB = TGraphErrors( len(totalSig), ( (dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][2])/5. if 'deltaEta' in var[0] else (dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][2]) ), sigOverSqrtSigBkg, array( 'd', [0]*len(sigOverSqrtSigBkg)), totalErrSigOverSqrtSigBkg ) 
				SOB = TGraph( len(totalSig), ( (dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][2])/5. if 'deltaEta' in var[0] else (dictVariablesNum[ var[0]+'_QCD'+qcd+'All_ROC' ][2]) ), sigOverSqrtSigBkg ) 
				dictNumVar[ var[0] ] = SOB 
				#if returnSOB in var[0]: return SOB
				#else: continue

			print 'test'
			plotROC( 'SOB', '', dictNumVar, len(cutsList), False, True )
		else: 
			for bkg in bkgSamples: 
				dictBkg = { rocs: dictROC[ rocs ] for rocs in dictROC if bkg in rocs }
				plotROC( bkg, bkg, dictBkg, len(cutsList), False, False )

def plotROC( name, sample, dictROC, numCuts, varOrbkg, SOB, diffMasses=False ):
	"""docstring for plotROC"""

	dictSOB = OrderedDict()
	dictSOBError = OrderedDict()
	dictSOBLowEdge = OrderedDict()

	if diffMasses:
		dictROC = OrderedDict()
		tmpName = name.replace( 'SOB_', '' )

		for masses in [80, 90, 100, 110, 120, 130, 140, 150, 170, 180, 190, 210, 220, 230, 240, 300 ]: 
		 	SOB = makeROCs( 'ROCfiles/ROC'+version+'Values_QCD'+qcd+'_RPVSt'+str(masses)+'_cut2_v1.txt', [ [tmpName] ], '', True, '', False, '', returnSOB=tmpName)
			dictROC[ 'M_{#tilde{t}} = '+str(masses)+' GeV' ] = SOB
	
	f1 = TF1("f1","x",0,1)
	f1.SetLineColor(1)
	f1.SetLineStyle(3)
	can = TCanvas('c1', 'c1',  10, 10, 1000, 750 )
	can.SetGrid()
	#can.SetLogy()
	
	PT = TText(0.6, 0.05, sample )
	multiGraph = TMultiGraph()
	legend=TLegend(0.65,0.15,0.90,0.45)
	#legend=TLegend(0.80,0.50,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)
	dummy=1
	for h in dictROC:
		#tmpName = h.replace( name+'_', '' ).replace( '_ROC', '' )
		tmpName = str(h)
		legend.AddEntry( dictROC[ h ], tmpName, 'l' )
		#for var in variables:
		#	if var[0] in tmpName: varColor = var[7]
		#dictROC[h].SetLineColor( bkgSamples[ tmpName ][1] if varOrbkg else varColor )
		dictROC[h].SetLineColor( dummy ) 
		dictROC[h].SetLineWidth( 2 )
		dictROC[h].SetMarkerStyle(4)
		multiGraph.Add( dictROC[h] )
		dummy += 1
		if dummy == 5: dummy = 6
		if dummy == 9: dummy = 40
	multiGraph.Draw("ALP")
	PT.Draw()
	if SOB:
		if diffMasses: multiGraph.GetXaxis().SetTitle( 'Leading jet #tau_{21}' )
		else: multiGraph.GetXaxis().SetTitle( 'A.U.' )
		#multiGraph.GetYaxis().SetTitle('S/#sqrt{S+B}')
		multiGraph.GetYaxis().SetTitle('S/#sqrt{B}')
		#multiGraph.GetYaxis().SetTitle('#sqrt{2*((s+b)ln(s/b)-s)}')
	else:
		multiGraph.GetXaxis().SetRangeUser(-0.05,1.05)
		multiGraph.GetYaxis().SetRangeUser(-0.05,1.05)
		multiGraph.GetXaxis().SetTitle('Signal efficiency')
		multiGraph.GetYaxis().SetTitle('Bkg rejection')
		f1.Draw("same")
	multiGraph.GetYaxis().SetTitleOffset(0.95)
	legend.Draw()
	if diffMasses: can.SaveAs('Plots/'+name+'_'+version+'_QCD'+qcd+'_ROC_cut'+str(numCuts)+'.'+args.ext)
	else: can.SaveAs('Plots/'+name+'_'+version+signalName+'_QCD'+qcd+'_ROC_cut'+str(numCuts)+'.'+args.ext)
	del can

def plotSigOverBkg( name, sample, dictNum, numCuts ):
	"""docstring for plotROC"""

	can = TCanvas('c1', 'c1',  10, 10, 1000, 750 )
	can.SetGrid()

	PT = TText(0.7, 1.10, sample )
	#legend=TLegend(0.15,0.15,0.45,0.45)
	#legend.SetFillStyle(0)
	#legend.SetTextSize(0.03)
	SOB.SetLineWidth( 2 )
	SOB.SetMarkerStyle(4)
	SOB.Draw("ALP")
	PT.Draw()
	SOB.GetYaxis().SetTitleOffset(0.95)
	#legend.Draw()
	can.SaveAs('Plots/'+name+'_'+version+signalName+'_QCD'+qcd+'_SOB_cut'+str(numCuts)+'.'+args.ext)
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
	factory = TMVA.Factory( "TMVATraining"+version+bkgName+"_RPVSt"+mass, outputFile, "!V:!Silent:Transformations=I;D;P;G,D:AnalysisType=Classification")

	# define input var
	factory.AddTarget( 'massAve', 'F' )
	for k in variables: factory.AddVariable( k, "F" )

	#factory.SetWeightExpression( "weight" if ( 'Mini' in inputFiles ) else 'puWeight*lumiWeight' )
	factory.SetWeightExpression( 'puWeight*lumiWeight' )

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

	sigFile, sigTree, sigNumEntries = getTree( SigSample, treename )
	for k in variables: sigTree.SetBranchAddress( k, dictVariables[ k ] )
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
		bkgFile, bkgTree, bkgNumEntries  = getTree( bkgSamples[ sample ], treename )
		for k in variables: bkgTree.SetBranchAddress( k, dictVariables[ k ] )
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
	parser.add_argument( '-t', '--typeROC', action='store',  dest='typeROC', default='var', help='Type of ROC: variables only (var) or bkgs only (bkg)')
	parser.add_argument( '-P', '--printValue', action='store',  dest='printValue', type=bool, default=False, help='Print values of ROCs')
	parser.add_argument( '-q', '--quantity', action='store',  dest='quantity', default='massAsym', help='Variable to print ROC.')
	parser.add_argument( '-s', '--selection', action='store',  dest='selection', default='', help='Selection, like _cutDEta' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='Simple', help='Process: simple or TMVA' )
	parser.add_argument( '-v', '--version', action='store',  dest='version', default='Boosted', help='Variable to optimize, as histogram in rootfile.' )
	parser.add_argument( '-e', '--eff', action='store', dest='effS', type=int, default=0, help='Mass of the Stop' )
	parser.add_argument( '-l', '--lumi', action='store', dest='lumi', type=int, default=2666, help='Mass of the Stop' )
	parser.add_argument('-Q', '--QCD', action='store', default='Pt', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-E', '--extension', action='store', dest='ext', default='png', help='Extension of plots.' )
	parser.add_argument( '-b', '--batchSys', action='store',  dest='batchSys', type=bool, default=False, help='Process: all or single.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	selection = args.selection
	process = args.process
	version = args.version
	typeROC = args.typeROC
	quantity = args.quantity
	printValue = args.printValue
	effS = args.effS
	qcd = args.QCD

	if args.batchSys: folder = '/cms/gomez/archiveEOS/Archive/763patch2/v5/'
	else: folder = 'Rootfiles/'

	bkgSamples = OrderedDict()
	bkgSamples[ 'QCD'+qcd+'All' ] = [ folder+'/RUNAnalysis_QCD'+qcd+'All_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kBlue-4 ]
	bkgSamples[ 'TTJets' ] = [ folder+'/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kGreen ]
	bkgSamples[ 'WJetsToQQ' ] = [ folder+'/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kMagenta ]
	bkgSamples[ 'ZJetsToQQ' ] = [ folder+'/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kOrange ]
	bkgSamples[ 'WWTo4Q' ] = [ folder+'/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kMagenta+2 ]
	bkgSamples[ 'ZZTo4Q' ] = [ folder+'/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kOrange+2 ]
	bkgSamples[ 'WZ' ] = [ folder+'/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kCyan ]

	sigSamples = {}
	sigSamples[ 'RPVSt'+str(mass) ] = folder+'/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v2p0_v05.root'
	#sigSamples[ 'WWTo4Q' ] = folder+'/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'ZZTo4Q' ] = folder+'/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'WZ' ] = folder+'/RUNAnalysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'TTJets' ] = folder+'/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'WJetsToQQ' ] = folder+'/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'ZJetsToQQ' ] = folder+'/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'

	SigSample = folder+'/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	treename = "ResolvedAnalysisPlots/RUNATree" if ( 'Resolved' in version ) else 'BoostedAnalysisPlots/RUNATree'

	var = [
		## Version, Variable, nBins, minX, maxX, Below value, cut, Check ROC value
		#[ 'Resolved', 'mindR', 50, 0., 5., True, 0., 0.8 ],
		[ 'Resolved', 'deltaEta', 50, 0., 5., True, 0., 0.65 ],
		[ 'Resolved', 'massAsym', 20, 0., 1., True, 0., 0.64 ],
		[ 'Resolved', 'cosThetaStar1', 20, 0., 1., True, 0., 0.70 ],
		[ 'Resolved', 'cosThetaStar2', 20, 0., 1., True, 0., 0.70 ],
		[ 'Resolved', 'delta1', 30, -500, 1000,  False, 0, 0.6 ],
		[ 'Resolved', 'delta2', 30, -500, 1000, False, 0, 0.6 ],
		#[ 'Resolved', 'xi1', 20, 0., 1., True, 0, 0.6 ],
		#[ 'Resolved', 'xi2', 20, 0., 1., True , 0, 0.6],
		##### RPV St 100
#		[ 'Boosted', "prunedMassAsym", 20, 0., 1., True, 0.2, 0.9 ],
#		[ 'Boosted', "jet1CosThetaStar", 20, 0., 1, True, 0., 0.8 ],
#		[ 'Boosted', "jet2CosThetaStar", 20, 0., 1, True, 0., 0.8 ],
#		[ 'Boosted', "jet1Tau21", 20, 0., 1., True, 0.5, 0.8  ],
#		[ 'Boosted', "jet2Tau21", 20, 0., 1., True, 0.5, 0.80 ],
#		[ 'Boosted', "jet1Tau31", 20, 0., 1., True, 0.3, 0.7 ],
#		[ 'Boosted', "jet2Tau31", 20, 0., 1., True, 0.3, 0.7 ],
#		[ 'Boosted', "jet1Tau32", 20, 0., 1., True, 0., 0  ],
#		[ 'Boosted', "jet2Tau32", 20, 0., 1., True, 0., 0  ],
#		[ 'Boosted', "deltaEtaDijet", 50, 0., 5., True, 0.4, 0.6 ],
#		[ 'Boosted', "jet1SubjetPtRatio", 20, 0., 1., True, 0., 0  ],
#		[ 'Boosted', "jet2SubjetPtRatio", 20, 0., 1., True, 0., 0  ],
		[ 'Boosted', "prunedMassAsym", 20, 0., 1., True, 0., 0.2, 1 ],
		[ 'Boosted', "jet1CosThetaStar", 20, 0., 1, True, 0., 0.8, 2 ],
#		[ 'Boosted', "jet2CosThetaStar", 20, 0., 1, True, 0., 0.8, 3 ],
		[ 'Boosted', "jet1Tau21", 20, 0., 1., True, 0., 0. , 4 ],
		[ 'Boosted', "jet2Tau21", 20, 0., 1., True, 0., 0., 5 ],
		[ 'Boosted', "jet1Tau31", 20, 0., 1., True, 0., 0., 6 ],
		[ 'Boosted', "jet2Tau31", 20, 0., 1., True, 0., 0., 7 ],
		[ 'Boosted', "jet1Tau32", 20, 0., 1., True, 0., 0 , 8 ],
		[ 'Boosted', "jet2Tau32", 20, 0., 1., True, 0., 0 , 9 ],
		[ 'Boosted', "deltaEtaDijet", 50, 0., 5., True, 0., 0.6, 11 ],
		[ 'Boosted', "jet1SubjetPtRatio", 20, 0., 1., True, 0., 0 , 12 ],
		[ 'Boosted', "jet2SubjetPtRatio", 20, 0., 1., True, 0., 0 , 13 ],
	]

	if 'calcROC' in process: 
		variables = [ x[1:] for x in var if ( version in x[0] ) ]
		cuts = [ x[1:] for x in var if ( ( version in x[0] ) and ( x[6]!=x[3] ) ) ]
		p0 = Process( target=calcROCs, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts ) )
		p0.start()
		p0.join()
	
	elif 'plotROC' in process: 
		variables = [ x[1:] for x in var if ( ( version in x[0] ) and ( x[6]==x[3] ) ) ]
		cuts = [ x[1:] for x in var if ( ( version in x[0] ) and ( x[6]!=x[3] ) ) ]
		for q in sigSamples: signalName = ( q )
		if printValue: 	makeROCs( 'ROCfiles/ROC'+version+'Values_QCD'+qcd+'_'+signalName+'_cut'+str(len(cuts)-1)+'.txt', cuts, bkgSamples, True if 'var' in typeROC else False, cuts, printValue, quantity )
		else: makeROCs( 'ROCfiles/ROC'+version+'Values_QCD'+qcd+'_'+signalName+'_cut'+str(len(cuts))+'_v1.txt', variables, bkgSamples, True if 'var' in typeROC else False, cuts, printValue, quantity )

	elif 'tmp' in process: 	
		plotROC( 'SOB_jet1Tau21', '', '', '', True, True, diffMasses=True )

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
				

