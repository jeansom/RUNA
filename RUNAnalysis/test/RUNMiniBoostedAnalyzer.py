#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time
import argparse
from collections import OrderedDict
from multiprocessing import Process
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2F, TMath
from array import array
try: 
	from RUNA.RUNAnalysis.commonFunctions import *
	from RUNA.RUNAnalysis.cuts import selection
	from RUNA.RUNAnalysis.scaleFactors import scaleFactor
except ImportError: 
	sys.path.append('../python') 
	from commonFunctions import *
	from cuts import selection
	from scaleFactors import scaleFactor

gROOT.SetBatch()
######################################
def myAnalyzer( dictSamples, listCuts, signalName, RANGE ):

	if (( len(dictSamples) == 1 ) and ( signalName not in ['RPVStopStopToJets_'+args.decay+'_M-'+str(mass)] )): outputFileName = 'Rootfiles/RUNMiniBoostedAnalysis_'+grooming+'_'+signalName+'_'+RANGE+'_v2.root' 
	else: outputFileName = 'Rootfiles/RUNMiniBoostedAnalysis_'+grooming+'_'+signalName+'_v2.root' 
	outputFile = TFile( outputFileName, 'RECREATE' )

	###################################### output Tree
	#tree = TTree('RUNAFinTree'+grooming, 'RUNAFinTree'+grooming)
	#AvgMass = array( 'f', [ 0. ] )
	#tree.Branch( 'AvgMass', AvgMass, 'AvgMass/F' )
	#Scale = array( 'f', [ 0. ] )
	#tree.Branch( 'Scale', Scale, 'Scale/F' )


	################################################################################################## Histos
	massBins = 500
	massXmin = 0.
	massXmax = 500.
	listOfOptions = [ [ j,k] for j in range(len(listCuts)-1) for k in range(1, len(listCuts) ) if k > j ]

	for sam in dictSamples:
		allHistos[ "cutFlow_"+sam ] = TH1F( "cutflow_"+sam, "cutflow_"+sam, len(listCuts), 0., len(listCuts) )
		allHistos[ "HT_"+sam ] = TH1F( "HT_"+sam, "HT_"+sam, 5000, 0., 5000 )
		allHistos[ "HT_"+sam ].Sumw2()
		allHistos[ "MET_"+sam ] = TH1F( "MET_"+sam, "MET_"+sam, 500, 0., 500 )
		allHistos[ "MET_"+sam ].Sumw2()
		allHistos[ "massAve_"+sam ] = TH1F( "massAve_"+sam, "massAve_"+sam, 500, 0., 500 )
		allHistos[ "massAve_"+sam ].Sumw2()
		allHistos[ "numJets_"+sam ] = TH1F( "numJets_"+sam, "numJets_"+sam, 20, 0., 20 )
		allHistos[ "numJets_"+sam ].Sumw2()
		allHistos[ "jet1Pt_"+sam ] = TH1F( "jet1Pt_"+sam, "jet1Pt_"+sam, 2000, 0., 2000 )
		allHistos[ "jet1Pt_"+sam ].Sumw2()
		allHistos[ "jet2Pt_"+sam ] = TH1F( "jet2Pt_"+sam, "jet2Pt_"+sam, 2000, 0., 2000 )
		allHistos[ "jet2Pt_"+sam ].Sumw2()
		allHistos[ "jet1CosThetaStar_"+sam ] = TH1F( "jet1CosThetaStar_"+sam, "jet1CosThetaStar_"+sam, 20, 0., 1 )
		allHistos[ "jet1CosThetaStar_"+sam ].Sumw2()
		allHistos[ "jet2CosThetaStar_"+sam ] = TH1F( "jet2CosThetaStar_"+sam, "jet2CosThetaStar_"+sam, 20, 0., 1 )
		allHistos[ "jet2CosThetaStar_"+sam ].Sumw2()

		for var in listCuts:
			if 'deltaEta' in var[0]: allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 50, 0., 5. )
			else: allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 20, 0., 1. )
			allHistos[ var[0]+'_'+sam ].Sumw2()
			allHistos[ "massAve_"+var[0]+'_'+sam ] = TH1F( "massAve_"+var[0]+'_'+sam, "massAve_"+var[0]+'_'+sam, massBins, massXmin, massXmax )
			allHistos[ "massAve_"+var[0]+'_'+sam ].Sumw2()

		for ind in listOfOptions:
			tmpName = listCuts[ind[0]][0]+'Vs'+listCuts[ind[1]][0]+'_'+sam
			allHistos[ tmpName ] = TH2F( tmpName, tmpName, 
					(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
					(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
					)
			allHistos[ tmpName ].Sumw2()

	################################################################################################## Running the Analysis
	for sample in dictSamples:

		####### Get GenTree 
		inputFile, events, numEntries = getTree( dictSamples[ sample ], ('BoostedAnalysisPlotsPuppi/RUNATree' if 'Puppi' in args.grooming else 'BoostedAnalysisPlots/RUNATree' ) )
		print '-'*40
		print '------> ', sample
		print '------> Number of events: '+str(numEntries)
		d = 0
		cutFlowList = OrderedDict()
		cutFlowList[ 'Process' ] = 0
		cutFlowList[ 'Preselection' ] = 0
		for k in listCuts: cutFlowList[ k[0] ] = 0

		SF = scaleFactor( sample )
		for i in xrange(numEntries):
			events.GetEntry(i)
			cutFlowList[ 'Process' ] += 1

			#---- progress of the reading --------
			fraction = 10.*i/(1.*numEntries)
			if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
			d = TMath.FloorNint(fraction)
			#if ( i > 100000 ): break

			Run      = events.run
			Lumi     = events.lumi
			NumEvent = events.event
			puWeight	= events.puWeight
			lumiWeight	= events.lumiWeight
			HT		= events.HT
			MET		= events.MET
			numJets		= events.numJets
			massAve		= getattr( events, (args.grooming+"MassAve").replace('Puppi','') )
			jet1Pt          = events.jet1Pt
			jet2Pt          = events.jet2Pt
			jet1Eta          = events.jet1Eta
			jet2Eta          = events.jet2Eta
			jet1CosThetaStar	= events.jet1CosThetaStar
			jet2CosThetaStar	= events.jet2CosThetaStar
			#print 'Entry ', Run, ':', Lumi, ':', NumEvent

			if 'DATA' in sample: scale = 1
			#elif 'RPV' in sample: scale = 2606 * puWeight * SF
			else: scale = 2606 * puWeight * lumiWeight

			#### test
			#if ( jet1Mass > 400 ) or ( jet2Mass > 400 ): print 'Entry ', Run, ':', Lumi, ':', NumEvent
			#if ( Lumi != tmpLumi ):
			#	newLumi += Lumi
			#	tmpLumi == Lumi
			#print Run/float(Lumi), Run, Lumi, Run/float(newLumi)
			
			
			#### Pre-selection
			HTCut = ( HT > 900 )
			dijetCut =  ( numJets > 1 )
			jetPtCut =  ( jet1Pt > 500 ) and ( jet2Pt > 450 )
			
			if HTCut and dijetCut and jetPtCut:
				cutFlowList[ 'Preselection' ] += 1
				sigCutsList = []
				allHistos[ "HT_"+sam ].Fill( HT, scale)
				allHistos[ "MET_"+sam ].Fill( MET, scale)
				allHistos[ "massAve_"+sam ].Fill( massAve, scale)
				allHistos[ "numJets_"+sam ].Fill( numJets, scale)
				allHistos[ "jet1Pt_"+sam ].Fill( jet1Pt, scale)
				allHistos[ "jet2Pt_"+sam ].Fill( jet2Pt, scale)
				allHistos[ "jet1CosThetaStar_"+sam ].Fill( jet1CosThetaStar, scale)
				allHistos[ "jet2CosThetaStar_"+sam ].Fill( jet2CosThetaStar, scale)
				for var in listCuts:
					allHistos[ var[0]+'_'+sample ].Fill( getattr( events, var[0] ), scale )
					nextCut = False
					if ( getattr( events, var[0] ) < var[1] ): nextCut = True 
					else: nextCut = False
					sigCutsList.append( nextCut )
					if all(sigCutsList): 
						allHistos[ 'massAve_'+var[0]+'_'+sample ].Fill( massAve, scale )
						cutFlowList[ var[0] ] += 1

				for Ind in listOfOptions:
					allHistos[ listCuts[Ind[0]][0]+'Vs'+listCuts[Ind[1]][0]+'_'+sample ].Fill( getattr( events, listCuts[Ind[0]][0] ), getattr( events, listCuts[Ind[1]][0] ), scale )
					tmpSigCutsList = [ x for i,x in enumerate(sigCutsList) if i not in Ind ]
						

				##### TEST

				##########################################

		dummy = 1
		for q in cutFlowList: 
			allHistos[ 'cutFlow_'+sample ].SetBinContent( dummy, cutFlowList[q] )
			allHistos[ 'cutFlow_'+sample ].GetXaxis().SetBinLabel( dummy, q )
			dummy+=1

	outputFile.Write()
	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Close()




#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store',  dest='grooming', default='pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='single', help='Process: all or single.' )
	parser.add_argument( '-d', '--decay', action='store',  dest='decay', default='UDD312', help='Decay: UDD312 or UDD323.' )
	parser.add_argument( '-s', '--sample', action='store',   dest='samples', default='RPV', help='Type of sample' )
	parser.add_argument( '-r', '--range', action='store',  dest='RANGE', default='low', help='Range: low, med, high.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	process = args.process
	grooming = args.grooming
	samples = args.samples

	if 'RPV' in samples: samples = 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass)
	allSamples = {}
	allSamples[ 'DATA' ] = 'Rootfiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v1p0_v02.root'
	#if not 'Dibosons' in mass: allSamples[ 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass) ] = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v1p0_v01.root'
	allSamples[ 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass) ] = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
	allSamples[ 'QCDHTAll' ] = 'Rootfiles/RUNAnalysis_QCDHTAll_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
	allSamples[ 'TTJets' ] = 'Rootfiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
	allSamples[ 'WJetsToQQ' ] = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
	#allSamples[ 'ZJetsToQQ' ] = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WWTo4Q' ] = 'Rootfiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
	#allSamples[ 'ZZTo4Q' ] = 'Rootfiles/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WZ' ] = 'Rootfiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'

	cutList = ( 'Dibosons' if 'Dibosons' in mass else 'RPVStopStopToJets_'+args.decay+'_M-'+mass )
	try: cuts = selection[ cutList ]
	except KeyError: 
		print 'Mass', mass, 'not in list.'
		sys.exit(0)
		
	if 'single' in process: 
		for q in allSamples:
			if q in samples:
				dictSamples = { q: allSamples[ q ] } 
				signalSample = q
	else: 
		dictSamples = allSamples
		signalSample = 'RPVStopStopToJets_'+args.decay+'_M-'+mass+'_All'
	allHistos = {}

	p = Process( target=myAnalyzer, args=( dictSamples, cuts, signalSample, args.RANGE ) )
	p.start()
	p.join()
