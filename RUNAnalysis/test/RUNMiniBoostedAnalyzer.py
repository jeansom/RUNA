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
except ImportError: 
	sys.path.append('../python') 
	from commonFunctions import *

gROOT.SetBatch()

######################################
def myAnalyzer( dictSamples, listCuts, signalName ):


	outputFileName = 'Rootfiles/RUNMiniBoostedAnalysis_'+signalName+'_allHistos.root' 
	outputFile = TFile( outputFileName, 'RECREATE' )

	###################################### output Tree
	#tree = TTree('RUNAFinTree'+grooming, 'RUNAFinTree'+grooming)
	#AvgMass = array( 'f', [ 0. ] )
	#tree.Branch( 'AvgMass', AvgMass, 'AvgMass/F' )
	#Scale = array( 'f', [ 0. ] )
	#tree.Branch( 'Scale', Scale, 'Scale/F' )


	################################################################################################## Histos
	for sam in dictSamples:
		allHistos[ "massAve_"+sam ] = TH1F( "massAve_"+sam, "massAve_"+sam, 100, 0., 500. )
		allHistos[ "massAve_"+sam+'_A' ] = TH1F( "massAve_"+sam+'_A', "massAve_"+sam+'_A', 100, 0., 500. )
		allHistos[ "massAve_"+sam+'_B' ] = TH1F( "massAve_"+sam+'_B', "massAve_"+sam+'_B', 100, 0., 500. )
		allHistos[ "massAve_"+sam+'_Bkg' ] = TH1F( "massAve_"+sam+'_Bkg', "massAve_"+sam+'_Bkg', 100, 0., 500. )
		allHistos[ "massAve_"+sam+'_C' ] = TH1F( "massAve_"+sam+'_C', "massAve_"+sam+'_C', 100, 0., 500. )
		allHistos[ "massAve_"+sam+'_D' ] = TH1F( "massAve_"+sam+'_D', "massAve_"+sam+'_D', 100, 0., 500. )
		allHistos[ "cutFlow_"+sam ] = TH1F( "cutflow_"+sam, "cutflow_"+sam, len(listCuts), 0., len(listCuts) )

		for tmpVar in listCuts:
			for var in tmpVar:
				if 'deltaEta' in var[0]: allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 50, 0., 5. )
				else: allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 20, 0., 1. )
		for k in [ 'A', 'B', 'C', 'D' ]:
			if len(listCuts[0]) == 2: tmpName = listCuts[0][0][0]+'Vs'+listCuts[0][1][0]+'_'+sam+'_'+k
			else: tmpName = listCuts[0][0][0]+'Vs'+listCuts[0][1][0][3:]+'_'+sam+'_'+k
			allHistos[ tmpName ] = TH2F( tmpName, tmpName, 
					(50 if 'deltaEta' in listCuts[0][0][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[0][0][0] else 1. ),
					(50 if 'deltaEta' in listCuts[0][1][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[0][1][0] else 1. ) 
					)

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
		for tmpk in listCuts:
			for k in tmpk: cutFlowList[ k[0] ] = 0

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

			if 'Data' in samples: scale = 1
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
				if len(listCuts) > 0:
					for setCuts in listCuts:
						tmpBoolList = []
						for var in setCuts: 
							allHistos[ var[0]+'_'+sample ].Fill( getattr( events, var[0] ), scale )
							if ( getattr( events, var[0] ) < var[1] ):
								tmpBoolList.append( True )
								cutFlowList[ var[0] ] += 1
							else: tmpBoolList.append( False )
						sigCutsList.append( tmpBoolList )
				else: print 'Correct selection dictionary'

				if all(sigCutsList[1]):    ## pass first selection
					plotABCD( sigCutsList[0][0], sigCutsList[0][1], listCuts[0], events, massAve, scale, sample )
					if all(sigCutsList[0]): 	### pass second selection
						allHistos[ 'massAve_'+sample ].Fill( massAve, scale )
						
		dummy = 1
		for q in cutFlowList: 
			allHistos[ 'cutFlow_'+sample ].SetBinContent( dummy, cutFlowList[q] )
			allHistos[ 'cutFlow_'+sample ].GetXaxis().SetBinLabel( dummy, q )
			dummy+=1
			
		allHistos[ 'massAve_'+sample+'_Bkg' ].Multiply( allHistos[ 'massAve_'+sample+'_D' ] )
		allHistos[ 'massAve_'+sample+'_Bkg' ].Divide( allHistos[ 'massAve_'+sample+'_C' ] )

		'''
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

	###### Extra: send prints to file
	#if couts == False: 
	#	sys.stdout = outfileStdOut
	#	f.close()
	#########################

def plotABCD( sel1, sel2, var, fromTree, massAve, scale, sample ):
	"""docstring for plotABCD"""

	if len(var) == 2:
		if sel1 and sel2: 
			allHistos[ 'massAve_'+sample+'_A' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0]+'_'+sample+'_A' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
		elif sel1 and not sel2: 
			allHistos[ 'massAve_'+sample+'_B' ].Fill( massAve, scale )
			allHistos[ 'massAve_'+sample+'_Bkg' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0]+'_'+sample+'_B' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
		elif not sel1 and sel2: 
			allHistos[ 'massAve_'+sample+'_D' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0]+'_'+sample+'_D' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
		else:
			allHistos[ 'massAve_'+sample+'_C' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0]+'_'+sample+'_C' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
	else:
		if sel1 and (sel2[0][0] and sel2[1][0]): 
			allHistos[ 'massAve_'+sample+'_A' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_A' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_A' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[2][0] ), scale )
		elif sel1 and not ( sel2[0][0] and sel2[1][0] ): 
			allHistos[ 'massAve_'+sample+'_B' ].Fill( massAve, scale )
			allHistos[ 'massAve_'+sample+'_Bkg' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_B' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_B' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[2][0] ), scale )
		elif not sel1 and ( sel2[0][0] and sel2[1][0] ): 
			allHistos[ 'massAve_'+sample+'_D' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_D' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_D' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[2][0] ), scale )
		else:
			allHistos[ 'massAve_'+sample+'_C' ].Fill( massAve, scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_C' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[1][0] ), scale )
			allHistos[ var[0][0]+'Vs'+var[1][0][3:]+'_'+sample+'_C' ].Fill( getattr( fromTree, var[0][0] ), getattr( fromTree, var[2][0] ), scale )


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
	allSamples[ 'RPVSt'+str(mass) ] = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'QCDPtAll' ] = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'TTJets' ] = 'Rootfiles/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WJetsToQQ' ] = 'Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'ZJetsToQQ' ] = 'Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WWTo4Q' ] = 'Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'ZZTo4Q' ] = 'Rootfiles/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	allSamples[ 'WZ' ] = 'Rootfiles/RUNAnalysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'


	selection = OrderedDict()
	selection[ 'Dibosons' ] = [ [ [ 'massAsym', 0.65 ], [ 'jet1Tau21', 0.55 ], [ 'jet2Tau21', 0.55 ] ], [ [ 'jet1Tau31', 0.35 ], [ 'jet2Tau31', 0.35 ] ] ]
	selection[ 'RPVSt100' ] = [ [ [ 'massAsym', 0.30 ], [ 'deltaEtaDijet', 0.7 ] ], [ [ 'jet1Tau21', 0.5 ], [ 'jet2Tau21', 0.5 ], [ 'jet1Tau31', 0.5, 4 ], [ 'jet2Tau31', 0.5, 4 ] ] ]
	selection[ 'RPVSt200' ] = [ [ [ 'massAsym', 0.10 ], [ 'deltaEtaDijet', 0.9 ] ], [ [ 'jet1Tau21', 0.4 ], [ 'jet2Tau21', 0.4 ] ] ]
		

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
