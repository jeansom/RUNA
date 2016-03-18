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
def bkgEstimator( dictSamples, listCuts, listABCDCuts, signalName, binSize ):


	outputFileName = 'Rootfiles/RUNBkgEstimation_'+args.process+'_'+args.grooming+'_'+args.RANGE+'_v2.root' 
	outputFile = TFile( outputFileName, 'RECREATE' )

	###################################### output Tree
	#tree = TTree('RUNAFinTree'+grooming, 'RUNAFinTree'+grooming)
	#AvgMass = array( 'f', [ 0. ] )
	#tree.Branch( 'AvgMass', AvgMass, 'AvgMass/F' )
	#Scale = array( 'f', [ 0. ] )
	#tree.Branch( 'Scale', Scale, 'Scale/F' )


	################################################################################################## Histos
	massBins = 500/binSize
	massXmin = 0.
	massXmax = 500.

	tmpName = listABCDCuts[0][0]+'Vs'+listABCDCuts[1][0]
	allHistos[ "massAve_"+tmpName+'_ABCDProj' ] = TH1F( "massAve_"+tmpName+'_ABCDProj', "massAve_"+tmpName+'_ABCDProj', massBins, massXmin, massXmax )
	allHistos[ "massAve_"+tmpName+'_ABCDProj' ].Sumw2()
	allHistos[ "massAve_"+tmpName+'_QCDHTAll_BC' ] = TH1F( "massAve_"+tmpName+'_QCDHTAll_BC', "massAve_"+tmpName+'_QCDHTAll_BC', massBins, massXmin, massXmax )
	allHistos[ "massAve_"+tmpName+'_QCDHTAll_BC' ].Sumw2()

	for k in [ 'A', 'B', 'C', 'D' ]:
		allHistos[ "massAve_"+tmpName+'_QCDHTAll_'+k ] = TH1F( "massAve_"+tmpName+'_QCDHTAll_'+k, "massAve_"+tmpName+'_QCDHTAll_'+k, massBins, massXmin, massXmax )
		allHistos[ "massAve_"+tmpName+'_QCDHTAll_'+k ].Sumw2()
	for sam in dictSamples:
		tmpNameSam = tmpName+'_'+sam
		allHistos[ "massAve_"+tmpNameSam+'_ABCDProj' ] = TH1F( "massAve_"+tmpNameSam+'_ABCDProj', "massAve_"+tmpNameSam+'_ABCDProj', massBins, massXmin, massXmax )
		allHistos[ "massAve_"+tmpNameSam+'_ABCDProj' ].Sumw2()
		allHistos[ tmpNameSam+'_Bkg' ] = TH2F( tmpNameSam+'_Bkg', tmpNameSam+'_Bkg', 
				(50 if 'deltaEta' in listABCDCuts[0][0] else 20 ), 0., (5. if 'deltaEta' in listABCDCuts[0][0] else 1. ),
				(50 if 'deltaEta' in listABCDCuts[1][0] else 20 ), 0., (5. if 'deltaEta' in listABCDCuts[1][0] else 1. ) 
				)
		allHistos[ tmpNameSam+'_Bkg' ].Sumw2()

		for k in [ 'A', 'B', 'C', 'D' ]:
			allHistos[ "massAve_"+tmpNameSam+'_'+k ] = TH1F( "massAve_"+tmpNameSam+'_'+k, "massAve_"+tmpNameSam+'_'+k, massBins, massXmin, massXmax )
			allHistos[ "massAve_"+tmpNameSam+'_'+k ].Sumw2()
			allHistos[ tmpNameSam+'_'+k ] = TH2F( tmpNameSam+'_'+k, tmpNameSam+'_'+k, 
					(50 if 'deltaEta' in listABCDCuts[0][0] else 20 ), 0., (5. if 'deltaEta' in listABCDCuts[0][0] else 1. ),
					(50 if 'deltaEta' in listABCDCuts[1][0] else 20 ), 0., (5. if 'deltaEta' in listABCDCuts[1][0] else 1. ) 
					)
			allHistos[ tmpNameSam+'_'+k ].Sumw2()

	################################################################################################## Running the Analysis
	BsideContent = OrderedDict()
	CsideContent = OrderedDict()
	DsideContent = OrderedDict()
	BsideError = OrderedDict()
	CsideError = OrderedDict()
	DsideError = OrderedDict()
	for sample in dictSamples:

		####### Get GenTree 
		inputFile, events, numEntries = getTree( dictSamples[ sample ], ('BoostedAnalysisPlotsPuppi/RUNATree' if 'Puppi' in args.grooming else 'BoostedAnalysisPlots/RUNATree' ) )
		print '-'*40
		print '------> ', sample
		print '------> Number of events: '+str(numEntries)
		d = 0

		for i in xrange(numEntries):
			events.GetEntry(i)

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
			numJets		= events.numJets
			massAve		= getattr( events, (args.grooming+"MassAve").replace('Puppi','') )
			jet1Pt          = events.jet1Pt
			jet2Pt          = events.jet2Pt
			#print 'Entry ', Run, ':', Lumi, ':', NumEvent

			#### Pre-selection
			HTCut = ( HT > 900 )
			dijetCut =  ( numJets > 1 )
			jetPtCut =  ( jet1Pt > 500 ) and ( jet2Pt > 450 )
			
			allCuts = False
			if HTCut and dijetCut and jetPtCut:
				sigCutsList = []
				for var in listCuts:
					if ( getattr( events, var[0] ) < var[1] ): sigCutsList.append( True )
					else: sigCutsList.append( False )
				if all(sigCutsList): allCuts = True

				if allCuts:
					allHistos[ tmpName+'_'+sample+'_Bkg' ].Fill( getattr( events, listABCDCuts[0][0] ), getattr( events, listABCDCuts[1][0] ), 2606*puWeight*lumiWeight)
					plotABCD( [ ( getattr( events, listABCDCuts[0][0] ) < listABCDCuts[0][1] ), ( getattr( events, listABCDCuts[1][0] ) < listABCDCuts[1][1] ) ], [ listABCDCuts[0][0], listABCDCuts[1][0] ], events, massAve, 2606*puWeight*lumiWeight, sample )

		#BsideContent[ sample ], BsideError[ sample ]  = listOfCont( allHistos[ 'massAve_'+tmpName+'_'+sample+'_B' ] )
		#CsideContent[ sample ], CsideError[ sample ]  = listOfCont( allHistos[ 'massAve_'+tmpName+'_'+sample+'_C' ] )
		#DsideContent[ sample ], DsideError[ sample ]  = listOfCont( allHistos[ 'massAve_'+tmpName+'_'+sample+'_D' ] )

		#for ibkg in BsideContent: 
		#	 BCDHisto( allHistos[ 'massAve_'+tmpName+'_'+sample+'_ABCDProj' ], BsideContent[ ibkg ], CsideContent[ ibkg ], DsideContent[ ibkg ] )

	if 'Bkg' in args.process:
		for sample in dictSamples:
			if 'QCD' in sample: 
				allHistos[ 'massAve_'+tmpName+'_QCDHTAll_A' ].Add( allHistos[ 'massAve_'+tmpName+'_'+sample+'_A' ] )
				allHistos[ 'massAve_'+tmpName+'_QCDHTAll_B' ].Add( allHistos[ 'massAve_'+tmpName+'_'+sample+'_B' ] )
				allHistos[ 'massAve_'+tmpName+'_QCDHTAll_C' ].Add( allHistos[ 'massAve_'+tmpName+'_'+sample+'_C' ] )
				allHistos[ 'massAve_'+tmpName+'_QCDHTAll_D' ].Add( allHistos[ 'massAve_'+tmpName+'_'+sample+'_D' ] )
		allHistos[ 'massAve_'+tmpName+'_QCDHTAll_BC' ].Multiply( allHistos[ 'massAve_'+tmpName+'_QCDHTAll_B' ], allHistos[ 'massAve_'+tmpName+'_QCDHTAll_C' ], 1, 1, '')
		allHistos[ 'massAve_'+tmpName+'_ABCDProj' ].Divide( allHistos[ 'massAve_'+tmpName+'_QCDHTAll_BC' ], allHistos[ 'massAve_'+tmpName+'_QCDHTAll_D' ], 1, 1, '')
		'''
		for jbin in range( 0, allHistos[ 'massAve_'+tmpName+'_ABCDProj' ].GetNbinsX() ):
			Bcont = Ccont = Dcont = 0
			Berr = Cerr = Derr = 0
			for sample in dictSamples:
				nameABCD = tmpName+'_'+sample
				scale = scaleFactor( sample )
				#scale = 2606 * SF
				Bcont += scale * allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinContent( jbin )
				try: Berr += TMath.Power( scale* allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinError( jbin ) , 2 )
				#try: Berr += scale* TMath.Power( allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinError( jbin ) / allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinContent( jbin ), 2 )
				#try: Berr += scale* TMath.Power( TMath.Sqrt( allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinContent( jbin ) ) / allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinContent( jbin ), 2 )
				except ZeroDivisionError: Berr += 0 
				Ccont += scale * allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinContent( jbin )
				try: Cerr += TMath.Power( scale* allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinError( jbin ) , 2 )
				#try: Cerr += scale* TMath.Power( allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinError( jbin ) / allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinContent( jbin ), 2 )
				#try: Cerr += scale* TMath.Power( TMath.Sqrt( allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinContent( jbin ) ) / allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinContent( jbin ), 2 )
				except ZeroDivisionError: Cerr += 0 
				Dcont += scale *allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinContent( jbin )
				try: Derr += TMath.Power( scale* allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinError( jbin ) , 2 )
				#try: Derr += scale* TMath.Power( allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinError( jbin ) / allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinContent( jbin ), 2 )
				#try: Derr += scale* TMath.Power( TMath.Sqrt( allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinContent( jbin ) ) / allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinContent( jbin ), 2 )
				except ZeroDivisionError: Derr += 0 
				

			try: iCont = Bcont * Ccont / Dcont
			except ZeroDivisionError: iCont = 0 

			try: iErr = iCont * TMath.Sqrt( Berr + Cerr + Derr ) 
			#try: iErr = iCont * TMath.Sqrt( TMath.Power( BErr / Bcont , 2 ) + TMath.Power( CErr / Ccont , 2 ) + TMath.Power( DErr / Dcont , 2 ) )
			except ZeroDivisionError: iErr = 0 

			allHistos[ 'massAve_'+tmpName+'_ABCDProj' ].SetBinContent( jbin, iCont )
			allHistos[ 'massAve_'+tmpName+'_ABCDProj' ].SetBinError( jbin, iErr )
		'''
	else: 
		for sample in dictSamples:
			nameABCD = tmpName+'_'+sample
			for ibin in range( 0, allHistos[ 'massAve_'+nameABCD+'_B' ].GetNbinsX() ):
				Bcont = allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinContent( ibin )
				Berr = allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinError( ibin )
				Ccont = allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinContent( ibin )
				Cerr = allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinError( ibin )
				Dcont = allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinContent( ibin )
				Derr = allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinError( ibin )

				try: Nbkg = ( Bcont * Ccont ) / Dcont
				except ZeroDivisionError: Nbkg = 0
				allHistos[ "massAve_"+nameABCD+'_ABCDProj' ].SetBinContent( ibin, Nbkg )
				#try: NbkgErr = Nbkg * TMath.Sqrt( TMath.Power( Berr / Bcont, 2 ) + TMath.Power( Cerr / Ccont, 2 ) + TMath.Power( Derr / Dcont, 2 ) )
				try: NbkgErr = Nbkg * TMath.Sqrt( TMath.Power( TMath.Sqrt(Bcont) / Bcont, 2 ) + TMath.Power( TMath.Sqrt(Ccont) / Ccont, 2 ) + TMath.Power( TMath.Sqrt(Dcont) / Dcont, 2 ) )
				except ZeroDivisionError: NbkgErr = 0
				allHistos[ "massAve_"+nameABCD+'_ABCDProj' ].SetBinError( ibin, NbkgErr )

	outputFile.Write()
	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Close()


