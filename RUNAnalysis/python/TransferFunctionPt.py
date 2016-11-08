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
#from RUNA.RUNAnalysis.MakePlots import *
import MakePlots
from MakePlots import *
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis, finalLabels, setSelection
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.commonFunctions import * 
	from RUNA.RUNAnalysis.cuts import selection 
	from RUNA.RUNAnalysis.StackHistos import *
	from RUNA.RUNAnalysis.TransferFunction import *
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

class TransferFunctionPt:
	def __init__(self):
		self.name = "test"
	def MakeConvFactor(self):
		self.X = "deltaEtaDijet-0"
		self.ConvFact = "({0:2.9f} + (({3})*{1:2.9f}) + (({3})*({3})*{2:2.9f}))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.X)
		ConvFactUp = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) + (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),self.X)
		ConvFactDn = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) - (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrDn.GetParameter(0),self.ErrDn.GetParameter(1),self.ErrDn.GetParameter(2),self.ErrDn.GetParameter(3),self.ErrDn.GetParameter(4),self.ErrDn.GetParameter(5),self.ErrDn.GetParameter(6),self.ErrDn.GetParameter(7),self.ErrDn.GetParameter(8),self.X)

	def GetRates( self, range_min, range_max ):
		self.rm = range_min
		self.rp = range_max
		self.fit = TF1( "QuadraticFit", " [0] + [1]*x + [2]*x*x + [3]*x*x*x", self.rm, self.rp )
		self.fit.SetParameter( 1, 0 )
		self.fit.SetParameter( 2, 0 )
		self.fitter()

	def fitter(self):
		self.G.Fit( self.fit )
		fitter = TVirtualFitter.GetFitter()
		self.Converter(fitter)

	def Converter( self,fitter ):
		errTerm = "[4]^2+((2*[8])*x)+(([5]^2+2*[9])*x^2)+((2*[10]+2*[11])*x^3)+(([6]^2+2*[12])*x^4)+((2*[13])*x^5)+(([7]^2)*x^6)"
		self.ErrUp = TF1("CubicFitErrorUp"+self.name, "[0]+ [1]*x + [2]*x*x + [3]*x*x*x + sqrt("+errTerm+")",self.rm,self.rp)
		self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
		self.ErrUp.SetParameter(1, self.fit.GetParameter(1))
		self.ErrUp.SetParameter(2, self.fit.GetParameter(2))
		self.ErrUp.SetParameter(3, self.fit.GetParameter(3))
		self.ErrUp.SetParameter(4, self.fit.GetParErrors()[0])
		self.ErrUp.SetParameter(5, self.fit.GetParErrors()[1])
		self.ErrUp.SetParameter(6, self.fit.GetParErrors()[2])
		self.ErrUp.SetParameter(7, self.fit.GetParErrors()[3])
		self.ErrUp.SetParameter(8, fitter.GetCovarianceMatrixElement(0,1))
		self.ErrUp.SetParameter(9, fitter.GetCovarianceMatrixElement(0,2))
		self.ErrUp.SetParameter(10, fitter.GetCovarianceMatrixElement(0,3))
		self.ErrUp.SetParameter(11, fitter.GetCovarianceMatrixElement(1,2))
		self.ErrUp.SetParameter(12, fitter.GetCovarianceMatrixElement(1,3))
		self.ErrUp.SetParameter(13, fitter.GetCovarianceMatrixElement(2,3))
		self.ErrDn = TF1("CubicFitErrorUp"+self.name, "[0]+ [1]*x + [2]*x*x + [3]*x*x*x - sqrt("+errTerm+")",self.rm,self.rp)
		self.ErrDn.SetParameter(0, self.fit.GetParameter(0))
		self.ErrDn.SetParameter(1, self.fit.GetParameter(1))
		self.ErrDn.SetParameter(2, self.fit.GetParameter(2))
		self.ErrDn.SetParameter(3, self.fit.GetParameter(3))
		self.ErrDn.SetParameter(4, self.fit.GetParErrors()[0])
		self.ErrDn.SetParameter(5, self.fit.GetParErrors()[1])
		self.ErrDn.SetParameter(6, self.fit.GetParErrors()[2])
		self.ErrDn.SetParameter(7, self.fit.GetParErrors()[3])
		self.ErrDn.SetParameter(8, fitter.GetCovarianceMatrixElement(0,1))
		self.ErrDn.SetParameter(9, fitter.GetCovarianceMatrixElement(0,2))
		self.ErrDn.SetParameter(10, fitter.GetCovarianceMatrixElement(0,3))
		self.ErrDn.SetParameter(11, fitter.GetCovarianceMatrixElement(1,2))
		self.ErrDn.SetParameter(12, fitter.GetCovarianceMatrixElement(1,3))
		self.ErrDn.SetParameter(13, fitter.GetCovarianceMatrixElement(2,3))
		for i in [self.ErrUp, self.ErrDn]:
			i.SetLineStyle(2)

	def bkgEstFunctionPt( self, rootFile, nameInRoot, rootFile2, nameInRoot2, nameInRoot3, xmin, xmax, rebinX, labX, labY, log, version, binning, grooming, plotFolder, data=False, subtract=False, Norm=False ):
		outputFileName = nameInRoot+'_all_MC_transferfunction_pruned_bkgShapeEstimationBoostedPlots'+version+'.png'	
		
		print 'Processing.......', outputFileName
		
		bkgHistos = OrderedDict()
		hMassAveVsHT = OrderedDict()
		if isinstance( rootFile, dict):
			print "dictionary"

			hMassAveVsHT_C =  rootFile[ "QCDPtAll" ][0].Get( nameInRoot3 + "__C" ).Clone()
