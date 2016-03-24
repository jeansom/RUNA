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
except ImportError: 
	sys.path.append('../python') 
	from commonFunctions import *
	from cuts import selection

gROOT.SetBatch()
######################################
def myAnalyzer( dictSamples, listCuts, signalName ):


	outputFileName = 'Rootfiles/RUNMiniBoostedAnalysis_'+signalName+'_allHistos_v7.root' 
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
		allHistos[ "massAve_"+sam ] = TH1F( "massAve_"+sam, "massAve_"+sam, massBins, massXmin, massXmax )
		allHistos[ "massAve_"+sam ].Sumw2()
		allHistos[ "cutFlow_"+sam ] = TH1F( "cutflow_"+sam, "cutflow_"+sam, len(listCuts), 0., len(listCuts) )

		for var in listCuts:
			if 'deltaEta' in var[0]: allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 50, 0., 5. )
			else: allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 20, 0., 1. )
			allHistos[ var[0]+'_'+sam ].Sumw2()

		for ind in listOfOptions:
			tmpName = listCuts[ind[0]][0]+'Vs'+listCuts[ind[1]][0]+'_'+sam
			allHistos[ tmpName ] = TH2F( tmpName, tmpName, 
					(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
					(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
					)
			allHistos[ tmpName ].Sumw2()
			allHistos[ "massAve_"+tmpName+'_BD' ] = TH1F( "massAve_"+tmpName+'_BD', "massAve_"+tmpName+'_BD', massBins, massXmin, massXmax )
			allHistos[ "massAve_"+tmpName+'_BD' ].Sumw2()
			allHistos[ "massAve_"+tmpName+'_BCD' ] = TH1F( "massAve_"+tmpName+'_BCD', "massAve_"+tmpName+'_BCD', massBins, massXmin, massXmax )
			allHistos[ "massAve_"+tmpName+'_BCD' ].Sumw2()
			allHistos[ tmpName+'_Bkg' ] = TH2F( tmpName+'_Bkg', tmpName+'_Bkg', 
					(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
					(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
					)
			allHistos[ tmpName+'_Bkg' ].Sumw2()

			for k in [ 'A', 'B', 'C', 'D' ]:
				allHistos[ "massAve_"+tmpName+'_'+k ] = TH1F( "massAve_"+tmpName+'_'+k, "massAve_"+tmpName+'_'+k, massBins, massXmin, massXmax )
				allHistos[ "massAve_"+tmpName+'_'+k ].Sumw2()
				allHistos[ tmpName+'_'+k ] = TH2F( tmpName+'_'+k, tmpName+'_'+k, 
						(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
						(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
						)
				allHistos[ tmpName+'_'+k ].Sumw2()
	################################################################################################## Running the Analysis
	for sample in dictSamples:

		####### Get GenTree 
		inputFile, events, numEntries = getTree( dictSamples[ sample ], 'RUNATree'+grooming+'/RUNATree' )
		print '-'*40
		print '------> ', sample
		print '------> Number of events: '+str(numEntries)
		d = 0
		cutFlowList = OrderedDict()
		cutFlowList[ 'Process' ] = 0
		cutFlowList[ 'Preselection' ] = 0
		for k in listCuts: cutFlowList[ k[0] ] = 0

		#newLumi = 0
		#tmpLumi = 0

		for i in xrange(numEntries):
			events.GetEntry(i)
			cutFlowList[ 'Process' ] += 1

			#---- progress of the reading --------
			fraction = 10.*i/(1.*numEntries)
			if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
			d = TMath.FloorNint(fraction)
			#if ( i > 500000 ): break

			Run      = events.run
			Lumi     = events.lumi
			NumEvent = events.event
			puWeight	= events.puWeight
			lumiWeight	= events.lumiWeight
			HT		= events.HT
			numJets		= events.numJets
			massAve		= events.massAve
			jet1Pt          = events.jet1Pt
			jet2Pt          = events.jet2Pt
			#print 'Entry ', Run, ':', Lumi, ':', NumEvent

			if 'DATA' in sample: scale = 1
			else: scale = 2476* puWeight * lumiWeight

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
				for var in listCuts:
					allHistos[ var[0]+'_'+sample ].Fill( getattr( events, var[0] ), scale )
					if ( getattr( events, var[0] ) < var[1] ): sigCutsList.append( True )
					else: sigCutsList.append( False )
				if all(sigCutsList): allHistos[ 'massAve_'+sample ].Fill( massAve, scale )

				for Ind in listOfOptions:
					allHistos[ listCuts[Ind[0]][0]+'Vs'+listCuts[Ind[1]][0]+'_'+sample ].Fill( getattr( events, listCuts[Ind[0]][0] ), getattr( events, listCuts[Ind[1]][0] ), scale )
					tmpSigCutsList = [ x for i,x in enumerate(sigCutsList) if i not in Ind ]
					if all(tmpSigCutsList): 
						allHistos[ listCuts[Ind[0]][0]+'Vs'+listCuts[Ind[1]][0]+'_'+sample+'_Bkg' ].Fill( getattr( events, listCuts[Ind[0]][0] ), getattr( events, listCuts[Ind[1]][0] ), scale )
						plotABCD( [ sigCutsList[Ind[0]], sigCutsList[Ind[1]] ], [ listCuts[Ind[0]], listCuts[Ind[1]] ], events, massAve, scale, sample )
						
		for IND in listOfOptions:
			tmpNameABCD = listCuts[IND[0]][0]+'Vs'+listCuts[IND[1]][0]+'_'+sample
			allHistos[ 'massAve_'+tmpNameABCD+'_BD' ].Multiply( allHistos[ 'massAve_'+tmpNameABCD+'_D' ] )
			allHistos[ 'massAve_'+tmpNameABCD+'_BCD' ].Divide( allHistos[ 'massAve_'+tmpNameABCD+'_BD' ], allHistos[ 'massAve_'+tmpNameABCD+'_C' ], 1., 1., 'B' )

		'''
		dummy = 1
		for q in cutFlowList: 
			allHistos[ 'cutFlow_'+sample ].SetBinContent( dummy, cutFlowList[q] )
			allHistos[ 'cutFlow_'+sample ].GetXaxis().SetBinLabel( dummy, q )
			dummy+=1
			
		tmpHT_cutDEtaMassAsym.Divide( tmpHT_cutNOTau21 )
		for k in range( len( variablesBkg ) ):
			try: 
				binNewWeight = tmpHT_cutDEtaMassAsym.GetXaxis().FindBin( variablesBkg[k][0] )
				newScale = tmpHT_cutDEtaMassAsym.GetBinContent( binNewWeight ) 
			except IndexError: newScale = 0
			if (newScale <= 1):
				HT_cutNOTau21_ReScale.Fill( variablesBkg[k][0], newScale )
				massAve_cutNOTau21_ReScale.Fill( variablesBkg[k][1], newScale )
		'''
	outputFile.Write()
	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Close()


def plotABCD( listSel, var, fromTree, massAve, scale, sample ):
	"""docstring for plotABCD"""

	nameABCD = var[0][0]+'Vs'+var[1][0]+'_'+sample
	if listSel[0] and listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_A' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_A' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
	elif listSel[0] and not listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_B' ].Fill( massAve, scale )
		allHistos[ 'massAve_'+nameABCD+'_BD' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_B' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
	elif not listSel[0] and listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_D' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_D' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
	else:
		allHistos[ 'massAve_'+nameABCD+'_C' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_C' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )


#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store',  dest='grooming', default='Pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='single', help='Process: all or single.' )
	parser.add_argument( '-d', '--debug', action='store_true', dest='couts', default=False, help='True print couts in screen, False print in a file' )
	parser.add_argument( '-s', '--sample', action='store',   dest='samples', default='RPV', help='Type of sample' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	process = args.process
	couts = args.couts
	grooming = args.grooming
	samples = args.samples

	allSamples = {}
	allSamples[ 'DATA' ] = 'Rootfiles/RUNAnalysis_JetHTRun2015D-All_v09_v03.root'
	if not 'Dibosons' in mass: allSamples[ 'RPVSt'+str(mass) ] = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'QCDPtAll' ] = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'TTJets' ] = 'Rootfiles/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WJetsToQQ' ] = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'ZJetsToQQ' ] = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WWTo4Q' ] = 'Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'ZZTo4Q' ] = 'Rootfiles/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WZ' ] = 'Rootfiles/RUNAnalysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'

	signalSample = ( 'Dibosons' if 'Dibosons' in mass else 'RPVSt'+mass )
	try: cuts = selection[ signalSample ]
	except KeyError: 
		print 'Mass', mass, 'not in list.'
		sys.exit(0)
		
	if 'single' in process: dictSamples = { q: allSamples[ q ] for q in allSamples if q in samples }
	else: dictSamples = allSamples
	allHistos = {}

	p = Process( target=myAnalyzer, args=( dictSamples, cuts, signalSample ) )
	p.start()
	p.join()
