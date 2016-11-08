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
	


def ratioPlots( histo1, histo2 ):
	"""docstring for ratioPlots"""

	chi2 = 0
	ndf = 0
	ratioList = []
	binCenterList = []
	ratioLogNErrXPlusList = []
	ratioLogNErrXMinusList = []

	for ibin in range( 0, histo1.GetNbinsX() ):
		binCenterList.append( histo1.GetXaxis().GetBinCenter( ibin ) )
		x = histo1.GetBinContent( ibin )
		xErr = histo1.GetBinError( ibin )
		y = histo2.GetBinContent( ibin )
		yErr = histo2.GetBinError( ibin )
		try: 
			ratio = x/y
			ratioErrX = ratio * TMath.Sqrt( TMath.Power( xErr/x, 2) + TMath.Power( yErr/y, 2)  )
			ratioErrY = ratio* yErr / y
			ratioLogNErrXPlus = TMath.Sqrt( TMath.Power( ( (x/(y-yErr)) - ratio ), 2 )  + TMath.Power( ( ((x+xErr)/y) - ratio ) , 2) ) 
			ratioLogNErrXMinus = TMath.Sqrt( TMath.Power( ( (x/(y+yErr)) - ratio ), 2 )  + TMath.Power( ( ((x-xErr)/y) - ratio ) , 2) ) 
		except ZeroDivisionError: 
			ratio = 0
			ratioErrX = 0
			ratioErrY = 0
			ratioLogNErrXPlus = 0
			ratioLogNErrXMinus = 0

		ratioList.append( ratio )
		ratioLogNErrXPlusList.append( ratioLogNErrXPlus )
		ratioLogNErrXMinusList.append( ratioLogNErrXMinus )

	zeroArray = array( 'd', ( [ 0 ] * (len( ratioList )) ) )
	asymErrors = TGraphAsymmErrors( len(ratioList), array('d', binCenterList), array('d', ratioList), zeroArray, zeroArray, array('d',ratioLogNErrXMinusList), array('d', ratioLogNErrXPlusList) )

	return asymErrors