#			hMassAveVsHT_C.Add( rootFile[ "TTJets" ][0].Get( nameInRoot3 + "__C" ) )
#			hMassAveVsHT_C.Add( rootFile[ "WJetsToQQ" ][0].Get( nameInRoot3 + "__C" ) )
#			hMassAveVsHT_C.Add(rootFile[ "WWTo4Q" ][0].Get( nameInRoot3 + "__C" ))
#			hMassAveVsHT_C.Add(rootFile[ "WZ" ][0].Get( nameInRoot3 + "__C" ))
#			hMassAveVsHT_C.Add(rootFile[ "ZJetsToQQ" ][0].Get( nameInRoot3 + "__C" ))
#			hMassAveVsHT_C.Add(rootFile[ "ZZTo4Q" ][0].Get( nameInRoot3 + "__C" ))

			hMassAveVsHT_C.Reset()
			hMassAveVsHT[ "QCDPtAll" ] = rootFile[ "QCDPtAll" ][0].Get( nameInRoot3 + "__C" )
			for bkgSam in rootFile:
				hMassAveVsHT_C.Add(rootFile[ bkgSam ][0].Get( nameInRoot3 + "__C" ).Clone())
				hMassAveVsHT[ bkgSam ] = rootFile[ bkgSam ][0].Get( nameInRoot3+"__C" )
				bkgHistos[ bkgSam+'_A' ] = rootFile[ bkgSam ][0].Get( nameInRoot2+'__A' )
				bkgHistos[ bkgSam+'_B' ] = rootFile[ bkgSam ][0].Get( nameInRoot+'__B' )
				bkgHistos[ bkgSam+'_C' ] = rootFile[ bkgSam ][0].Get( nameInRoot+'__C' )
				bkgHistos[ bkgSam+'_D' ] = rootFile[ bkgSam ][0].Get( nameInRoot+'__D' )
		elif data:
			plotFolder = plotFolder + 'DATA'
			print "file1"
			bkgSam = 'DATA'
			bkgHistos[ bkgSam+'_B' ] = rootFile.Get( nameInRoot+'__B' )
			bkgHistos[ bkgSam+'_C' ] = rootFile.Get( nameInRoot+'__C' )
			bkgHistos[ bkgSam+'_D' ] = rootFile.Get( nameInRoot+'__D' )
			hMassAveVsHT_C = rootFile.Get( nameInRoot3+'__C' )
			if isinstance( rootFile2, dict):
				print "dictionary2"
				for bkgSam in rootFile2:
					bkgHistos[ bkgSam+'_A' ] = rootFile2[ bkgSam ][0].Get( nameInRoot2+'__A' )
			else: 
				print "file2"
				bkgSam = 'bkg'
				bkgHistos[ bkgSam+'_A' ] = rootFile2.Get( nameInRoot2+'__A' )
		else:
			print "file"
			bkgSam = 'bkg'
			bkgHistos[ bkgSam+'_A' ] = rootFile.Get( nameInRoot2+'__A' )
			bkgHistos[ bkgSam+'_B' ] = rootFile.Get( nameInRoot+'__B' )
			bkgHistos[ bkgSam+'_C' ] = rootFile.Get( nameInRoot+'__C' )
			bkgHistos[ bkgSam+'_D' ] = rootFile.Get( nameInRoot+'__D' )
			hMassAveVsHT_C = rootFile.Get( nameInRoot3+'__C' )
		
			
