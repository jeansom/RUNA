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
import MakePlots
from MakePlots import *
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis, finalLabels, setSelection
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.commonFunctions import * 
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

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1, 1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

yline11 = array('d', [1.1, 1.1])
line11 = TGraph(2, xline, yline11)
line11.SetLineColor(kGreen)

yline09 = array('d', [0.9, 0.9])
line09 = TGraph(2, xline, yline09)
line09.SetLineColor(kGreen)

yline0 = array('d', [0,0])
line0 = TGraph(2, xline, yline0)
line0.SetLineColor(kRed)

class TransferFunction:
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
		'''
		self.ErrUp = TF1("QuadraticSelf.FitErrorUp", "[0]+ [1]*x + [2]*x*x + sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))",self.rm,self.rp)
		self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
		self.ErrUp.SetParameter(1, self.fit.GetParameter(1))
		self.ErrUp.SetParameter(2, self.fit.GetParameter(2))
		self.ErrUp.SetParameter(3, self.fit.GetParErrors()[0])
		self.ErrUp.SetParameter(4, self.fit.GetParErrors()[1])
		self.ErrUp.SetParameter(5, self.fit.GetParErrors()[2])
		self.ErrUp.SetParameter(6, fitter.GetCovarianceMatrixElement(0,1))
		self.ErrUp.SetParameter(7, fitter.GetCovarianceMatrixElement(0,2))
		self.ErrUp.SetParameter(8, fitter.GetCovarianceMatrixElement(1,2))
		self.ErrDn = TF1("QuadrarticSelf.FitErrorDn", "[0]+ [1]*x + [2]*x*x - sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))",self.rm,self.rp)
		self.ErrDn.SetParameter(0, self.fit.GetParameter(0))
		self.ErrDn.SetParameter(1, self.fit.GetParameter(1))
		self.ErrDn.SetParameter(2, self.fit.GetParameter(2))
		self.ErrDn.SetParameter(3, self.fit.GetParErrors()[0])
		self.ErrDn.SetParameter(4, self.fit.GetParErrors()[1])
		self.ErrDn.SetParameter(5, self.fit.GetParErrors()[2])
		self.ErrDn.SetParameter(6, fitter.GetCovarianceMatrixElement(0,1))
		self.ErrDn.SetParameter(7, fitter.GetCovarianceMatrixElement(0,2))
		self.ErrDn.SetParameter(8, fitter.GetCovarianceMatrixElement(1,2))
		'''
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
	def bkgEstFunction( self, rootFile, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):
		outputFileName = nameInRoot+'_all_MC_transferfunction_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension	
		
		print 'Processing.......', outputFileName
		
		bkgHistos = OrderedDict()
		if isinstance( rootFile, dict):
			for bkgSam in rootFile:
				print bkgSam
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

		self.hBkg_BD = TH1D( "h", "h", 12, 3, 15 )
		self.hBkg_BD.Reset()

		x = []
		y = []
		exl = []
		eyl = []
		exh = []
		eyh = []
		
		bins = []
		
		self.hBkg_BD = hBkg_B.Clone()
		self.hBkg_BD.Divide( hBkg_D )
		
		for b in xrange( 11, 72 ):
			print " -=-=-=-=-=-=-=-=--=-=- " + str(b)
			print str(float(b))
			passed = hBkg_B.GetBinContent( b )
			failed = hBkg_D.GetBinContent( b )

			ep = math.sqrt( passed )
			ef = math.sqrt( failed )
			
			if failed != 0 and passed != 0: 
				err = (passed/(failed))*((ep/passed)+(ef/failed))
				x.append( float(b * 5) )
				exl.append(2.5)
				exh.append(2.5)
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

		self.GetRates( 11, 71 )
#		self.MakeConvFactor()
		hBkg_Est = hBkg_D.Clone()
		hBkg_Est.Reset()
		for b in xrange(11,71):
			hBkg_Est.SetBinContent(b, hBkg_C.GetBinContent(b) * self.fit.Eval( float(b)*5 ) )
		hRatiohBkg = ratioPlots( hBkg_A, hBkg_Est )
		makePlots( nameInRoot, hBkg_A, 'All MCs SR', hBkg_Est, 'ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCBkgTransfer_Log', True )
		
		canBD = TCanvas( 'canBD', 'canBD', 10, 10, 750, 500 )
#		self.hBkg_BD.Draw("ep")
		#hBkg_Est.Draw()
#		print self.fit.GetParameter(0)
#		print self.fit.GetParameter(1)
#		print self.fit.GetParameter(2)
		
		self.G.Draw("A*")
		canBD.SaveAs( "BkgEstWithTransferFunctionPlot.png" )
	
