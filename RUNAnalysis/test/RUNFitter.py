#!/usr/bin/env python

###################
### Make Fitting
###################

#from ROOT import RooRealVar, RooDataHist, RooArgList, RooArgSet, RooAddPdf, RooFit, RooGenericPdf, RooWorkspace, RooMsgService, RooHistPdf
from ROOT import *
from array import array
import argparse
import glob,sys, os
import warnings
import random
import numpy as np
from multiprocessing import Process
try: 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python') 
	import CMS_lumi as CMS_lumi 
	from scaleFactors import * #scaleFactor as SF
	from histoLabels import labels, labelAxis 
	import tdrstyle as tdrstyle

gSystem.SetIncludePath('-I$ROOFITSYS/include')
if os.access('RooPowerFunction.cxx', os.R_OK): ROOT.gROOT.ProcessLine('.L RooPowerFunction.cxx+')

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
CMS_lumi.writeExtraText = 1
TVirtualFitter.SetMaxIterations(50000000)		######### Trick to increase number of iterations

gStyle.SetOptFit()
gStyle.SetStatY(0.91)
gStyle.SetStatX(0.95)
gStyle.SetStatW(0.15)
gStyle.SetStatH(0.15) 
gStyle.SetTextSize(0.5)

xline = array('d', [0,2000])
yline = array('d', [0,0])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

######## Fit Functions
P4 = TF1("P4", "[0]* TMath::Power(1-(x/13000.0),[1]) / (TMath::Power(x/13000.0,[2]+([3]*log(x/13000.))))",0,2000);
P3 = TF1("P3", "[0]* TMath::Power(1-(x/13000.0),[1]) / (TMath::Power(x/13000.0,[2]))",0,2000);
P1 = TF1("P1", "[0] / (TMath::Power(x/13000.0,[1]))",0,2000);
#expoPoli = TF1("expoPoli", "exp([0]+[1]*x+[2]*x*x)", 0, 2000 )
expoPoli = TF1("expoPoli", "exp([0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x)", 0, 1000 )
landau = TF1("landau","[0]*TMath::Landau(-x,[1],[2])",0,2000)
gaus = TF1("gaus", "gaus", 0, 2000);
P4Gaus = TF1("P4Gaus", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))+gaus(4)",0,2000);
massBins = [0, 30, 60, 90, 120, 150, 180, 210, 250, 290, 330, 370, 410, 460, 510, 560, 610, 670, 730, 790, 860, 930, 1000, 1080, 1160, 1240, 1330, 1420, 1520, 1620, 1730, 1840, 2000]

def createPseudoExperiment():
	"""docstring for createPseudoExperiment"""
	h1 = inFileBkg.Get(hist)
	binSize = h1.GetBinWidth(1)
	P4PSE = TF1("P4PSE", "[0]*pow(1-x/13000.0,[1])/pow(x/13000.0,[2]+[3]*log(x/13000.))", minX, maxX);
	P4PSE.SetParameter(0,bkgParameters[0])				
	P4PSE.SetParameter(1,bkgParameters[1])
	P4PSE.SetParameter(2,bkgParameters[2])
	P4PSE.SetParameter(3,bkgParameters[3])
	randomNumEventsQCD = random.randint( bkgParameters[4]-round(sqrt(bkgParameters[4])), bkgParameters[4]+round(sqrt(bkgParameters[4])) )
	print "randomNumberOf QCD events", randomNumEventsQCD
	hMainPSE = TH1D("hbkgPSE", "hbkgPSE", int( (maxX-minX)/binSize ) , minX, maxX)
	hMainPSE.FillRandom( "P4PSE", int(randomNumEventsQCD) )
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	c1.SetLogy()
	gStyle.SetOptFit()
	gStyle.SetStatY(0.94)
	gStyle.SetStatX(0.9)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.15) 
	hMainPSE.GetXaxis().SetTitle( histYaxis )
	hMainPSE.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	hMainPSE.GetYaxis().SetTitleOffset(1.2);
	hMainPSE.SetTitle("QCD PseudoExperiments")
	hMainPSE.Sumw2()
	hMainPSE.Draw()
	c1.SaveAs(outputDir+hist+"_PseudoExperiment_Fit_ResolvedAnalysis_"+args.version+"."+args.extension)
	del c1