#		for bkgSam in hMassAveVsHT:
#			hMassAveVsHT_C.Add( hMassAveVsHT[ bkgSam ].Clone() )

#		hMassAveVsHT_C = ( hMassAveVsHT[ "QCDPtAll" ].Clone() )

		hBkgSamples_A = OrderedDict()
		#hBkgSamples_A[ "Z + Jets" ] = bkgHistos[ "ZJetsToQQ_A" ].Clone()
		#hBkgSamples_A[ "ZZ (had)" ] = bkgHistos[ "ZZTo4Q_A" ].Clone()
		#hBkgSamples_A[ "WW (had)" ] = bkgHistos[ "WWTo4Q_A" ].Clone()
		#hBkgSamples_A[ "WZ" ] = bkgHistos[ "WZ_A" ].Clone()
		#hBkgSamples_A[ "QCD" ] = bkgHistos[ "QCDPtAll_A" ].Clone()
		hBkgSamples_A[ "W + Jets" ] = bkgHistos[ "WJetsToQQ_A" ].Clone()
		hBkgSamples_A[ "tt + Jets" ] = bkgHistos[ "TTJets_A" ].Clone()

		hBkgSamples_A[ "All MC Signal Region" ] = bkgHistos[ "QCDPtAll_A" ].Clone()
