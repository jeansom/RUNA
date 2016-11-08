#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
import time, os, math, sys
from array import array
import argparse
from DrawHistogram import Rebin2D
from RUNA.RUNAnalysis.TransferFunction import *
from RUNA.RUNAnalysis.MakePlots import *
from RUNA.RUNAnalysis.BkgEst2DPlots import *
from RUNA.RUNAnalysis.SimpleABCD import *
from RUNA.RUNAnalysis.TransferFunctionPt import *
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-b', '--binning', action='store', default='simple', help='Binning: resoBased or simple' )
	parser.add_argument('-v', '--version', action='store', default='v05', help='Version: v01, v02.' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-q', '--qcd', action='store', default='Pt', dest='qcd', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-l', '--lumi', action='store', default=2666, help='Luminosity, example: 1.' )
	parser.add_argument('-r', '--range', action='store', default='low', dest='RANGE', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--extension', action='store', default='png', help='Extension of plots.' )
	parser.add_argument('-B', '--bkgPlots', action='store', type=bool, default=False, help='Binning: resoBased or simple' )
	parser.add_argument('-f', '--folder', action='store', default='102216', help='Plot Folder' )
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)
	
	CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 1 ) )+" fb^{-1}"
	
	if 'Pt' in args.qcd: 
		#bkgLabel='(w QCD pythia8)'
		QCDSF = 0.77
	else: 
		#bkgLabel='(w QCD madgraphMLM+pythia8)'
		QCDSF = 1.05

	plotFolder = "/cms/data28/jeans/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/Plots/"+args.folder+"/"
	rootFolder = "/cms/data28/jeans/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/Rootfiles/"+args.folder+"/"

	bkgFiles = OrderedDict() 
	signalFiles = {}
	dataFile = TFile.Open(rootFolder+'RUNBkgEstimationUDD323_'+args.grooming+'_DATA_'+args.RANGE+'_'+args.version+'.root')
#	signalFiles[ 'Signal' ] = [ TFile.Open(rootFolder+'RUNBkgEstimationUDD323_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_'+args.RANGE+'_'+args.version+'.root'), 1, args.decay+' RPV #tilde{t} '+str(args.mass)+' GeV', kRed-4]
	bkgFiles[ 'TTJets' ] = [ TFile.Open('/cms/data28/jeans/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/Rootfiles/MiniBkgTau32Inverse/RUNBkgEstimationUDD323_'+args.grooming+'_TTJets_'+args.RANGE+'_'+args.version+'.root'),	1, 't #bar{t} + Jets', kGreen ]
 # 	bkgFiles[ 'ZJetsToQQ' ] = [ TFile.Open(rootFolder+'RUNBkgEstimationUDD323_'+args.grooming+'_ZJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'Z + Jets', kOrange]
    	bkgFiles[ 'WJetsToQQ' ] = [ TFile.Open('/cms/data28/jeans/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/Rootfiles/MiniBkgTau32Inverse/RUNBkgEstimationUDD323_'+args.grooming+'_WJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'W + Jets', kMagenta ]
#	bkgFiles[ 'WWTo4Q' ] = [ TFile.Open(rootFolder+'RUNBkgEstimationUDD323_'+args.grooming+'_WWTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1 , 'WW (had)', kMagenta+2 ]
#	bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open(rootFolder+'RUNBkgEstimationUDD323_'+args.grooming+'_ZZTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1, 'ZZ (had)', kOrange+2 ]
#	bkgFiles[ 'WZ' ] = [ TFile.Open(rootFolder+'RUNBkgEstimationUDD323_'+args.grooming+'_WZ_'+args.RANGE+'_'+args.version+'.root'), 1, 'WZ', kCyan ]
	bkgFiles[ 'QCD'+args.qcd+'All' ] = [ TFile.Open('/cms/data28/jeans/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/Rootfiles/MiniBkgTau32Inverse/RUNBkgEstimationUDD323_'+args.grooming+'_QCD'+args.qcd+'All_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]
	#bkgFiles[ 'QCDPtAll' ] = [ TFile.Open('/cms/data28/jeans/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/Rootfiles//102116/RUNBkgEstimationUDD323_'+args.grooming+'_QCDPtAll_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]


	massMinX = 0
	massMaxX = 510
	jetMassHTlabY = 0.20
	jetMassHTlabX = 0.85

	if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Groommers = [ args.grooming ]

	for optGroom in Groommers:
		if 'TransferFunction' in args.proc:
			transfun = TransferFunction()
			transfun.bkgEstFunction( bkgFiles, 'massAve_btagJet1VsbtagJet2', '', '', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder )
		if '2D' in args.proc:
			for bkg in bkgFiles: BkgEst2DPlots( bkgFiles[ bkg ][0], bkg, optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY, plotFolder, args.version, args.mass)
			BkgEst2DPlots( bkgFiles, "All MC", optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY, plotFolder, args.version, args.mass)
			for bkg in signalFiles: BkgEst2DPlots( signalFiles[ bkg ][0], 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass), optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY, plotFolder, args.version, args.mass)			
		if 'simple' in args.proc:
			SimpleABCD( bkgFiles, 'massAve_btagJet1VsbtagJet2', 0, massMaxX, 5, '', '', plotFolder, args.version, args.binning, args.grooming, False )	
		if 'DataTransfer' in args.proc:
			transfun = TransferFunction()
			transfun.bkgEstFunction( dataFile, 'massAve_btagJet1VsbtagJet2', bkgFiles, 'massAve_btagJet1VsbtagJet2', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder, True )
		if 'DataMinusTW' in args.proc:
			transfun = TransferFunction()
			transfun.bkgEstFunction( dataFile, 'massAve_btagJet1VsbtagJet2', bkgFiles, 'massAve_btagJet1VsbtagJet2', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder, True, True )
		if 'MCMinusTW' in args.proc:
			transfun = TransferFunction()
			transfun.bkgEstFunction( bkgFiles, 'massAve_btagJet1VsbtagJet2', '', '', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder, False, True )
		if 'MCTransFunPt' in args.proc:
			transfunpt = TransferFunctionPt()
			transfunpt.bkgEstFunctionPt( bkgFiles, 'ptAve_btagJet1VsbtagJet2', '', 'massAve_btagJet1VsbtagJet2', 'massAveVsptAve_btagJet1VsbtagJet2', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder, False, False )
		if 'DataTransFunPt' in args.proc:
			transfunpt = TransferFunctionPt()
			transfunpt.bkgEstFunctionPt( dataFile, 'ptAve_btagJet1VsbtagJet2', bkgFiles, 'massAve_btagJet1VsbtagJet2', 'massAveVsptAve_btagJet1VsbtagJet2', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder, True, False )
		if 'MCTransFunPtMinusTW' in args.proc:
			transfunpt = TransferFunctionPt()
			transfunpt.bkgEstFunctionPt( bkgFiles, 'ptAve_btagJet1VsbtagJet2', '', 'massAve_btagJet1VsbtagJet2', 'massAveVsptAve_btagJet1VsbtagJet2', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder, False, True )
		if 'DataTransFunPtMinusTW' in args.proc:
			transfunpt = TransferFunctionPt()
			transfunpt.bkgEstFunctionPt( dataFile, 'ptAve_btagJet1VsbtagJet2', bkgFiles, 'massAve_btagJet1VsbtagJet2', 'massAveVsptAve_btagJet1VsbtagJet2', 0, massMaxX, 5, '', '', False, args.version, args.binning, args.grooming, plotFolder, True, True ) # 