def rootFitter( inFile, hist, scale, fitFunction, fitParam, minX, maxX, rebinX, plot, log=True ):
	"""Simple rootFitter"""

	tmpBinContent = []
	tmpBinError = []
	minBinX = int(minX/(rebinX if args.miniTree else rebinX*10 ))+1
	maxBinX = int(maxX/(rebinX if args.miniTree else rebinX*10 ))+1

	rawHisto = inFile.Get( hist )
	rawHisto.SetBinErrorOption(TH1.kPoisson)
	rawHisto.Scale( scale )
	rawHisto.Rebin( rebinX )
	#rawHisto.Scale( 1/rawHisto.Integral() )
	numEvents = rawHisto.Integral( int((args.mass-50)/rebinX)+1, int((args.mass+50/rebinX)+1) ) #minBinX, maxBinX )
	print "|----> Number of events", numEvents, 'out of', rawHisto.Integral( )

	print '|----> Creating histograms from bin', minBinX, '(', rawHisto.GetBinLowEdge(minBinX),') to ', maxBinX, '(', rawHisto.GetBinLowEdge(maxBinX),')'
	for ibin in range( minBinX, maxBinX ):
		tmpBinContent.append( rawHisto.GetBinContent(ibin) / rebinX )
		tmpBinError.append( rawHisto.GetBinError(ibin) / rebinX )
		#print rawHisto.GetBinLowEdge( ibin ), rawHisto.GetBinContent(ibin) , rebinX, rawHisto.GetBinError(ibin)

	binContents = np.array(tmpBinContent)
	binError = np.array(tmpBinError)
	#print '|----> bins NO normalized:', tmpBinContent
	#sumBinContents = np.sum(binContents)
	#binContents = binContents/sumBinContents
	#binError = binError/sumBinContents		####################### CHECK THE STUPID ERRORS!!!!
	print '|----> bins :', binContents
	print '|----> bins error :', binError
	
	numBins = maxBinX - minBinX
	finalHisto = TH1D("finalHisto", "finalHisto", numBins, minX, maxX)
	finalHisto.Sumw2()
	for ibin in range( 0, numBins ):
		finalHisto.SetBinContent( ibin+1, binContents[ibin] )
		finalHisto.SetBinError( ibin+1, binError[ibin] )


	if( len(fitParam)>0 ):
		for k in range( len(fitParam) ): fitFunction.SetParameter(k, fitParam[k])

	fitStatus = 0
	numParam = 0
	for loop in range(0,5):
		#result = finalHisto.Fit(fitFunction,"MIRS","",minX,maxX)
		result = finalHisto.Fit( fitFunction,"ELLSR","",minX,maxX)
		#fitStatus = int(result.Status())
		numParam = result.NFreeParameters()
		#print "|----> Fit status : %d" % fitStatus
		#if(fitStatus==1):
		#	stopProgram=0
		#	result.Print("V")
		#	break

	fitParameters =  [ fitFunction.GetParameter(k) for k in range( numParam ) ]
	fitParErrors =  [ fitFunction.GetParError(k) for k in range( numParam ) ]
	print "|----> Fitter parameters for", fitFunction.GetName(), fitParameters, fitParErrors

	######### Plotting Histograms
	if plot:
		c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
		if log: c1.SetLogy()
		finalHisto.GetXaxis().SetTitle( histYaxis )
		finalHisto.GetYaxis().SetTitle('dN/dm_{av} / '+str(round(rebinX))+' GeV' ) 
		finalHisto.GetYaxis().SetTitleOffset(0.9);
		finalHisto.GetXaxis().SetRangeUser( minX-50, maxX+50 )
		finalHisto.SetTitle("")
		finalHisto.Draw()
		c1.SaveAs(outputDir+hist.replace('ResolvedAnalysisPlotsMassPairing/','')+"_"+args.process+"_"+fitFunction.GetName()+"Fit_ResolvedAnalysis_"+args.version+"."+args.extension)
		del c1
	
	return [ fitParameters, fitParErrors, numEvents, binContents, binError ]




def histoFunctionFit( nameHisto, initFitFunction, parameters, parErrors, massBin, massBinErr, minX, maxX ):
	"""docstring for histoFunctionFit"""

	#p4Function = TF1("p4Function", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))", minX, maxX)
	fitFunction = initFitFunction.Clone()
	for i in range(0, initFitFunction.GetNpar() ): 
		fitFunction.SetParameter( i, parameters[i] )
		fitFunction.SetParError( i, parErrors[i] )

	histoFit = TH1D( nameHisto, nameHisto, len(massBin) , minX, maxX)
	histoFit.Sumw2()

	for ibin in range( 0, len(massBin)):
		histoFit.SetBinContent( ibin, massBin[ibin] )
		histoFit.SetBinError( ibin, massBinErr[ibin] )
			
	histoFit.Fit( fitFunction, "MIR", "", minX, maxX )

	return histoFit, fitFunction





def FitterCombination( inFileData, inFileBkg, inFileSignal, hist, scale, bkgFunction, fitParam, minX, maxX, rebinX, runData ):
	"""docstring for FitterCombination"""

	### Fit QCD MC
	print "|----> Fitting MC QCD"
	BkgParameters = rootFitter( inFileBkg, hist+('QCD'+args.qcd+'All' if args.miniTree else ''), scale*( 1 if args.miniTree else 0.75 ), bkgFunction.Clone(), fitParam, minX, maxX, rebinX, True )
	bkgParameters = BkgParameters[0]
	bkgParErrors = BkgParameters[1]
	bkgAcceptance = BkgParameters[2]
	bkgpoints = BkgParameters[3]
	bkgpointsErr = BkgParameters[4]