#		hBkgSamples_A[ "All MC Signal Region" ].Add(bkgHistos[ "ZJetsToQQ_A" ])
#		hBkgSamples_A[ "All MC Signal Region" ].Add(bkgHistos[ "ZZTo4Q_A" ])
#		hBkgSamples_A[ "All MC Signal Region" ].Add(bkgHistos[ "WWTo4Q_A" ])
#		hBkgSamples_A[ "All MC Signal Region" ].Add(bkgHistos[ "WZ_A" ])
		hBkgSamples_A[ "All MC Signal Region" ].Add(bkgHistos[ "TTJets_A" ])
		hBkgSamples_A[ "All MC Signal Region" ].Add(bkgHistos[ "WJetsToQQ_A" ])
		for bkgSam in bkgHistos:
			if '_A' in bkgSam: hBkg_A = bkgHistos[ bkgSam ].Clone()
		hBkg_A.Reset()
		for samples in bkgHistos:
			if '_A' in samples: hBkg_A.Add( bkgHistos[samples].Clone() )
		    
		for bkgSam in bkgHistos:
			if '_B' in bkgSam: hBkg_B = bkgHistos[ bkgSam ].Clone()
		hBkg_B.Reset()
		for samples in bkgHistos:
			if '_B' in samples: hBkg_B.Add( bkgHistos[samples].Clone() )

		for bkgSam in bkgHistos:
			if '_C' in bkgSam: hBkg_C = bkgHistos[ bkgSam ].Clone()
		hBkg_C.Reset()
		for samples in bkgHistos:
			if '_C' in samples: hBkg_C.Add( bkgHistos[samples].Clone() )

		for bkgSam in bkgHistos:
			if '_D' in bkgSam: hBkg_D = bkgHistos[ bkgSam ].Clone()
		hBkg_D.Reset()
		for samples in bkgHistos:
			if '_D' in samples: hBkg_D.Add( bkgHistos[samples].Clone() )

		if subtract and not data and isinstance( rootFile, dict):
			hBkg_B.Add( rootFile['TTJets'][0].Get( nameInRoot+'__B' ), -1 )
			hBkg_C.Add( rootFile['TTJets'][0].Get( nameInRoot+'__C' ), -1 )
			hBkg_D.Add( rootFile['TTJets'][0].Get( nameInRoot+'__D' ), -1 )

			hMassAveVsHT_C.Add( rootFile['TTJets'][0].Get( nameInRoot3+'__C'), -1 )

			hBkg_B.Add( rootFile['WJetsToQQ'][0].Get( nameInRoot2+'__B' ), -1 )
			hBkg_C.Add( rootFile['WJetsToQQ'][0].Get( nameInRoot2+'__C' ), -1 )
			hBkg_D.Add( rootFile['WJetsToQQ'][0].Get( nameInRoot2+'__D' ), -1 )
			hMassAveVsHT_C.Add( rootFile['WJetsToQQ'][0].Get( nameInRoot3+'__C'), -1 )
		elif subtract and data and isinstance( rootFile2, dict):
			hBkg_B.Add( rootFile2['TTJets'][0].Get( nameInRoot+'__B' ), -1 )
			hBkg_C.Add( rootFile2['TTJets'][0].Get( nameInRoot+'__C' ), -1 )
			hBkg_D.Add( rootFile2['TTJets'][0].Get( nameInRoot+'__D' ), -1 )

			hBkg_B.Add( rootFile2['WJetsToQQ'][0].Get( nameInRoot+'__B' ), -1 )
			hBkg_C.Add( rootFile2['WJetsToQQ'][0].Get( nameInRoot+'__C' ), -1 )
			hBkg_D.Add( rootFile2['WJetsToQQ'][0].Get( nameInRoot+'__D' ), -1 )


		self.hBkg_BD = TH1D( "h", "h", 12, 3, 15 )
		self.hBkg_BD.Reset()

		x = []
		y = []
		exl = []
		eyl = []
		exh = []
		eyh = []
		
		bins = []

		hBkg_B.Rebin(500)
		hBkg_D.Rebin(500)

		self.hBkg_BD = hBkg_B.Clone()
		self.hBkg_BD.Divide( hBkg_D )
		
		for b in xrange( 2, 12 ):
			print " -=-=-=-=-=-=-=-=--=-=- " + str(b)
			print str(float(b))
			passed = hBkg_B.GetBinContent( b )
			print passed
			failed = hBkg_D.GetBinContent( b )
			print failed

			
			if failed > 0 and passed > 0: 
				ep = math.sqrt( passed )
				ef = math.sqrt( failed )

				print passed/failed
				err = (passed/(failed))*((ep/passed)+(ef/failed))
				x.append( float((b)*500 - 250) )
				exl.append(250)
				exh.append(250)
				y.append( passed/failed )
				self.hBkg_BD.SetBinContent( b, passed/failed )
				eyh.append(err)
				if (passed/failed)-err > 0.:
					eyl.append(err)
				else:
					eyl.append(passed/failed)
		print str(scipy.array(x))
#		print str(y)
		
		if len(x) > 0:
			self.G = TGraphAsymmErrors( len(x), scipy.array(x), scipy.array(y), scipy.array(exl), scipy.array(exh), scipy.array(eyl), scipy.array(eyh) )
		else:
			self.G = TGraphAsymmErrors()
		
#		print str(self.G.GetX())
#		print str(self.G.GetY())

		self.GetRates( 900, 5000 )