def makePlots( nameInRoot, tmphisto1, labelh1, tmphisto2, labelh2, binWidth, xmin, xmax, ratio, labelRatio, ratio2, typePlot, log=False, reScale=False, addUncBand=True):

	histo1 = tmphisto1.Clone()
	histo2 = tmphisto2.Clone()
	legend=TLegend(0.55,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	if ('Pred' in labelh1) and ('Pred' in labelh2): legend.AddEntry( histo1, labelh1, 'l' )
	elif 'DATA' in labelh1: legend.AddEntry( histo1, labelh1, 'ep' )
	else: legend.AddEntry( histo1, labelh1, 'l' )
	legend.AddEntry( histo2, labelh2, 'pl' )

	histo1.GetYaxis().SetTitle('Events / '+(str(int(binWidth)) if 'simple' in args.binning else binWidth )+' GeV')
	histo1.GetXaxis().SetRangeUser( 60, 350 )
	histo1.SetMaximum( 11.1* max( histo1.GetMaximum(), histo2.GetMaximum() ) )
	if 'MC' in labelh1: 
		histo1.SetLineColor(kRed-4)
		histo1.SetLineWidth(2)
	elif ('Pred' in labelh1) and ('Pred' in labelh2):
		histo1.SetLineColor(kGreen-2)
		histo1.SetLineWidth(2)
	if not isinstance( histo2, THStack ):
		histo2.GetXaxis().SetRangeUser( 60, 350 )
		histo2.SetLineColor(kBlue-4)
		histo2.SetLineWidth(2)
		if 'MC' in labelh2: histo2.SetLineStyle(2)
		else: histo2.SetLineStyle(1)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: 
		pad1.SetLogy() 	
		if not 'Region' in labelh1: histo1.SetMaximum( (5000 if 'low' in args.RANGE else 500) )
		histo1.SetMinimum( 0.5 )
	else: 
		pad1.SetGrid()
	if ('Pred' in labelh1) and ('Pred' in labelh2): histo1.Draw("histe")
	elif 'DATA' in labelh1: 
		histo1.SetMarkerStyle(8)
		histo1.Draw("PE")
	else: histo1.Draw("histe")

	histo2.Draw('hist E0 same')

	tmpHisto1 = histo1.Clone()
	tmpHisto2 = histo2.Clone()

	if not isinstance( histo2, THStack ):
		try: 
			res = array( 'd', ( [ 0 ] * tmpHisto1.GetNbinsX() ) )
			chi2Ndf =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2/NDFP', res), 2 )
			chi2 =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2'), 2 )
			chi2Test = TLatex( 0.6, 0.7, '#chi^{2}/ndF Test = '+ str( chi2 )+'/'+str( round(chi2/chi2Ndf) ) )
			chi2Test.SetNDC()

			chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
			chi2Test.SetTextSize(0.04)
			chi2Test.Draw()
		except ZeroDivisionError: print ' |---> chi2Test failed. ZeroDivisionError'

		if 'DATA' in labelh1: tmpLabel = 'DATA'
		else: tmpLabel = 'SR'
		numEvents = TLatex( 0.6, 0.62, '#splitline{events '+tmpLabel+'/ABCD Pred = }{'+ str( round( histo1.Integral(),2 ) )+'/'+str( round( histo2.Integral(),2 ) )+'}' )
		numEvents.SetNDC()
		numEvents.SetTextFont(42) ### 62 is bold, 42 is normal
		numEvents.SetTextSize(0.04)
		numEvents.Draw()

	CMS_lumi.extraText = ("Preliminary" if 'DATA' in labelh2 else "Simulation Preliminary")
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend.Draw()

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	tmpPad2= pad2.DrawFrame(60,0,350,2)
	tmpPad2.SetXTitle( 'Average pruned mass [GeV]' )
	tmpPad2.SetYTitle( labelRatio )
	tmpPad2.SetTitleSize(0.12, "x")
	tmpPad2.SetTitleSize(0.12, 'y')
	tmpPad2.SetLabelSize(0.12, 'x')
	tmpPad2.SetLabelSize(0.12, 'y')
	tmpPad2.SetTitleOffset(0.5, 'y')
	tmpPad2.SetNdivisions(505, 'x' )
	tmpPad2.SetNdivisions(505, 'y' )
	pad2.Modified()
	
	ratio.SetMarkerStyle(8)
	ratio.SetLineColor(kBlack)
	ratio.Draw('P')
	if isinstance( ratio2, TH1 ):
		ratio2.SetFillStyle(3004)
		ratio2.SetFillColor( kRed )
		ratio2.Draw('same E2')
	line.Draw("same")
	if addUncBand:
		line11.Draw("same")
		line09.Draw("same")

	outputFileName = nameInRoot+'_'+typePlot+'_'+args.grooming+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	if not 'simple' in args.binning: outputFileName = outputFileName.replace( typePlot, typePlot+'_ResoBasedBin' )
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/101916/'+ outputFileName )
	del can


def plotDataMinusTTWJetsBkgEstimation( rootFile, dataFile, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):

	outputFileName = nameInRoot+'_all_MC_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

        dataHistos = OrderedDict()
	Data_A = dataFile.Get( nameInRoot+'__A' )
	Data_B = dataFile.Get( nameInRoot+'__B' )
	Data_C = dataFile.Get( nameInRoot+'__C' )
	Data_D = dataFile.Get( nameInRoot+'__D' )

	TTJets_A = rootFile[ 'TTJets' ][0].Get( nameInRoot+"__A" )
	TTJets_B = rootFile[ 'TTJets' ][0].Get( nameInRoot+"__B" )
	TTJets_C = rootFile[ 'TTJets' ][0].Get( nameInRoot+"__C" )
	TTJets_D = rootFile[ 'TTJets' ][0].Get( nameInRoot+"__D" )

	WJets_A = rootFile[ 'WJetsToQQ' ][0].Get( nameInRoot+"__A" )
	WJets_B = rootFile[ 'WJetsToQQ' ][0].Get( nameInRoot+"__B" )
	WJets_C = rootFile[ 'WJetsToQQ' ][0].Get( nameInRoot+"__C" )
	WJets_D = rootFile[ 'WJetsToQQ' ][0].Get( nameInRoot+"__D" )

	Data_B.Add( TTJets_B, -1 )
	Data_C.Add( TTJets_C, -1 )
	Data_D.Add( TTJets_D, -1 )

	Data_B.Add( WJets_B, -1 )
	Data_C.Add( WJets_C, -1 )
	Data_D.Add( WJets_D, -1 )

	histoBC = Data_A.Clone()
	histoBC.Reset()
	histoBC.Multiply( Data_B, Data_C, 1, 1, '' )
	
	histoBCD = Data_A.Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, Data_D, 1, 1, '' )

	histoBCD.Add( TTJets_A, 1 )
	histoBCD.Add( WJets_A )
	Bkg_A = Data_A.Clone()
	Bkg_A.Reset()
	if isinstance( rootFile, dict ):
		for bkgSam in rootFile:
			Bkg_A.Add( rootFile[ bkgSam ][0].Get( nameInRoot+'__A' ) )
	
	hRatiohBkg = ratioPlots( Bkg_A, histoBCD )
	makePlots( nameInRoot, Bkg_A, 'All MCs SR', histoBCD, 'Data ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'No_TTJets_WJets_bkg_Log', True )


def plotDataMinusTTBkgEstimation( rootFile, dataFile, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):

	outputFileName = nameInRoot+'_all_MC_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

        dataHistos = OrderedDict()
	Data_A = dataFile.Get( nameInRoot+'__A' )
	Data_B = dataFile.Get( nameInRoot+'__B' )
	Data_C = dataFile.Get( nameInRoot+'__C' )
	Data_D = dataFile.Get( nameInRoot+'__D' )
	
	print  "massAve_"+nameInRoot+"_TTJets_A"
	TTJets_A = rootFile[ 'TTJets' ][0].Get(nameInRoot+"__A" )	
	TTJets_B = rootFile[ 'TTJets' ][0].Get( nameInRoot+"__B" )
	TTJets_C = rootFile[ 'TTJets' ][0].Get( nameInRoot+"__C" )
	TTJets_D = rootFile[ 'TTJets' ][0].Get( nameInRoot+"__D" )

	Data_B.Add( TTJets_B, -1 )
	Data_C.Add( TTJets_C, -1 )
	Data_D.Add( TTJets_D, -1 )

	histoBC = Data_A.Clone()
	histoBC.Reset()
	histoBC.Multiply( Data_B, Data_C, 1, 1, '' )
	
	histoBCD = Data_A.Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, Data_D, 1, 1, '' )

	histoBCD.Add( TTJets_A, 1 )

	Bkg_A = Data_A.Clone()
	Bkg_A.Reset()
	if isinstance( rootFile, dict ):
		for bkgSam in rootFile:
			Bkg_A.Add( rootFile[ bkgSam ][0].Get( nameInRoot+'__A' ) )
	
	hRatiohBkg = ratioPlots( Bkg_A, histoBCD )
	makePlots( nameInRoot, Bkg_A, 'All MCs SR', histoBCD, 'Data ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'NoTTJetsBkg_Log', True )


def plotDataAllMCBkgEstimation( rootFile, dataFile, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):

	outputFileName = nameInRoot+'_all_MC_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

        dataHistos = OrderedDict()
	Data_A = dataFile.Get( nameInRoot+'__A' )
	Data_B = dataFile.Get( nameInRoot+'__B' )
	Data_C = dataFile.Get( nameInRoot+'__C' )
	Data_D = dataFile.Get( nameInRoot+'__D' )

	histoBC = Data_A.Clone()
	histoBC.Reset()
	histoBC.Multiply( Data_B, Data_C, 1, 1, '' )
	
	histoBCD = Data_A.Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, Data_D, 1, 1, '' )


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
	
	hRatiohBkg = ratioPlots( hBkg_A, histoBCD )
	makePlots( nameInRoot, hBkg_A, 'All MCs SR', histoBCD, 'All MC ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'DataAll_MCBkg_Log', True )

def plotMCMinusTTWJetsBkgEstimation( rootFile, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):

	outputFileName = nameInRoot+'_all_MC_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
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
		if 'TT' not in samples and 'WJets' not in samples:
			if '_B' in samples: hBkg_B.Add( bkgHistos[samples].Clone() )

	hBkg_C = bkgHistos[ bkgSam+'_C' ].Clone()
	hBkg_C.Reset()
	for samples in bkgHistos:
		if 'TT' not in samples and 'WJets' not in samples:
			if '_C' in samples: hBkg_C.Add( bkgHistos[samples].Clone() )

	hBkg_D = bkgHistos[ bkgSam+'_D' ].Clone()
	hBkg_D.Reset()
	for samples in bkgHistos:
		if 'TT' not in samples and 'WJets' not in samples:
			if '_D' in samples: hBkg_D.Add( bkgHistos[samples].Clone() )

	histoBC = hBkg_A.Clone()
	histoBC.Reset()
	histoBC.Multiply( hBkg_B, hBkg_C, 1, 1, '' )
	
	histoBCD = hBkg_A.Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, hBkg_D, 1, 1, '' )
	
	histoBCD.Add( bkgHistos[ 'TTJets_A' ], 1 )
	histoBCD.Add( bkgHistos[ 'WJetsToQQ_A' ], 1 )
	
	hRatiohBkg = ratioPlots( hBkg_A, histoBCD )
	makePlots( nameInRoot, hBkg_A, 'All MCs SR', histoBCD, 'No TTJets or WJets ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCNoTTWJetsBkg_Log', True )
	