#	SigParameters = rootFitter( inFileSignal, hist, scale, gaus, [], args.mass-50, args.mass+50, rebinX, False )
#	gausParameters = SigParameters[0]
#	sigAcceptance = SigParameters[1]
#	sigContent = SigParameters[2]
#	sigErr = SigParameters[3]
	
	legend=TLegend(0.18,0.15,0.50,0.35)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	if runData:
		print "|----> Fitting Data"
		DataParameters = rootFitter( inFileData, hist+('JetHT_Run2016' if args.miniTree else ''), 1, bkgFunction.Clone(), bkgParameters, minX, maxX, rebinX, False )
		#DataParameters = rootFitter( inFileData, hist+('QCDHerwigAll' if args.miniTree else ''), scale, bkgFunction, bkgParameters, minX, maxX, rebinX, False )
		dataParameters = DataParameters[0]
		dataParErrors = DataParameters[1]
		dataAcceptance = DataParameters[2]
		points = DataParameters[3]
		pointsErr = DataParameters[4]
		hMain, mainP4 = histoFunctionFit( 'Data', bkgFunction, dataParameters, dataParErrors, points, pointsErr, minX, maxX )
		legend.AddEntry( hMain, 'Data', 'ep' )
		legend.AddEntry( mainP4, 'Fit to data', 'l' )
		hMCQCD, qcdMCP4 = histoFunctionFit( 'QCD'+args.qcd+'All', bkgFunction, bkgParameters, bkgParErrors, bkgpoints, bkgpointsErr, minX, maxX )
		legend.AddEntry( qcdMCP4, 'Fit to MC QCD pythia', 'l' )

		if isinstance( inFileSignal, TFile):
			Bkg2Parameters = rootFitter( inFileSignal, hist+'QCDHerwigAll', scale, bkgFunction, fitParam, minX, maxX, rebinX, True )
			#Bkg2Parameters = rootFitter( inFileSignal, hist+'QCDHTAll', scale, bkgFunction, fitParam, minX, maxX, rebinX, True )
			bkg2Parameters = Bkg2Parameters[0]
			bkg2ParErrors = Bkg2Parameters[1]
			bkg2Acceptance = Bkg2Parameters[2]
			bkg2points = Bkg2Parameters[3]
			bkg2pointsErr = Bkg2Parameters[4]
			hBkg2, qcdHTMCP4 = histoFunctionFit( 'QCDHerwig', bkgFunction, bkg2Parameters, bkg2ParErrors, bkg2points, bkg2pointsErr, minX, maxX )
			#hBkg2, qcdHTMCP4 = histoFunctionFit( 'QCDHT', bkg2Parameters, bkg2points, bkg2pointsErr, minX, maxX )
			legend.AddEntry( qcdHTMCP4, 'Fit to MC QCD powheg', 'l' )
			#legend.AddEntry( qcdHTMCP4, 'Fit to MC QCD madgraph+pythia', 'l' )

	else:
		hMain, mainP4 = histoFunctionFit( 'QCD'+args.qcd+'All', bkgFunction, bkgParameters, bkgParErrors, bkgpoints, bkgpointsErr, minX, maxX )
		points = bkgpoints
		pointsErr = bkgpointsErr
	
	print '|----> DATA Plotted:', points
	print '|----> DATA Err:', pointsErr

	hPull = TH1D("hpull", "hpull", len(points) , minX, maxX)
	hPull.Sumw2()
	hResidual = TH1D("hresidual", "hresidual", len(points) , minX, maxX)
	hResidual.Sumw2()

	'''
	for ibin in range( 0, len(points)):
		hMain.SetBinContent( ibin, points[ibin] )
		hMain.SetBinError( ibin, pointsErr[ibin] )
			
	#hMain.Fit( mainP4, "ELLSR", "", minX, maxX )
	hMain.Fit( mainP4, "MIR", "", minX, maxX )
	P4Gaus.SetParameter(0,bkgParameters[0])				
	P4Gaus.SetParameter(1,bkgParameters[1])
	P4Gaus.SetParameter(2,bkgParameters[2])
	P4Gaus.SetParameter(3,bkgParameters[3])
	P4Gaus.SetParameter(4,gausParameters[0])
	P4Gaus.SetParameter(5,gausParameters[1])
	P4Gaus.SetParameter(6,gausParameters[2])
	hMain.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	hMain.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	hMain.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	P4_2 = TF1("P4_2", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))", minX, maxX);
	#P4_2.SetParameter(0, P4Gaus.GetParameter(0) )
	#P4_2.SetParameter(1, P4Gaus.GetParameter(1) )
	#P4_2.SetParameter(2, P4Gaus.GetParameter(2) )
	#P4_2.SetParameter(3, P4Gaus.GetParameter(3) )
	P4_2.SetParameter(0,bkgParameters[0])				
	P4_2.SetParameter(1,bkgParameters[1])
	P4_2.SetParameter(2,bkgParameters[2])
	P4_2.SetParameter(3,bkgParameters[3])

	#gaus2.SetParameter(0, P4Gaus.GetParameter(4) )
	#gaus2.SetParameter(1, P4Gaus.GetParameter(5) )
	#gaus2.SetParameter(2, P4Gaus.GetParameter(6) )
	#print "SIGNALLLL", gaus2.Integral(args.mass-30, args.mass+30)
	#P4_2Parameters = [ P4_2.GetParameter(0), P4_2.GetParameter(1), P4_2.GetParameter(2), P4_2.GetParameter(3), P4Gaus.GetParameter(4), P4Gaus.GetParameter(5), P4Gauss.GetParameter(6), bkgAcceptance, sigAcceptance, minX, maxX ]
	#print P4_2Parameters
	'''


	######## Calculating Pull and Residual
	chi2 = 0 
	nof = 0
	for ibin in range(0, len(points) ):
	
		binCont = points[ibin]
		binErr = pointsErr[ibin]
		valIntegral = mainP4.Eval( hMain.GetBinCenter(ibin) ) 
		diff = (binCont - valIntegral)/ valIntegral
		#errDiff = diff * TMath.Sqrt( TMath.Power( P4Gaus.GetParError(0) / P4Gaus.GetParameter(0),2 ) + TMath.Power( P4Gaus.GetParError(1)/ P4Gaus.GetParameter(1), 2 )  + TMath.Power( P4Gaus.GetParError(2)/ P4Gaus.GetParameter(2), 2 )  + TMath.Power( P4Gaus.GetParError(3)/ P4Gaus.GetParameter(3), 2 ) )
		#errDiff = diff * TMath.Sqrt( TMath.Power( mainP4.GetParError(0) / mainP4.GetParameter(0),2 ) + TMath.Power( mainP4.GetParError(1)/ mainP4.GetParameter(1), 2 )  + TMath.Power( mainP4.GetParError(2)/ mainP4.GetParameter(2), 2 )  + TMath.Power( mainP4.GetParError(3)/ mainP4.GetParameter(3), 2 ) )
		#print binCont, binErr, valIntegral 

		if (binCont != 0):
			pull = (binCont - valIntegral)/ binErr
			chi2 += TMath.Power(pull,2)
			nof += 1
			
			hPull.SetBinContent(ibin, pull)
			hPull.SetBinError(ibin, 1.0)
	
			hResidual.SetBinContent(ibin, diff)
			hResidual.SetBinError(ibin, binErr/valIntegral )
	print '|----> ############### chi2 and nof: ', chi2, nof


	######### Plotting Histograms
	maxXPlot = maxX+500
	tdrStyle.SetPadRightMargin(0.05)
  	tdrStyle.SetPadLeftMargin(0.15)
	gStyle.SetOptFit()
	gStyle.SetStatY(0.91)
	gStyle.SetStatX(0.95)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.30) 
	#c3 = TCanvas('c1', 'c1',  10, 10, 750, 1000 )
	#pad1 = TPad("pad1", "Fit",0,0.40,1.00,1.00,-1)
	#pad2 = TPad("pad2", "Pull",0,0.25,1.00,0.475,-1);
	#pad3 = TPad("pad3", "Residual",0,0,1.00,0.277,-1);
	c3 = TCanvas('c1', 'c1',  10, 10, 1250, 500 )
	pad1 = TPad("pad1", "Fit",0,0.00,0.50,1.00,-1)
	pad2 = TPad("pad2", "Pull",0.50,0.50,1.00,1.00,-1);
	pad3 = TPad("pad3", "Residual",0.50,0,1.00,0.557,-1);
	pad1.Draw()
	pad2.Draw()
	pad3.Draw()

	pad1.cd()
	pad1.SetLogy()
	hMain.SetMarkerStyle(8)
	hMain.GetYaxis().SetTitle("dN/dm_{av} / "+ str(hMain.GetBinWidth(1)) +" GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	hMain.GetXaxis().SetTitle( histYaxis )
	hMain.GetYaxis().SetTitleOffset(1.2);
	hMain.SetTitle("")
	#hMain.SetMaximum( 1.5 * hMain.GetMaximum() )
	hMain.Draw()
	hMain.GetXaxis().SetRangeUser( minX, maxXPlot  )
	mainP4.SetLineColor(kBlack)
	mainP4.Draw("same")
	#gaus2.SetLineColor(kRed-4)
	#gaus2.Draw("same")
	mainP4.SetLineColor(kBlue-4)
	mainP4.Draw("same")
	if runData:
		qcdMCP4.SetLineColor( kMagenta )
		qcdMCP4.Draw("same")	
		if isinstance( inFileSignal, TFile):
			qcdHTMCP4.SetLineColor( kViolet )
			qcdHTMCP4.Draw("same")	
		legend.Draw("same")
	CMS_lumi.relPosX = 0.13
	CMS_lumi.cmsTextSize = 0.60
	CMS_lumi.lumiTextSize = 0.50
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	#labels( hist, '', '', 0.20, 0.45, 'left' )


	pad2.cd()
	pad2.SetGrid()
	#pad2.SetTopMargin(0)
	gStyle.SetOptStat(0)
	hPull.GetYaxis().SetTitle("#frac{(Data - Fit)}{#sigma_{Data}}")
	hPull.GetYaxis().SetLabelSize(0.08)
	hPull.GetYaxis().SetTitleSize(0.09)
	hPull.GetYaxis().SetTitleOffset(0.70)
	hPull.GetYaxis().CenterTitle()
	hPull.SetMarkerStyle(7)
	#hPull.SetMaximum(3)
	hPull.GetXaxis().SetRangeUser( minX, maxXPlot )
	hPull.Sumw2()
	hPull.Draw("e")
	line.Draw("same")
	
	pad3.cd()
	pad3.SetGrid()
	pad3.SetTopMargin(0)
	pad3.SetBottomMargin(0.3)
	gStyle.SetOptStat(0)
	hResidual.GetXaxis().SetTitle( histYaxis )
	hResidual.GetYaxis().SetTitle("#frac{(Data - Fit)}{Fit}")
	hResidual.GetXaxis().SetTitleSize(0.10)
	hResidual.GetXaxis().SetLabelSize(0.07)
	hResidual.GetYaxis().SetLabelSize(0.07)
	hResidual.GetYaxis().SetTitleSize(0.08)
	hResidual.GetYaxis().SetTitleOffset(0.80)
	hResidual.GetYaxis().CenterTitle()
	hResidual.SetMarkerStyle(7)
	hResidual.SetMaximum(0.59)
	hResidual.SetMinimum(-0.59)
	hResidual.GetXaxis().SetRangeUser( minX, maxXPlot )
	#hResidual.Sumw2()
	hResidual.Draw("e")
	line.Draw("same")
	c3.SaveAs("Plots/"+hist.replace('ResolvedAnalysisPlotsMassPairing/','')+"_"+args.process+"_"+args.version+"Fit"+bkgFunction.GetName()+"_ResolvedAnalysis_"+args.version+"."+args.extension)
	del c3

	fitParameters =  [ mainP4.GetParameter(k) for k in range( 0, 5) ]
	fitParErrors =  [ mainP4.GetParError(k) for k in range( 0, 5 ) ]

	return [ fitParameters, fitParErrors, (dataAcceptance if runData else ''), points, pointsErr ] 

def createCards( dataFile, bkgFile, inFileSignal, hist, scale, bkgFunction, minX, maxX, rebinX ):
	"""function to run Roofit and save workspace for RooStats"""
	
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )

	print '|----> Background'
	bkgFuncParameters = FitterCombination( dataFile, bkgFile, '', hist, scale, bkgFunction, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX, True )
	#bkgFuncParameters = rootFitter( bkgFile, hist+('QCD'+args.qcd+'All' if args.miniTree else ''), scale, bkgFunction, [ 0.1, 100, 2, 0.1 ], minX, maxX, rebinX, True)
	#bkgFuncParameters = rootFitter( dataFile, hist+('JetHT_Run2016' if args.miniTree else ''), 1, bkgFunction, [ 0.1, 100, 2, 0.1 ], minX, maxX, rebinX, True )

	#hData = dataFile.Get( hist+('JetHT_Run2016C' if args.miniTree else '') )
	hData = TH1D("hData", "hData", len(bkgFuncParameters[3]) , minX, maxX)
	hData.Sumw2()
	for ibin in range(0, len( bkgFuncParameters[3] ) ):
		hData.SetBinContent( ibin+1, bkgFuncParameters[3][ibin] )
		hData.SetBinError( ibin+1, bkgFuncParameters[4][ibin] )

	p1 = RooRealVar('p1','p1',bkgFuncParameters[0][1], -abs(bkgFuncParameters[0][1])*100, abs(bkgFuncParameters[0][1])*100) 
	p2 = RooRealVar('p2','p2',bkgFuncParameters[0][2], -abs(bkgFuncParameters[0][2])*100, abs(bkgFuncParameters[0][2])*100)
	p3 = RooRealVar('p3','p3',bkgFuncParameters[0][3], -abs(bkgFuncParameters[0][3])*100, abs(bkgFuncParameters[0][3])*100)
	#p1.setConstant()
	#p2.setConstant()
	#p3.setConstant()
	sqrtS = 13000

	if ( args.mass > 0 ): listMass = [ args.mass ]
	else: listMass = range( 300, 700, 50 )

	for imass in listMass:

		print '|----> Signal'
		SignalParameters = rootFitter( TFile.Open( inFileSignal.replace( str(args.mass), str(imass) ) ), hist+('RPVStopStopToJets_UDD312_M-'+str(imass) if args.miniTree else ''), scale, gaus, '', imass-100, imass+100, rebinX, True )

		massWindow = int(SignalParameters[0][2])*2
		mass = RooRealVar( 'mass', 'mass', imass-massWindow, imass+massWindow )

		sigMean = RooRealVar('sigMean', 'sigMean', imass )
		sigSigma = RooRealVar('sigSigma', 'sigSigma', SignalParameters[0][2] )
		#sigMean.setConstant()
		#sigSigma.setConstant()
		signal = RooGaussian( 'signal', 'signal', mass, sigMean, sigSigma )
		signal.Print()

		signalGaus = TF1( "RPVStop"+str(imass), "gaus", imass-massWindow, imass+massWindow )
		signalGaus.SetParameter( 0, SignalParameters[0][0] ) 
		signalGaus.SetParameter( 1, imass ) 
		signalGaus.SetParameter( 2, SignalParameters[0][2] ) 
		sigAcc = round( signalGaus.Integral( imass-massWindow, imass+massWindow ), 2 )
		#sigAcc = int ( np.sum( SignalParameters[3][ (( imass - minX - 50 )/(rebinX*(1 if args.miniTree else 10))): (( imass - minX + 50 )/(rebinX*(1 if args.miniTree else 10))+1 ) ] ) )
		print '|----> Signal events:', sigAcc

		#hBkg = inFileBkg.Get(hist)
		#hData = hBkg.Clone()
		#hData.Add( hSignal )

		tmpBkgFunct = bkgFunction.Clone()
		for p in range( 0, len( bkgFuncParameters[0] )): tmpBkgFunct.SetParameter( p, bkgFuncParameters[0][p] )
		bkgAcc = round( tmpBkgFunct.Integral( imass-massWindow, imass+massWindow ), 2 )
		#bkgAcc = int( np.sum( bkgFuncParameters[3][ (( imass - minX - 50 )/(rebinX*(1 if args.miniTree else 10))): (( imass - minX + 50 )/(rebinX*(1 if args.miniTree else 10))+1 ) ] ) ) 
		print '|----> Background events in mass (', imass, '):', bkgAcc
	
		background = RooGenericPdf('background','(pow(1-@0/13000,@1)/pow(@0/13000,@2+@3*log(@0/13000)))',RooArgList(mass,p1,p2,p3))
		background.Print()

		# S+B model
		#signal_norm = RooRealVar( 'signal_norm', 'signal_norm', sigAcc, 0, 20.*TMath.Sqrt(sigAcc))
		#signal_norm = RooRealVar( 'signal_norm', 'signal_norm', sigAcc, 0, 10000000000 ) #+(20.*TMath.Sqrt(sigAcc)))
		#signal_norm.setConstant()
		#signal_norm.Print()
		#background_norm = RooRealVar('background_norm','background_norm', bkgAcc, 0., 20.*TMath.Sqrt(bkgAcc))
		#background_norm.Print()
		#model = RooAddPdf("model","s+b",RooArgList(background,signal),RooArgList(background_norm,signal_norm))

		rooDataHist = RooDataHist('data_obs','data_obs',RooArgList(mass),hData)
		rooDataHist.Print()

		#res = model.fitTo(rooDataHist, RooFit.Save(kTRUE), RooFit.Strategy(0), RooFit.SumW2Error(kFALSE))
		#res.Print()

		outputRootFile = '/afs/cern.ch/work/a/algomez/RPVStops/CMSSW_8_0_20/src/RUNA/RUNStatistics/test/Rootfiles/workspace_RPVStopStopToJets_UDD312_M-'+str(imass)+'_Resolved_'+args.cut+'_'+args.version+'.root' 
		myWS = RooWorkspace("myWS")
		getattr(myWS,'import')(signal)
		getattr(myWS,'import')(background, RooCmdArg())
		getattr(myWS,'import')(rooDataHist) 
		myWS.Print()
		myWS.writeToFile(outputRootFile, True)
		print '|----> Workspace created:', outputRootFile
	 # -----------------------------------------
		# write a datacard

		datacard = open('/afs/cern.ch/work/a/algomez/RPVStops/CMSSW_8_0_20/src/RUNA/RUNStatistics/test/Datacards/datacard_RPVStopStopToJets_UDD312_M-'+str(imass)+'_Resolved_'+args.cut+'_'+args.version+'.txt','w')
		datacard.write('imax 1\n')
		datacard.write('jmax 1\n')
		datacard.write('kmax *\n')
		datacard.write('---------------\n')
		datacard.write("shapes * * "+outputRootFile+" myWS:$PROCESS \n")
		datacard.write('---------------\n')
		datacard.write('bin 1\n')
		datacard.write('observation -1\n')
		datacard.write('------------------------------\n')
		datacard.write('bin          1          1\n')
		datacard.write('process      signal     background\n')
		datacard.write('process      0          1\n')
		datacard.write('rate         '+str(sigAcc)+'      '+str(bkgAcc)+'\n')
		#datacard.write('rate	     1		1\n')
		datacard.write('------------------------------\n')
		datacard.write('p1  param	'+str(bkgFuncParameters[0][1])+'	'+str(bkgFuncParameters[1][1])+'\n')
		datacard.write('p2  param	'+str(bkgFuncParameters[0][2])+'	'+str(bkgFuncParameters[1][2])+'\n')
		datacard.write('p3  param	'+str(bkgFuncParameters[0][3])+'	'+str(bkgFuncParameters[1][3])+'\n')
		#flat parameters --- flat prior
		datacard.write('p1  flatParam\n')
		datacard.write('p2  flatParam\n')
		datacard.write('p3  flatParam\n')
		datacard.close()
		print '|----> Datacard created:', datacard