def plotABCD( listSel, var, fromTree, massAve, scale, sample ):
	"""docstring for plotABCD"""

	nameABCD = var[0]+'Vs'+var[1]+'_'+sample
	if listSel[0] and listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_A' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_A' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	elif listSel[0] and not listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_B' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_B' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	elif not listSel[0] and listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_C' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_C' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	else:
		allHistos[ 'massAve_'+nameABCD+'_D' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_D' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )


def listOfCont( histo ):
 	"""docstring for listOfCont"""
	tmpListContent = []
	tmpListError = []
	for ibin in range( histo.GetNbinsX() ): 
		tmpListContent.append( histo.GetBinContent( ibin ) )
		tmpListError.append( histo.GetBinError( ibin ) )
	return tmpListContent, tmpListError

def BCDHisto( tmpHisto, BList, CList, DList ):
	"""docstring for BCDHisto"""

	#tmpHisto.Reset()
	for jbin in range( len( BList ) ):
		Nominal_Side = BList[ jbin ]
		Side_Side = CList[ jbin ]
		Side_Nominal = DList[ jbin ]
		if Side_Side != 0: 
			Bkg = Nominal_Side*Side_Nominal/Side_Side
			#BkgError = TMath.Sqrt( Bkg ) 
			try: BkgError = Bkg * TMath.Sqrt( TMath.Power(( TMath.Sqrt( Nominal_Side ) / Nominal_Side ), 2) + TMath.Power(( TMath.Sqrt( Side_Nominal ) / Side_Nominal ), 2) + TMath.Power(( TMath.Sqrt( Side_Side ) / Side_Side ), 2) )
			except ZeroDivisionError: BkgError = 0
		else: 
			Bkg = 0
			BkgError = 0
		tmpHisto.SetBinContent( jbin, Bkg )
		tmpHisto.SetBinError( jbin, BkgError )
	#return tmpHisto


#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-b', '--binSize', action='store', dest='binSize', default=10, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store',  dest='grooming', default='pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='single', help='Process: all or single.' )
	parser.add_argument( '-r', '--range', action='store',  dest='RANGE', default='low', help='Process: all or single.' )
	#parser.add_argument( '-s', '--sample', action='store',   dest='samples', default='RPV', help='Type of sample' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	process = args.process

	allSamples = {}
	if 'DATA' in process: allSamples[ 'DATA' ] = 'Rootfiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v1p0_v02.root'
	elif 'RPV' in process: 
		allSamples[ 'RPVStopStopToJets_UDD312_M-'+str(mass) ] = 'Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
	elif 'QCDHT' in process: 
		#allSamples[ 'QCDPtAll' ] = 'Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
		allSamples[ 'QCDHT500to700' ] = 'Rootfiles/RUNAnalysis_QCD_HT500to700_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
		allSamples[ 'QCDHT700to1000' ] = 'Rootfiles/RUNAnalysis_QCD_HT700to1000_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
		allSamples[ 'QCDHT1000to1500' ] = 'Rootfiles/RUNAnalysis_QCD_HT1000to1500_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
		allSamples[ 'QCDHT1500to2000' ] = 'Rootfiles/RUNAnalysis_QCD_HT1500to2000_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'
		allSamples[ 'QCDHT2000toInf' ] = 'Rootfiles/RUNAnalysis_QCD_HT2000toInf_RunIIFall15MiniAODv2_v76x_v1p0_v02.root'

	samples = 'RPVStopStopToJets_UDD312_M-'+str(mass)
	signalSample = ( 'Dibosons' if 'Dibosons' in mass else samples  )
	try: cuts = selection[ signalSample ]
	except KeyError: 
		print 'Mass', mass, 'not in list.'
		sys.exit(0)
	allHistos = {}
	
	p = Process( target=bkgEstimator, args=( allSamples, cuts[:-2], cuts[-2:], signalSample, args.binSize ) )
	p.start()
	p.join()