#		self.MakeConvFactor()
	
		hBkg_Est = hBkg_A.Clone()
		hBkg_Est_Up = hBkg_A.Clone()
		hBkg_Est_Dn = hBkg_A.Clone()
		hBkg_Est.Reset()
		hBkg_Est_Up.Reset()
		hBkg_Est_Dn.Reset()

		for m in xrange(50,351):
			for ht in range(900, 5001): 
				if m%5 == 0:
					b = hMassAveVsHT_C.FindBin( m, ht )
					nEvents = hMassAveVsHT_C.GetBinContent( b )
					factor = (float(self.fit.Eval( float( ht ) )))
					factorUp = (float(self.ErrUp.Eval( float( ht ) )))
					factorDn = (float(self.ErrDn.Eval( float( ht ) )))
					hBkg_Est.Fill( m, (float((nEvents * factor)) ))
					hBkg_Est_Up.Fill( m, (float((nEvents * factorUp)) ))
					hBkg_Est_Dn.Fill( m, (float((nEvents * factorDn)) ))
		if subtract and not data and isinstance( rootFile, dict):
			TTJets_A = rootFile['TTJets'][0].Get( nameInRoot2+'__A' )
			hBkg_Est.Add( TTJets_A )
			hBkg_Est_Up.Add( TTJets_A )
			hBkg_Est_Dn.Add( TTJets_A )
			WJetsToQQ_A = rootFile['WJetsToQQ'][0].Get( nameInRoot2+'__A' )
			hBkg_Est.Add( WJetsToQQ_A )
			hBkg_Est_Up.Add( WJetsToQQ_A )
			hBkg_Est_Dn.Add( WJetsToQQ_A )
		elif subtract and data and isinstance( rootFile2, dict):
			TTJets_A = rootFile2['TTJets'][0].Get( nameInRoot2+'__A' )
			hBkg_Est.Add( TTJets_A )
			hBkg_Est_Up.Add( TTJets_A )
			hBkg_Est_Dn.Add( TTJets_A )
			WJetsToQQ_A = rootFile2['WJetsToQQ'][0].Get( nameInRoot2+'__A' )
			hBkg_Est.Add( WJetsToQQ_A )
			hBkg_Est_Up.Add( WJetsToQQ_A )
			hBkg_Est_Dn.Add( WJetsToQQ_A )

		ErrHistos = OrderedDict()
		ErrHistos[ "Error Up" ] = hBkg_Est_Up
		ErrHistos[ "Error Down" ] = hBkg_Est_Dn


		hRatiohBkg = ratioPlots( hBkg_A, hBkg_Est )
		if subtract and data:
			makePlots( nameInRoot, hBkg_A, 'All MCs SR', hBkg_Est, 'DATA ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log_Subtract', binning, 'v05p5', grooming, plotFolder, True )
			StackHistos( nameInRoot, hBkgSamples_A, 'All MCs SR', hBkg_Est, 'DATA ABCD Pred', ErrHistos, 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log_Subtract', binning, 'v05p5', grooming, plotFolder, True )
		elif subtract and not data:
			makePlots( nameInRoot, hBkg_A, 'All MCs SR', hBkg_Est, 'ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log_Subtract', binning, 'v05p5', grooming, plotFolder, True )
			StackHistos( nameInRoot, hBkgSamples_A, 'All MCs SR', hBkg_Est, 'ABCD Pred', ErrHistos, 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log_Subtract', binning, 'v05p5', grooming, plotFolder, True )
		elif not subtract and data:
			makePlots( nameInRoot, hBkg_A, 'All MCs SR', hBkg_Est, 'DATA ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log', binning, 'v05p5', grooming, plotFolder, True )
			StackHistos( nameInRoot, hBkgSamples_A, 'All MCs SR', hBkg_Est, 'DATA ABCD Pred', ErrHistos, 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log', binning, 'v05p5', grooming, plotFolder, True )

		else:
			makePlots( nameInRoot, hBkg_A, 'All MCs SR', hBkg_Est, 'ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log', binning, 'v05p5', grooming, plotFolder, True )
			StackHistos( nameInRoot, hBkgSamples_A, 'All MCs SR', hBkg_Est, 'ABCD Pred', ErrHistos, 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransferHT_Log', binning, 'v05p5', grooming, plotFolder, True )
		
		canBD = TCanvas( 'canBD', 'canBD', 10, 10, 750, 500 )
		canBD.SetTitle( 'B / D and Fit' )
#		self.hBkg_BD.Draw("ep")
		#hBkg_Est.Draw()
#		print self.fit.GetParameter(0)
#		print self.fit.GetParameter(1)
#		print self.fit.GetParameter(2)
		
		self.G.Draw("A*")
		self.G.GetXaxis().SetTitle( "HT [GeV]" )
		self.G.GetYaxis().SetTitle( "Ratio B/D" )
#		self.G.GetYaxis().SetRangeUser( 0, 3 )
		gStyle.SetOptFit(1111)

		self.ErrUp.SetRange( 0, 6000 )
		self.ErrDn.SetRange( 0, 6000 )
		
		self.G.Draw("A*")
		self.ErrUp.Draw("same")
		self.ErrDn.Draw("same")
		if subtract:
			canBD.SaveAs( plotFolder+"BkgEstWithTransferFunctionHTPlotSubtract.png" )
		else:
			canBD.SaveAs( plotFolder+"BkgEstWithTransferFunctionHTPlot.png" )
	