def rooFitter( dataFile, bkgFile, inFileSignal, hist, scale, P4, minX, maxX, rebinX ):

	myWS = RooWorkspace("myWS")
	''' CONFIG FOR 732 WORKS PERFECT
	x = RooRealVar( "x", "x", 50., 190. )
	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[50,190],p1[2116,2117],p2[-62,63],p3[-5,-4]})")
	myWS.factory("Gaussian:sig_pdf(x, mean[93,94], sigma[5,6])")
	myWS.factory("SUM:model(nsig[0,100000]*sig_pdf, nbkg[0,1000000]*bkg_pdf)")
	myWS.factory("SUM:model_b(nbkg[0,1000000]*bkg_pdf)")

	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[70,600], p1[-4000,4000],p2[-300,300],p3[0,40]})")

	'''

	myWS.factory("x["+str(P4GausParameters[7])+","+str(P4GausParameters[8])+"]")
	bins = (P4GausParameters[8]-P4GausParameters[7])/10
	myWS.var("x").setBins(int(bins))
	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1["+str(P4GausParameters[1])+"],p2["+str(P4GausParameters[2])+"],p3["+str(P4GausParameters[3])+"]})")
	#myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1[-2000,1000],p2[-200,200],p3[-20,20]})")
	#myWS.factory("Gaussian:sig_pdf(x, mean["+str(args.mass)+"], sigma[0,10])")
	myWS.factory("Gaussian:sig_pdf(x, mean["+str(P4GausParameters[5])+"], sigma["+str(P4GausParameters[6])+"])")
	#myWS.factory("Gaussian:sig_pdf(x, mean[93.29], sigma[5.52])")
	#myWS.factory("Gaussian:sig_pdf(x, mean[90,100], sigma[0,10])")
	myWS.factory("SUM:model_bkg( nbkg[0,100000]*bkg_pdf )")
	#myWS.factory("SUM:model_sig( nsig[0,10000]*sig_pdf )")
	myWS.factory("SUM:model( nbkg[0,100000]*bkg_pdf , nsig[0,100000]*sig_pdf)")
	myWS.Print()

	bkg_pdf = myWS.pdf("model_bkg")
	#signal_pdf = myWS.pdf("model_sig")
	#bkg_pdf = myWS.pdf("bkg_"+args.extension)
	#signal_pdf = myWS.pdf("sig_"+args.extension)
	pdf = myWS.pdf("model")

	mass = RooArgList( myWS.var("x") )
	h1 = inFileBkg.Get(hist)
	Bkg = h1.Clone()
	#Bkg.Scale( 1.5 )
	hData = h1.Clone()
	bkg = RooDataHist( 'bkg', 'bkg', mass, Bkg)

	#hSignal.Scale(0.1)
	data_sig = RooDataHist( 'data_sig', 'data_sig', mass, hSignal)
	#getattr( myWS, 'import')(data_sig)
	hData.Add( hSignal )
	data = RooDataHist( 'data', 'data', mass, hData)

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	c1.SetLogy()
	xframe = myWS.var("x").frame()
	bkg.plotOn( xframe )
	xframe.Draw()
	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")

	#### MINOS better than MIGRAD http://pprc.qmul.ac.uk/~bevan/yeti/fitting.pdf
	nll = bkg_pdf.createNLL(bkg, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
	m = RooMinuit(nll)
	m.migrad()
	m.hesse()
	m.minos()
	#bkg_pdf.fitTo( bkg, RooFit.Extended(kTRUE), RooFit.SumW2Error(kFALSE) )
	#bkg_pdf.fitTo( bkg, RooFit.Extended(), RooFit.Strategy(2), RooFit.Minos(), RooFit.Save(), RooFit.PrintEvalErrors(-1), RooFit.SumW2Error(kTRUE) ) 
	#bkg_pdf.fitTo( bkg, RooFit.Strategy(2), RooFit.Minos(), RooFit.Save(), RooFit.PrintEvalErrors(-1), RooFit.SumW2Error(kTRUE) ) 
	#bkg_pdf.fitTo( bkg,RooFit.Save(true),RooFit.Minimizer("Minuit2", "Migrad"),RooFit.SumW2Error(kTRUE), RooFit.PrintEvalErrors(-1) )
	bkg_pdf.plotOn( xframe )
	#bkg_pdf.plotOn( xframe, RooFit.Components("bkg_"+args.extension), RooFit.LineStyle(kDashed) )
	bkg_pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	xframe.SetMaximum(100000)
	xframe.SetMinimum(0.00001)
	c1.SaveAs('Plots/'+hist+"_QCD_FitP4Gaus_rooFit_"+args.version+"."+args.extension)
	del c1

	'''
	c2 = TCanvas('c2', 'c2',  10, 10, 750, 500 )
	c2.SetLogy()
	x2frame = myWS.var("y").frame()
	data_sig1.plotOn( x2frame )
	x2frame.Draw()
	x2frame.GetXaxis().SetTitle("Average Pruned Mass [GeV]")

	#### MINOS better than MIGRAD http://pprc.qmul.ac.uk/~bevan/yeti/fitting.pdf
	nll2 = signal_pdf.createNLL(data_sig1, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
	m2 = RooMinuit(nll2)
	m2.migrad()
	m2.hesse()
	m2.minos()
	signal_pdf.plotOn( x2frame )
	signal_pdf.paramOn( x2frame, RooFit.Layout(0.6,0.9,0.94))
	x2frame.Draw()
	c2.SaveAs('Plots/'+hist+"_RPVSt100tojj_FitP4Gaus_rooFit_"+args.version+"."+args.extension)
	del c2
	'''

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	xframe = myWS.var("x").frame()
	data.plotOn( xframe )
	xframe.Draw()
	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	#pdf.fitTo( data, RooFit.Save(true), RooFit.PrintEvalErrors(-1) ) # RooFit.Minimizer("Minuit2", "Migrad") )
	#pdf.fitTo( data,RooFit.Save(true),RooFit.Minimizer("Minuit2", "Migrad"),RooFit.SumW2Error(kTRUE), RooFit.PrintEvalErrors(-1) )
	nll_data = pdf.createNLL(data, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
	m_data = RooMinuit(nll_data)
	m_data.migrad()
	m_data.hesse()
	m_data.minos()
	pdf.plotOn( xframe )
	pdf.plotOn( xframe, RooFit.Components("bkg_"+args.extension), RooFit.LineStyle(kDashed) )
	pdf.plotOn( xframe, RooFit.Components("sig_"+args.extension), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	c1.SaveAs('Plots/'+hist+'_QCD_RPVSt'+str(args.mass)+'tojj_FitP4Gaus_rooFit.'+args.extension)
	del c1

	#### PSEUDOEXPERIMENT AS DATA
	'''
	numBkg = round( myWS.var("nbkg").getVal() )
	#numBkg = round( myWS.var("nbkg").getVal()+myWS.var("nsig").getVal() )
	numData = random.randint( numBkg-round(sqrt(numBkg)), numBkg+round(sqrt(numBkg)) )
	data_obs = myWS.pdf("model_bkg").generateBinned(RooArgSet(mass),numData, RooFit.Name("data_obs")) 
	#print myWS.var("nbkg").getVal(), myWS.var("nsig").getVal()
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	c1.SetLogy()
	xframe = myWS.var("x").frame()
	data_obs.plotOn( xframe )
	xframe.Draw()
	c1.SaveAs('Plots/'+hist+"_PseudoExp_FitP4Gaus_rooFit_"+args.version+"."+args.extension)
	del c1
	'''

	####### QCD AS DATA
	#data_obs = RooDataHist( 'data_obs', 'data_obs', mass, Bkg)
	data_obs = RooDataHist( 'data_obs', 'data_obs', mass, hData)

	getattr( myWS, 'import')(data_obs)
	'''
	modelConfig = RooStats.ModelConfig( 'modelConfig', myWS )
	modelConfig.SetPdf( myWS.pdf("model") )
	#modelConfig.SetPdf( myWS.pdf("model_sig") )
	modelConfig.SetPdf( myWS.pdf("model_bkg") )
	poi = RooArgSet( myWS.var("nsig") )
	modelConfig.SetParametersOfInterest( poi )
	obs = RooArgSet( myWS.var("x") )
	modelConfig.SetObservables( obs )
	myWS.defineSet("nuisParams","p1,p2,p3,nbkg")
	modelConfig.SetNuisanceParameters( myWS.set("nuisParams") )
	getattr( myWS, 'import')(modelConfig)
	'''

	outputRootFile = '/afs/cern.ch/work/a/algomez/RPVStops/CMSSW_8_0_20/src/RUNA/RUNStatistics/test/Rootfiles/workspace_RPVStopStopToJets_UDD312_M-'+str(imass)+'_Resolved_'+args.cut+'_'+args.version+'.root' 
	myWS.writeToFile(outputRootFile, true )
	myWS.Print()

	####### Creating datacard
	outputfile = open('/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_1_5/src/MyLimits/datacard_RPVStop'+str(args.mass)+'.txt','w')
	outputfile.write("imax 1 channels\n")
	outputfile.write("jmax 1 backgrounds\n")
	outputfile.write("kmax 0 *\n")
	outputfile.write("-------------------------------\n")
	outputfile.write("shapes * * "+outputRootFile+" myWS:$PROCESS \n")
	outputfile.write("-------------------------------\n")
	outputfile.write("bin           1\n")
	outputfile.write("observation  -1\n")
	outputfile.write("-------------------------------\n")
	outputfile.write("bin           1          1\n")
	outputfile.write("process     sig_pdf bkg_pdf\n")
	outputfile.write("process       0          1\n")
	outputfile.write('rate          '+str( round( myWS.var("nsig").getVal() ) )+' '+str( round( myWS.var("nbkg").getVal() ) )+' \n')
	outputfile.write("-------------------------------\n")
	outputfile.write("# lumi    lnN     1.045         -     \n")
	outputfile.write("# GausSigma  param       45.1220       5.7784  \n")
	outputfile.write("# GausMean  param       1000.0000       10.0000  \n")
	outputfile.write("# SigNormFit   lnN    1.0600       - \n")
	outputfile.write("# SigNormPDF   lnN    1.0300       - \n")
	outputfile.write("# SigNormJES   lnN    1.0400       - \n")
	outputfile.write("# SigNormPU   lnN    1.0300        - \n")
	outputfile.write("# SigNormISR   lnN    1.1000        - \n")
	outputfile.write("# SigNormBtag   lnN    1.0000       - -\n")
	outputfile.write("# b  param       78.8566       33.5562\n")
	outputfile.write("# c  param       -8.4161       10.6159\n")
	outputfile.write("# d  param       -0.8140       1.5043\n")
	outputfile.write("# BkgNorm    lnN     -       2.0000\n")
	outputfile.close()

def rooFitterTree( inFileBkg, inFileSignal, inFileData, hist):
	"""function to run Roofit and save workspace for RooStats"""

	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )
	
	myWS = RooWorkspace("myWS")

	x = RooRealVar( "x", "x", 50., 180. )
	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[50,180],p1[0,1000],p2[0,100],p3[0,10]})")
	myWS.factory("Gaussian:sig_pdf(x, mean[90,110], sigma[0,10])")
	myWS.factory("SUM:model(nsig[0,10000]*sig_pdf, nbkg[0,1000000]*bkg_pdf)")
	myWS.Print()

	#x = myWS.var("x")
	mass = myWS.var("mass")
	pdf = myWS.pdf("model")

	#mass = RooArgList( x )
	massAveForFit = RooRealVar( "massAveForFit", "massAveForFit", 50., 180. )
	bkgTree = inFileBkg.Get('/RUNATree' )
	bkg = RooDataSet( "bkg", "bkg", RooArgSet(massAveForFit), RooFit.Import( bkgTree ) )
	signalTree = inFileSignal.Get('/RUNATree' )
	signal = RooDataSet( "signal", "signal", RooArgSet(massAveForFit), RooFit.Import( signalTree ) )
	dataTree = inFileData.Get('/RUNATree' )
	data = RooDataSet( "data", "data", RooArgSet(massAveForFit), RooFit.Import( dataTree ) )
	
	getattr( myWS, 'import')(data)

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	xframe = massAveForFit.frame()
	data.plotOn( xframe )
	xframe.Draw()
	xframe.GetXaxis().SetTitle( histYaxis )
	pdf.fitTo( data, RooFit.Save(true), RooFit.Minimizer("Minuit2", "Migrad") )
	#pdf.fitTo( data, RooFit.Save(true) , RooFit.Minimizer("Minuit2", "Migrad"), RooFit.SumW2Error(kTRUE) )
	pdf.plotOn( xframe )
	pdf.plotOn( xframe, RooFit.Components("bkg_"+args.extension), RooFit.LineStyle(kDashed) )
	pdf.plotOn( xframe, RooFit.Components("sig_"+args.extension), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	c1.SaveAs('Plots/'+hist+"_QCD_RPVSt100tojj_FitP4Gaus_rooFitTree_"+args.version+"."+args.extension)
	del c1

	modelConfig = RooStats.ModelConfig( 'modelConfig', myWS )
	modelConfig.SetPdf( myWS.pdf("model") )
	poi = RooArgSet( myWS.var("nsig") )
	modelConfig.SetParametersOfInterest( poi )
	obs = RooArgSet( myWS.var("x") )
	modelConfig.SetObservables( obs )
	myWS.defineSet("nuisParams","p1,p2,p3,nbkg")
	modelConfig.SetNuisanceParameters( myWS.set("nuisParams") )

	getattr( myWS, 'import')(modelConfig)
	myWS.writeToFile("Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_rooFitTree.root", True )
	myWS.Print()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--process', action='store', default='Full', help='Type of fit to use.' )
	parser.add_argument('-v', '--version', action='store', default='v00', help='For Boosted of Resolved.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', help='Decay, example: jj, bj.' )
	parser.add_argument('-m', '--mass', action='store', type=int, default=300, help='Decay, example: jj, bj.' )
	parser.add_argument('-q', '--qcd', action='store', default='Pt', dest='qcd', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=1787, help='Luminosity, example: 1.' )
	parser.add_argument('-f', '--final', action='store_true', default=False, help='Final distributions.' )
	parser.add_argument('-t', '--miniTree', action='store_true', default=False, help='miniTree: if plots coming from miniTree or RUNAnalysis.' )
	parser.add_argument('-e', '--extension', action='store', default='png', help='Extension of plots.' )
	parser.add_argument('-C', '--cut', action='store', default='delta', help='cut, example: cutDEta' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	QCDSF = 1

	if args.miniTree: 
		filePrefix = 'Rootfiles/RUNMiniResolvedAnalysis'
		hist = 'massAve_'+args.cut+'_'
		#scale = 1
		scale = args.lumi #* 0.75 
		rebinX = 20 
	else: 
		filePrefix = 'Rootfiles/RUNAnalysis' 
		hist = 'ResolvedAnalysisPlotsMassPairing/massAve_cutDelta'
		scale = args.lumi
		rebinX = 2

	outputDir = "Plots/"
	signalFile =  TFile.Open(filePrefix+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_80X_V2p1_'+args.version+'.root')
	bkgFile = TFile.Open(filePrefix+'_QCD'+args.qcd+'All_80X_V2p1_'+args.version+'.root')
	bkgFile2 = TFile.Open(filePrefix+'_QCDHTAll_80X_V2p1_'+args.version+'.root')
	bkgFile3 = TFile.Open(filePrefix+'_QCDHerwigAll_80X_V2p1_'+args.version+'.root')
	#dataFile = TFile.Open(filePrefix+'_JetHT_Run2016C_V2p1_'+args.version+'.root')
	dataFile = TFile.Open(filePrefix+'_JetHT_Run2016_V2p1_'+args.version+'.root')
	

	###### Input parameters
	histYaxis = "Average dijet mass [GeV]"
	minFit = 200
	maxFit = 750
	CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 1 ) )+" fb^{-1}"
	CMS_lumi.extraText = "Preliminary Simulation"
	

	if 'full' in args.process:
		CMS_lumi.extraText = "Preliminary"
		p = Process( target=FitterCombination, args=( dataFile, bkgFile, signalFile, hist, scale, P4, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX, True ))
	elif 'Data' in args.process:
		CMS_lumi.extraText = "Preliminary"
		p = Process( target=FitterCombination, args=( dataFile, bkgFile, '', hist, scale, expoPoli, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX, True ))
		#p = Process( target=FitterCombination, args=( bkgFile3, bkgFile, '', hist, scale, P4, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX, True ))
	elif 'MC' in args.process:
		p = Process( target=FitterCombination, args=( '', bkgFile, signalFile, hist, scale, P4, [ 1, 100, 1, 1 ], minFit, maxFit, rebinX, False ))
	elif 'QCD' in args.process:
		p = Process( target=rootFitter, args=( bkgFile, hist, scale, P4, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX, True ) ) 
	elif 'RPV' in args.process:
		process = 'RPVSt'+str(args.mass)+'tojj'
		p = Process( target=rootFitter, args=( signalFile, hist, scale, gaus, [ ], args.mass-50, args.mass+50, rebinX, True, False ) ) 
	elif 'Limit' in args.process:
		p = Process( target=createCards, args=( bkgFile, bkgFile, filePrefix+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_80X_V2p1_'+args.version+'.root', hist, scale, P4, minFit, maxFit, 1 ) )
		#p = Process( target=createCards, args=( dataFile, bkgFile, filePrefix+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_80X_V2p1_'+args.version+'.root', hist, scale, P4, minFit, maxFit, 1 ) )
	else:
		rooFitterTree( bkgFile, signalFile, dataFile, hist )
	p.start()
	p.join()

	


