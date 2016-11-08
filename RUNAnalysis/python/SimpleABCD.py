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
import scipy
from collections import OrderedDict
from DrawHistogram import Rebin2D
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis, finalLabels, setSelection
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.commonFunctions import * 
        from RUNA.RUNAnalysis.MakePlots import *
	from RUNA.RUNAnalysis.cuts import selection 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis, finalLabels
	from scaleFactors import * #scaleFactor as SF
	from commonFunctions import * 
	from cuts import selection 
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle

def SimpleABCD( rootFile, nameInRoot, xmin, xmax, rebinX, labX, labY, plotFolder, version, binning, grooming, log=False, Norm=False ):

	outputFileName = nameInRoot+'_all_MC_pruned_bkgShapeEstimationBoostedPlots'+version+'.png'
	print 'Processing.......', outputFileName

        bkgHistos = OrderedDict()
        if isinstance( rootFile, dict):
            for bkgSam in rootFile:
                bkgHistos[ bkgSam+'_A' ] = rootFile[ bkgSam ][0].Get( nameInRoot+'__A' )
                bkgHistos[ bkgSam+'_B' ] = rootFile[ bkgSam ][0].Get( nameInRoot+'__B' )
                bkgHistos[ bkgSam+'_C' ] = rootFile[ bkgSam ][0].Get( nameInRoot+'__C' )
                bkgHistos[ bkgSam+'_D' ] = rootFile[ bkgSam ][0].Get( nameInRoot+'__D' )

	hBkg_A = bkgHistos[ bkgSam+'_A' ].Clone()
	hBkg_A.Reset()
	for samples in bkgHistos:
		if '_A' in samples: hBkg_A.Add( bkgHistos[samples].Clone() )
                                    
	hBkg_B = bkgHistos[ bkgSam+'_B' ].Clone()
	hBkg_B.Reset()
	for samples in bkgHistos:
		if '_B' in samples: hBkg_B.Add( bkgHistos[samples].Clone() )

	hBkg_C = bkgHistos[ bkgSam+'_C' ].Clone()
	hBkg_C.Reset()
	for samples in bkgHistos:
		if '_C' in samples: hBkg_C.Add( bkgHistos[samples].Clone() )
		
	hBkg_D = bkgHistos[ bkgSam+'_D' ].Clone()
	hBkg_D.Reset()
	for samples in bkgHistos:
		if '_D' in samples: hBkg_D.Add( bkgHistos[samples].Clone() )
		
	histoBC = hBkg_A.Clone()
	histoBC.Reset()
	histoBC.Multiply( hBkg_B, hBkg_C, 1, 1, '' )
	
	histoBCD = hBkg_A.Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, hBkg_D, 1, 1, '' )
	
	hRatiohBkg = ratioPlots( hBkg_A, histoBCD )
	makePlots( nameInRoot, hBkg_A, 'All MCs SR', histoBCD, 'All MC ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'All_MCBkg_Log', binning, version, grooming, plotFolder, True )