def plotMCMinusTTBkgEstimation( rootFile, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):

	outputFileName = nameInRoot+'_all_MC_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
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
		if 'TT' not in samples:
			if '_B' in samples: hBkg_B.Add( bkgHistos[samples].Clone() )

	hBkg_C = bkgHistos[ bkgSam+'_C' ].Clone()
	hBkg_C.Reset()
	for samples in bkgHistos:
		if 'TT' not in samples:
			if '_C' in samples: hBkg_C.Add( bkgHistos[samples].Clone() )
			
	hBkg_D = bkgHistos[ bkgSam+'_D' ].Clone()
	hBkg_D.Reset()
	for samples in bkgHistos:
		if 'TT' not in samples:
			if '_D' in samples: hBkg_D.Add( bkgHistos[samples].Clone() )

	histoBC = hBkg_A.Clone()
	histoBC.Reset()
	histoBC.Multiply( hBkg_B, hBkg_C, 1, 1, '' )
	
	histoBCD = hBkg_A.Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, hBkg_D, 1, 1, '' )
	
	histoBCD.Add( bkgHistos[ 'TTJets_A' ], 1 )
	
	hRatiohBkg = ratioPlots( hBkg_A, histoBCD )
	makePlots( nameInRoot, hBkg_A, 'All MCs SR', histoBCD, 'No TTJets ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'MCNoTTBkg_Log', True )


def plotAllMCBkgEstimation( rootFile, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):

	outputFileName = nameInRoot+'_all_MC_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
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
	makePlots( nameInRoot, hBkg_A, 'All MCs SR', histoBCD, 'All MC ABCD Pred', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', 'All_MCBkg_Log', True )
            

def plotSimpleBkgEstimation( rootFile, bkg, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):

	outputFileName = nameInRoot+'_'+bkg+'_pruned_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	bkgHistos[ nameInRoot+'_'+bkg+'_A' ] = rootFile.Get( nameInRoot+'__A' )
	bkgHistos[ nameInRoot+'_'+bkg+'_B' ] = rootFile.Get( nameInRoot+'__B' )
	bkgHistos[ nameInRoot+'_'+bkg+'_C' ] = rootFile.Get( nameInRoot+'__C' )
	bkgHistos[ nameInRoot+'_'+bkg+'_D' ] = rootFile.Get( nameInRoot+'__D' )

	histoBC = bkgHistos[ nameInRoot+'_'+bkg+'_A' ].Clone()
	histoBC.Reset()
	histoBC.Multiply( bkgHistos[ nameInRoot+'_'+bkg+'_B' ], bkgHistos[ nameInRoot+'_'+bkg+'_C' ], 1, 1, '')
	histoBCD = bkgHistos[ nameInRoot+'_'+bkg+'_A' ].Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, bkgHistos[ nameInRoot+'_'+bkg+'_D' ], 1, 1, '')

	hRatiohBkg = ratioPlots( bkgHistos[ nameInRoot+'_'+bkg+'_A' ], histoBCD ) 
	makePlots( nameInRoot, bkgHistos[ nameInRoot+'_'+bkg+'_A' ], bkg+' SR', histoBCD, bkg+' MC ABCD Pred.', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', bkg+'Bkg_Log', True)
	



def plot2DBkgEstimation( rootFile, sample, Groom, nameInRoot, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY ):
	"""docstring for plot"""

	outputFileName = nameInRoot+'_'+sample+'_'+Groom+'_'+args.RANGE+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	if isinstance(rootFile, dict):
		for bkg in rootFile:
			bkgHistos[ bkg+'_A' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__A' ), rebinx, rebiny )
			bkgHistos[ bkg+'_B' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__B' ), rebinx, rebiny )
			bkgHistos[ bkg+'_C' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__C' ), rebinx, rebiny )
			bkgHistos[ bkg+'_D' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__D' ), rebinx, rebiny )

		hBkg = bkgHistos[ bkg+'_B' ].Clone()
		hBkg.Reset()
		for samples in bkgHistos:
			print samples
			hBkg.Add( bkgHistos[ samples ].Clone() )
	else: 
		print nameInRoot+'__A'
		bkgHistos[ sample+'_A' ] = Rebin2D( rootFile.Get( nameInRoot+'__A' ), rebinx, rebiny )
		bkgHistos[ sample+'_B' ] = Rebin2D( rootFile.Get( nameInRoot+'__B' ), rebinx, rebiny )
		bkgHistos[ sample+'_C' ] = Rebin2D( rootFile.Get( nameInRoot+'__C' ), rebinx, rebiny )
		bkgHistos[ sample+'_D' ] = Rebin2D( rootFile.Get( nameInRoot+'__D' ), rebinx, rebiny )

		hBkg = bkgHistos[ sample+'_B' ].Clone()
		for samples in bkgHistos:
			if sample+'_B' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )

	if 'DATA' in sample: CMS_lumi.extraText = "Preliminary"
	else: CMS_lumi.extraText = "Simulation Preliminary"
	hBkg.GetXaxis().SetTitle( titleXAxis )
	hBkg.GetYaxis().SetTitleOffset( 0.9 )
	hBkg.GetYaxis().SetTitle( titleXAxis2 )
	corrFactor = hBkg.GetCorrelationFactor()
	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextFont(62) ### 62 is bold, 42 is normal
	textBox.SetTextAlign(31)

	if (Xmax or Ymax):
		hBkg.GetXaxis().SetRangeUser( Xmin, Xmax )
		hBkg.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	hBkg.SetMaximum( 1500 )
	hBkg.SetMinimum( 0.01 )
	can = TCanvas('c1', 'c1',  750, 500 )
	can.SetLogz()
	hBkg.Draw('colz')
	textBox.DrawLatex(0.85, 0.85, ( 'M_{#tilde{t}} = '+args.mass+' GeV' if 'RPV' in sample else sample ) )
	textBox1 = textBox.Clone()
	textBox1.DrawLatex(0.85, 0.8, 'Corr. Factor = '+str(round(corrFactor,2)))
	textBox2 = textBox.Clone()
	textBox2.SetTextSize(0.12)
	textBox2.DrawLatex(0.27, 0.30, 'B  D')
	textBox3 = textBox.Clone()
	textBox3.SetTextSize(0.12)
	textBox3.DrawLatex(0.27, 0.15, 'A  C')

	xline = array('d', [0,1])
	yline = array('d', [1.0, 1.0])
	line = TGraph(2, xline, yline)
	line.SetLineColor(kBlack)
	line.SetLineWidth(5)
	line.Draw("same")
	xline2 = array('d', [0.1,0.1])
	yline2 = array('d', [0, 5])
	line2 = TGraph(2, xline2, yline2)
	line2.SetLineColor(kBlack)
	line2.SetLineWidth(5)
	line2.Draw("same")

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)

	can.SaveAs( 'Plots/101916/'+outputFileName )
	del can

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

	bkgFiles = OrderedDict() 
	signalFiles = {}
#	dataFile = TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_DATA_'+args.RANGE+'_'+args.version+'.root')
	signalFiles[ 'Signal' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_'+args.RANGE+'_'+args.version+'.root'), 1, args.decay+' RPV #tilde{t} '+str(args.mass)+' GeV', kRed-4]
	bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_TTJets_'+args.RANGE+'_'+args.version+'.root'),	1, 't #bar{t} + Jets', kGreen ]
    	bkgFiles[ 'ZJetsToQQ' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_ZJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'Z + Jets', kOrange]
    	bkgFiles[ 'WJetsToQQ' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_WJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'W + Jets', kMagenta ]
	bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_WWTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1 , 'WW (had)', kMagenta+2 ]
	bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_ZZTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1, 'ZZ (had)', kOrange+2 ]
	bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_WZ_'+args.RANGE+'_'+args.version+'.root'), 1, 'WZ', kCyan ]
	bkgFiles[ 'QCD'+args.qcd+'All' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_QCD'+args.qcd+'All_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]
	#bkgFiles[ 'QCDPtAll' ] = [ TFile.Open('Rootfiles/101816/RUNBkgEstimationUDD323_'+args.grooming+'_QCDPtAll_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]


	massMinX = 0
	massMaxX = 510
	jetMassHTlabY = 0.20
	jetMassHTlabX = 0.85

	if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Groommers = [ args.grooming ]

	for optGroom in Groommers:
		if '2D' in args.proc: 
			for bkg in bkgFiles: plot2DBkgEstimation( bkgFiles[ bkg ][0], bkg, optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
#			plot2DBkgEstimation( dataFile, 'DATA', optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
#			for bkg in bkgFiles: plot2DBkgEstimation( bkgFiles, bkg, optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
#			for bkg in signalFiles: plot2DBkgEstimation( signalFiles[ bkg ][0], 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass), optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)

		elif 'simple' in args.proc:
			for bkg in bkgFiles: 
				plotSimpleBkgEstimation( bkgFiles[ bkg ][0], bkg, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
#			plotSimpleBkgEstimation( dataFile, 'DATA', 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
		elif 'AllMCBkg' in args.proc:
			plotAllMCBkgEstimation( bkgFiles, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )			
#		elif 'DataAndMC' in args.proc:
#			plotDataAllMCBkgEstimation( bkgFiles, dataFile, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
#		elif 'DataMinusTT' in args.proc:
#			plotDataMinusTTBkgEstimation( bkgFiles, dataFile, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
#		elif 'DataMinusWTT' in args.proc:
#			plotDataMinusTTWJetsBkgEstimation( bkgFiles, dataFile, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
		elif 'MCMinusTT' in args.proc:
			plotMCMinusTTBkgEstimation( bkgFiles, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
		elif 'MCMinusWTT' in args.proc:
			plotMCMinusTTWJetsBkgEstimation( bkgFiles, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
		elif 'TransferFunction' in args.proc:
			transfun = TransferFunction()
			transfun.bkgEstFunction( bkgFiles, 'massAve_prunedMassAsymVsdeltaEtaDijet', 0, massMaxX, 5, '', '', False )
