#!/usr/bin/env python

###################
### Make Fitting
###################

from ROOT import RooRealVar, RooDataHist, RooArgList, RooArgSet, RooAddPdf, RooFit, RooGenericPdf, RooWorkspace, RooMsgService, RooHistPdf
from ROOT import *
from tdrstyle import setSelection
import CMS_lumi, tdrstyle
from array import array
import argparse
import glob,sys, os
import warnings
import random
import numpy as np

gSystem.SetIncludePath('-I$ROOFITSYS/include')
if os.access('RooPowerFunction.cxx', os.R_OK): ROOT.gROOT.ProcessLine('.L RooPowerFunction.cxx+')

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
TVirtualFitter.SetMaxIterations(50000000)		######### Trick to increase number of iterations


xline = array('d', [0,2000])
yline = array('d', [0,0])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

######## Fit Functions
#P4 = TF1("P4", "[0]* TMath::Power(1-(x/13000.0),[1]) / (TMath::Power(x/13000.0,[2]+([3]*log(x/13000.))))",0,2000);
P1 = TF1("P1", "[0] / (TMath::Power(x/13000.0,[1]))",0,2000);
P4 = TF1("P4", "( [0]*TMath::Power(1-x/13000,[1]) ) / ( TMath::Power(x/13000,[2]) )",0,2000);
mTilde = TF1("mTilde", "(x - [0])/[1]", 0, 300 )
sumExpo = TF1("sumExpo", "[0]*exp(-[1]*x)+[2]*exp(-[3]*x)", 0, 1000 )
expoPoli = TF1("expoPoli", "exp([0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x)", 0, 1000 )
sigmoid = TF1("sigmoid", "mTilde/ (sqrt(1+ pow(mTilde,2)))", 0, 1000 )
landau = TF1("landau","[0]*TMath::Landau(-x,[1],[2])",50,300)
gaus = TF1("gaus", "gaus", 0, 2000);
P4Gaus = TF1("P4Gaus", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))+gaus(4)",50,500);
massBins = [0, 30, 60, 90, 120, 150, 180, 210, 250, 290, 330, 370, 410, 460, 510, 560, 610, 670, 730, 790, 860, 930, 1000, 1080, 1160, 1240, 1330, 1420, 1520, 1620, 1730, 1840, 2000]


def bkgFit( inFile, hist, folder, minX, maxX, lumi):
	"""Background fitter"""
	
	hInitialBkg = inFileBkg.Get(folder+'/' + hist)
	'''
	DONT FORGET TO RESIZE YOUR BINS TO 1GEV
	h1GeVBin = hInitialBkg.Clone()
	xbins = range( int(h1GeVBin.GetXaxis().GetXmin()), int(h1GeVBin.GetXaxis().GetXmax()) )
	newBinRange = array('d', xbins ) 
	print len(newBinRange)
	h1GeVBin.Rebin( len(newBinRange)-1, 'hnew', newBinRange )
	'''
	tmpHBkg = hInitialBkg.Clone(hist)
	tmpHBkg.Scale(0.8)
	binSize = tmpHBkg.GetBinWidth(1)

	tmpBkgBinContent = []
	tmpBkgBinError = []
	for ibin in range( int( minX/binSize), int(maxX/binSize ) ):
		tmpBkgBinContent.append( tmpHBkg.GetBinContent(ibin) / ( binSize * lumi ) )
		tmpBkgBinError.append( tmpHBkg.GetBinError(ibin) / binSize )

	binBkgContents = np.array(tmpBkgBinContent)
	binBkgError = np.array(tmpBkgBinError)
	print 'QCD bins NO normalized:', binBkgContents
	sumBinContents = np.sum(binBkgContents)
	binBkgContents = binBkgContents/sumBinContents
	binBkgError = binBkgError/sumBinContents

	print 'QCD bins :', binBkgContents
	print 'QCD bins error :', binBkgError
	numBins = int ( (maxX - minX)/binSize )
	hBkg = TH1D("hbkg", "hbkg", numBins, minX, maxX)
	hBkg.Sumw2()
	for ibin in range( 0, numBins ):
		hBkg.SetBinContent( ibin, binBkgContents[ibin] )
		hBkg.SetBinError( ibin, binBkgError[ibin] )

	sys.exit(0)
	fitFunction.SetParameter(0,1)
	fitFunction.SetParameter(1,10)
	fitFunction.SetParameter(2,10.)
	fitFunction.SetParameter(3,10.)

	fitStatus = 0
	#for loop in range(0,20):
	hBkg.Fit(fitFunction,"MELLS","",minX,maxX)
	hBkg.Fit(fitFunction,"MELLS","",minX,maxX)
		#result = hBkg.Fit(fitFunction,"MELLS","",minX,maxX)
		#fitStatus = int(result)
		#print "fit status : %d" % fitStatus
		#if(fitStatus==1):
			#stopProgram=0
		#	result.Print("V")
		#	break
	#hBkg.Fit(fitFunction,"MR","",minX,maxX)
	#if 'QCD' in Signal: fitFunction.SetParameter(0,1)
	#hBkg.Fit(fitFunction,"MR","",minX,maxX)
	P4Parameters =  [ fitFunction.GetParameter(0), fitFunction.GetParameter(1), fitFunction.GetParameter(2), fitFunction.GetParameter(3) ]

			
	######### Plotting Histograms
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	c1.SetLogy()
	gStyle.SetOptFit()
	gStyle.SetStatY(0.91)
	gStyle.SetStatX(0.95)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.15) 
	hBkg.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	hBkg.GetYaxis().SetTitle("dN/dm_{av} / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	#hBkg.GetYaxis().SetTitleOffset(1.2);
	hBkg.SetTitle("")
	hBkg.Draw()
	#setSelection( Signal, '13 TeV - '+PU, 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.5 )
	numBkgEvents = round(hBkg.Integral( ) ) #int(minX/10), int(maxX/10) ))
	print "NUMBER OF EVENT IN QCD", numBkgEvents
	c1.SaveAs(outputDir+hist+"_QCD_"+PU+"_Fit.pdf")
	del c1




def Fitter( inFileBkg, inFileSignal, hist, folder, fitFunction, minX, maxX ):
	"""Main Fitter"""

	##### BKG
	hInitialBkg = inFileBkg.Get(folder+'/' + hist)
	tmpHBkg = hInitialBkg.Clone(hist)
	tmpHBkg.Scale(1.5)
	binSize = tmpHBkg.GetBinWidth(1)

	tmpBkgBinContent = []
	tmpBkgBinError = []
	for ibin in range( int( minX/binSize), int(maxX/binSize ) ):
		tmpBkgBinContent.append( tmpHBkg.GetBinContent(ibin) / binSize )
		tmpBkgBinError.append( tmpHBkg.GetBinError(ibin) / binSize )

	binBkgContents = np.array(tmpBkgBinContent)
	binBkgError = np.array(tmpBkgBinError)
	print 'QCD bins NO normalized:', binBkgContents
	sumBinContents = np.sum(binBkgContents)
	binBkgContents = binBkgContents/sumBinContents
	binBkgError = binBkgError/sumBinContents

	print 'QCD bins :', binBkgContents
	print 'QCD bins error :', binBkgError
	numBins = int ( (maxX - minX)/binSize )
	hBkg = TH1D("hbkg", "hbkg", numBins, minX, maxX)
	hBkg.Sumw2()
	for ibin in range( 0, numBins ):
		hBkg.SetBinContent( ibin, binBkgContents[ibin] )
		hBkg.SetBinError( ibin, binBkgError[ibin] )

	fitFunction.SetParameter(0,1)
	fitFunction.SetParameter(1,10)
	fitFunction.SetParameter(2,10.)
	fitFunction.SetParameter(3,10.)

	fitStatus = 0
	#for loop in range(0,20):
	hBkg.Fit(fitFunction,"MELLS","",minX,maxX)
	hBkg.Fit(fitFunction,"MELLS","",minX,maxX)
		#result = hBkg.Fit(fitFunction,"MELLS","",minX,maxX)
		#fitStatus = int(result)
		#print "fit status : %d" % fitStatus
		#if(fitStatus==1):
			#stopProgram=0
		#	result.Print("V")
		#	break
	#hBkg.Fit(fitFunction,"MR","",minX,maxX)
	#if 'QCD' in Signal: fitFunction.SetParameter(0,1)
	#hBkg.Fit(fitFunction,"MR","",minX,maxX)
	P4Parameters =  [ fitFunction.GetParameter(0), fitFunction.GetParameter(1), fitFunction.GetParameter(2), fitFunction.GetParameter(3) ]

			
	######### Plotting Histograms
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	c1.SetLogy()
	gStyle.SetOptFit()
	gStyle.SetStatY(0.91)
	gStyle.SetStatX(0.95)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.15) 
	hBkg.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	hBkg.GetYaxis().SetTitle("dN/dm_{av} / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	#hBkg.GetYaxis().SetTitleOffset(1.2);
	hBkg.SetTitle("")
	hBkg.Draw()
	#setSelection( Signal, '13 TeV - '+PU, 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.5 )
	numBkgEvents = round(hBkg.Integral( ) ) #int(minX/10), int(maxX/10) ))
	print "NUMBER OF EVENT IN QCD", numBkgEvents
	c1.SaveAs(outputDir+hist+"_QCD_"+PU+"_Fit.pdf")
	del c1
	
	#### Signal
	#hInitialSignal = inFileSignal.Get(folder+'/' + hist)
	hInitialSignal = inFileSignal.Get('BoostedAnalysisPlotsPruned/massAve_cutSubjetPtRatio')
	tmpSigHisto = hInitialSignal.Clone()
	tmpSigBinContent = []
	tmpSigBinError = []
	for ibin in range( int( minX/binSize), int(maxX/binSize ) ):
		print tmpSigHisto.GetBinContent(ibin)
		tmpSigBinContent.append( tmpSigHisto.GetBinContent(ibin)/ binSize )
		tmpSigBinError.append( tmpSigHisto.GetBinError(ibin) /binSize )
	
	binSigContents = np.array(tmpSigBinContent)
	binSigError = np.array(tmpSigBinError)
	print 'Signal bins NO normalized:', binSigContents
	sumBinSig = np.sum(binSigContents)
	binSigContents = binSigContents/sumBinSig
	binSigError = binSigError/sumBinSig
	print 'Signal bins :', binSigContents
	hSignal = TH1D("hSig", "hSig", numBins, minX, maxX)
	for ibin in range( 0, numBins ):
		hSignal.SetBinContent( ibin, binSigContents[ibin] )
	hSignal.Fit( gaus, "ELLSR","", MASS-30, MASS+30)
	hSignal.Fit( gaus, "ELLSR","", MASS-30, MASS+30)
	gausParameters = [ gaus.GetParameter(0), gaus.GetParameter(1) , gaus.GetParameter(2) ]
	## Acceptance
	tmpGaus = TF1("gaus", "gaus", 0, 2000);
	tmpSigHisto.Fit( tmpGaus, "ELLSR","", MASS-30, MASS+30 )
	numSigEvents = round( tmpSigHisto.Integral( ) )
	print "NUMBER OF EVENT IN Signal", numSigEvents
	
	return [ P4Parameters, numBkgEvents, binBkgContents, binBkgError, gausParameters, numSigEvents, binSigContents, binSigError ]

def FitterCombination( inFileBkg, inFileSignal, hist, folder, bkgFunction, minX, maxX ):
	"""docstring for FitterCombination"""

	outputDir = "Plots/"
	binSize = 10


	### Fit QCD
	parameters = Fitter( inFileBkg, inFileSignal, hist, folder, P4, minX, maxX )
	print 'exit'
	sys.exit(0)
	print parameters
	bkgParameters = parameters[0]
	bkgAcceptance = parameters[1]
	bkgContent = parameters[2]
	bkgErr = parameters[3]
	gausParameters = parameters[4]
	sigAcceptance = parameters[5]
	sigContent = parameters[6]
	sigErr = parameters[7]

	data = bkgContent + sigContent
	dataErr = [ TMath.Sqrt( bkgErr[k]*bkgErr[k] + sigErr[k]*sigErr[k]  ) for k in range( 0, len(bkgErr) ) ]
	print 'DATA :', data
	print 'DATA Err:', dataErr
	hBkg = TH1D("hbkg", "hbkg", len(data) , minX, maxX)
	hBkg.Sumw2()
	hPull = TH1D("hpull", "hpull", len(data) , minX, maxX)
	hPull.Sumw2()
	hResidual = TH1D("hresidual", "hresidual", len(data) , minX, maxX)
	hResidual.Sumw2()

	for ibin in range( 0, len(data)):
		hBkg.SetBinContent( ibin, data[ibin] )
		hBkg.SetBinError( ibin, dataErr[ibin] )
	### Create PseudoExperiment
	'''
	h1 = inFileBkg.Get(folder+'/' + hist)
	binSize = h1.GetBinWidth(1)
	P4PSE = TF1("P4PSE", "[0]*pow(1-x/13000.0,[1])/pow(x/13000.0,[2]+[3]*log(x/13000.))", minX, maxX);
	P4PSE.SetParameter(0,bkgParameters[0])				
	P4PSE.SetParameter(1,bkgParameters[1])
	P4PSE.SetParameter(2,bkgParameters[2])
	P4PSE.SetParameter(3,bkgParameters[3])
	randomNumEventsQCD = random.randint( bkgParameters[4]-round(sqrt(bkgParameters[4])), bkgParameters[4]+round(sqrt(bkgParameters[4])) )
	print "randomNumberOf QCD events", randomNumEventsQCD
	hBkgPSE = TH1D("hbkgPSE", "hbkgPSE", int( (maxX-minX)/binSize ) , minX, maxX)
	hBkgPSE.FillRandom( "P4PSE", int(randomNumEventsQCD) )
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	c1.SetLogy()
	gStyle.SetOptFit()
	gStyle.SetStatY(0.94)
	gStyle.SetStatX(0.9)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.15) 
	hBkgPSE.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	hBkgPSE.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	hBkgPSE.GetYaxis().SetTitleOffset(1.2);
	hBkgPSE.SetTitle("QCD PseudoExperiments")
	hBkgPSE.Sumw2()
	hBkgPSE.Draw()
	c1.SaveAs(outputDir+hist+"_PseudoExperiment_"+PU+"_Fit.pdf")
	del c1
	'''
			
	P4Gaus.SetParameter(0,bkgParameters[0])				
	P4Gaus.SetParameter(1,bkgParameters[1])
	P4Gaus.SetParameter(2,bkgParameters[2])
	P4Gaus.SetParameter(3,bkgParameters[3])
	P4Gaus.SetParameter(4,gausParameters[0])
	P4Gaus.SetParameter(5,gausParameters[1])
	P4Gaus.SetParameter(6,gausParameters[2])

	hBkg.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	hBkg.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	hBkg.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	gaus2 = TF1("gaus2", "gaus", MASS-30, MASS+30 );
	P4_2 = TF1("P4_2", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))", minX, maxX);
	P4_2.SetParameter(0, P4Gaus.GetParameter(0) )
	P4_2.SetParameter(1, P4Gaus.GetParameter(1) )
	P4_2.SetParameter(2, P4Gaus.GetParameter(2) )
	P4_2.SetParameter(3, P4Gaus.GetParameter(3) )
	gaus2.SetParameter(0, P4Gaus.GetParameter(4) )
	gaus2.SetParameter(1, P4Gaus.GetParameter(5) )
	gaus2.SetParameter(2, P4Gaus.GetParameter(6) )
	print "SIGNALLLL", gaus2.Integral(MASS-30, MASS+30)
	P4GausParameters = [ P4Gaus.GetParameter(0), P4Gaus.GetParameter(1), P4Gaus.GetParameter(2), P4Gaus.GetParameter(3), P4Gaus.GetParameter(4), P4Gaus.GetParameter(5), P4Gaus.GetParameter(6), bkgAcceptance, sigAcceptance, minX, maxX ]
	print P4GausParameters


	######## Calculating Pull and Residual
	for ibin in range(0, len(data) ):
	
		binCont = data[ibin]
		binErr = dataErr[ibin]
		valIntegral = P4_2.Eval( hBkg.GetBinCenter(ibin) ) ### +5 because binSize is 10
		print binCont, binErr, valIntegral 
	
		diff = (binCont - valIntegral)/ valIntegral
		errDiff = diff * TMath.Sqrt( TMath.Power( P4Gaus.GetParError(0) / P4Gaus.GetParameter(0),2 ) + TMath.Power( P4Gaus.GetParError(1)/ P4Gaus.GetParameter(1), 2 )  + TMath.Power( P4Gaus.GetParError(2)/ P4Gaus.GetParameter(2), 2 )  + TMath.Power( P4Gaus.GetParError(3)/ P4Gaus.GetParameter(3), 2 ) )

		if (binCont != 0):
			pull = (binCont - valIntegral)/ binErr
			#print pull
			hPull.SetBinContent(ibin, pull)
			hPull.SetBinError(ibin, 1.0)
	
			hResidual.SetBinContent(ibin, diff)
			#hResidual.SetBinError(ibin, binErr/valIntegral )
			hResidual.SetBinError(ibin, errDiff )#/valIntegral)


	######### Plotting Histograms
	tdrStyle.SetPadRightMargin(0.05)
  	tdrStyle.SetPadLeftMargin(0.15)
	c3 = TCanvas('c1', 'c1',  10, 10, 750, 1000 )
	pad1 = TPad("pad1", "Fit",0,0.50,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.25,1.00,0.50,-1);
	pad3 = TPad("pad3", "Residual",0,0,1.00,0.25,-1);
	pad1.Draw()
	pad2.Draw()
	pad3.Draw()

	pad1.cd()
	pad1.SetLogy()
	hBkg.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	hBkg.GetYaxis().SetTitle("dN/dm_{av} / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	hBkg.GetYaxis().SetTitleOffset(1.2);
	hBkg.SetTitle("")
	#hBkg.SetMaximum( 1.5 * hBkg.GetMaximum() )
	hBkg.Draw()
	hBkg.GetXaxis().SetRangeUser( minX, maxX+30 )
	P4Gaus.SetLineColor(kBlack)
	P4Gaus.Draw("same")
	gaus2.SetLineColor(kRed-4)
	gaus2.Draw("same")
	P4_2.SetLineColor(kBlue-4)
	P4_2.Draw("same")
	CMS_lumi.lumi_13TeV = '1 fb^{-1}'
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	CMS_lumi.relPosX = 0.14
	setSelection( listSel=[ 'QCD + RPV #tilde{t} '+str(MASS)+' GeV', 'AK8PFHT700_TrimMass50', 'number of jets > 1', 'A < 0.1, |cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'] , xMin=0.93 , yMax=0.60 )


	pad2.cd()
	gStyle.SetOptStat(0)
	#hPull.GetXaxis().SetTitle("Average Mass [GeV]")
	hPull.GetYaxis().SetTitle("Pull")
	hPull.GetYaxis().SetLabelSize(0.08)
	hPull.GetXaxis().SetLabelSize(0.08)
	hPull.GetYaxis().SetTitleSize(0.10)
	hPull.GetYaxis().SetTitleOffset(0.60)
	hPull.SetMarkerStyle(7)
	#hPull.SetMaximum(3)
	hPull.GetXaxis().SetRangeUser( minX, maxX+30 )
	hPull.Sumw2()
	hPull.Draw("e")
	line.Draw("same")
	
	pad3.cd()
	gStyle.SetOptStat(0)
	#hResidual.GetXaxis().SetTitle("Average Mass [GeV]")
	hResidual.GetYaxis().SetTitle("Residual ")
	hResidual.GetYaxis().SetLabelSize(0.08)
	hResidual.GetXaxis().SetLabelSize(0.08)
	hResidual.GetYaxis().SetTitleSize(0.10)
	hResidual.GetYaxis().SetTitleOffset(0.60)
	hResidual.SetMarkerStyle(7)
	#hResidual.SetMaximum(1)
	hResidual.GetXaxis().SetRangeUser( minX, maxX+30 )
	#hResidual.Sumw2()
	hResidual.Draw("e")
	line.Draw("same")
	c3.SaveAs(outputDir+hist+"_QCD_RPVSt"+str(MASS)+"tojj_"+PU+"_FitP4Gaus.pdf")
	del c3

	return P4GausParameters

def rooFitter( inFileBkg, inFileSignal, hist, folder, MASS, outputRootFile, minX, maxX ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )

	P4GausParameters = FitterCombination( inFileBkg, inFileSignal, hist, folder, P4, minX, maxX )
	bkgAcc = P4GausParameters[7]
	#sigAcc = P4GausParameters[8]
	
	hSignal = inFileSignal.Get(folder+'/' + hist)
	sigAcc = hSignal.Integral(hSignal.GetXaxis().FindBin(minX), hSignal.GetXaxis().FindBin( maxX ))/hSignal.Integral(1,hSignal.GetXaxis().FindBin( maxX) )
	hBkg = inFileBkg.Get(folder+'/' + hist)
	hData = hBkg.Clone()
	#hData.Add( hSignal )

	mass = RooRealVar( 'mass', 'mass', minX, maxX  )
	rooSigHist = RooDataHist( 'rooSigHist', 'rooSigHist', RooArgList(mass), hSignal )
	rooSigHist.Print()

	signal = RooHistPdf('signal','signal',RooArgSet(mass),rooSigHist)
        signal.Print()
        signal_norm = RooRealVar('signal_norm','signal_norm',0,-1e+05,1e+05)
        #if args.fitBonly: signal_norm.setConstant()
        signal_norm.Print()

        p1 = RooRealVar('p1','p1',P4GausParameters[1], 0., 1000.)
        p2 = RooRealVar('p2','p2',P4GausParameters[2], 0., 50.)
        p3 = RooRealVar('p3','p3',P4GausParameters[3], -10., 10.)
	sqrtS = 13000

        background = RooGenericPdf('background','(pow(1-@0/%.1f,@1)/pow(@0/%.1f,@2+@3*log(@0/%.1f)))'%(sqrtS,sqrtS,sqrtS),RooArgList(mass,p1,p2,p3))
        background.Print()
        dataInt = hData.Integral(hData.GetXaxis().FindBin( minX ), hData.GetXaxis().FindBin(maxX) )
        background_norm = RooRealVar('background_norm','background_norm',dataInt,0.,1e+07)
        background_norm.Print()

        # S+B model
        model = RooAddPdf("model","s+b",RooArgList(background,signal),RooArgList(background_norm,signal_norm))

        rooDataHist = RooDataHist('rooDatahist','rooDathist',RooArgList(mass),hData)
        rooDataHist.Print()

	res = model.fitTo(rooDataHist, RooFit.Save(kTRUE), RooFit.Strategy(0))
	res.Print()

	myWS = RooWorkspace("myWS")
	getattr(myWS,'import')(signal)
        getattr(myWS,'import')(background)
        getattr(myWS,'import')(background_norm)
        getattr(myWS,'import')(rooDataHist,RooFit.Rename("data_obs"))
        myWS.Print()
        myWS.writeToFile(outputRootFile, True)
 # -----------------------------------------
        # write a datacard

        datacard = open('/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_1_5/src/MyLimits/datacard_RPVStop'+str(MASS)+'.txt','w')
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
        datacard.write('------------------------------\n')
        #flat parameters --- flat prior
        datacard.write('background_norm  flatParam\n')
        datacard.write('p1  flatParam\n')
        datacard.write('p2  flatParam\n')
        datacard.write('p3  flatParam\n')
        datacard.close()

#	''' CONFIG FOR 732 WORKS PERFECT
#	x = RooRealVar( "x", "x", 50., 190. )
#	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[50,190],p1[2116,2117],p2[-62,63],p3[-5,-4]})")
#	myWS.factory("Gaussian:sig_pdf(x, mean[93,94], sigma[5,6])")
#	myWS.factory("SUM:model(nsig[0,100000]*sig_pdf, nbkg[0,1000000]*bkg_pdf)")
#	myWS.factory("SUM:model_b(nbkg[0,1000000]*bkg_pdf)")
#
#	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[70,600], p1[-4000,4000],p2[-300,300],p3[0,40]})")
#
#	'''
#
#	myWS.factory("x["+str(P4GausParameters[7])+","+str(P4GausParameters[8])+"]")
#	bins = (P4GausParameters[8]-P4GausParameters[7])/10
#	myWS.var("x").setBins(int(bins))
#	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1["+str(P4GausParameters[1])+"],p2["+str(P4GausParameters[2])+"],p3["+str(P4GausParameters[3])+"]})")
#	#myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1[-2000,1000],p2[-200,200],p3[-20,20]})")
#	#myWS.factory("Gaussian:sig_pdf(x, mean["+str(MASS)+"], sigma[0,10])")
#	myWS.factory("Gaussian:sig_pdf(x, mean["+str(P4GausParameters[5])+"], sigma["+str(P4GausParameters[6])+"])")
#	#myWS.factory("Gaussian:sig_pdf(x, mean[93.29], sigma[5.52])")
#	#myWS.factory("Gaussian:sig_pdf(x, mean[90,100], sigma[0,10])")
#	myWS.factory("SUM:model_bkg( nbkg[0,100000]*bkg_pdf )")
#	#myWS.factory("SUM:model_sig( nsig[0,10000]*sig_pdf )")
#	myWS.factory("SUM:model( nbkg[0,100000]*bkg_pdf , nsig[0,100000]*sig_pdf)")
#	myWS.Print()
#
#	bkg_pdf = myWS.pdf("model_bkg")
#	#signal_pdf = myWS.pdf("model_sig")
#	#bkg_pdf = myWS.pdf("bkg_pdf")
#	#signal_pdf = myWS.pdf("sig_pdf")
#	pdf = myWS.pdf("model")
#
#	mass = RooArgList( myWS.var("x") )
#	h1 = inFileBkg.Get(folder+'/' + hist)
#	Bkg = h1.Clone()
#	#Bkg.Scale( 1.5 )
#	hData = h1.Clone()
#	bkg = RooDataHist( 'bkg', 'bkg', mass, Bkg)
#
#	#hSignal.Scale(0.1)
#	data_sig = RooDataHist( 'data_sig', 'data_sig', mass, hSignal)
#	#getattr( myWS, 'import')(data_sig)
#	hData.Add( hSignal )
#	data = RooDataHist( 'data', 'data', mass, hData)
#
#	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
#	c1.SetLogy()
#	xframe = myWS.var("x").frame()
#	bkg.plotOn( xframe )
#	xframe.Draw()
#	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
#
#	#### MINOS better than MIGRAD http://pprc.qmul.ac.uk/~bevan/yeti/fitting.pdf
#	nll = bkg_pdf.createNLL(bkg, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
#	m = RooMinuit(nll)
#	m.migrad()
#	m.hesse()
#	m.minos()
#	#bkg_pdf.fitTo( bkg, RooFit.Extended(kTRUE), RooFit.SumW2Error(kFALSE) )
#	#bkg_pdf.fitTo( bkg, RooFit.Extended(), RooFit.Strategy(2), RooFit.Minos(), RooFit.Save(), RooFit.PrintEvalErrors(-1), RooFit.SumW2Error(kTRUE) ) 
#	#bkg_pdf.fitTo( bkg, RooFit.Strategy(2), RooFit.Minos(), RooFit.Save(), RooFit.PrintEvalErrors(-1), RooFit.SumW2Error(kTRUE) ) 
#	#bkg_pdf.fitTo( bkg,RooFit.Save(true),RooFit.Minimizer("Minuit2", "Migrad"),RooFit.SumW2Error(kTRUE), RooFit.PrintEvalErrors(-1) )
#	bkg_pdf.plotOn( xframe )
#	#bkg_pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
#	bkg_pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
#	xframe.Draw()
#	xframe.SetMaximum(100000)
#	xframe.SetMinimum(0.00001)
#	c1.SaveAs('Plots/'+hist+"_QCD_"+PU+"_FitP4Gaus_rooFit.pdf")
#	del c1
#
#	'''
#	c2 = TCanvas('c2', 'c2',  10, 10, 750, 500 )
#	c2.SetLogy()
#	x2frame = myWS.var("y").frame()
#	data_sig1.plotOn( x2frame )
#	x2frame.Draw()
#	x2frame.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
#
#	#### MINOS better than MIGRAD http://pprc.qmul.ac.uk/~bevan/yeti/fitting.pdf
#	nll2 = signal_pdf.createNLL(data_sig1, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
#	m2 = RooMinuit(nll2)
#	m2.migrad()
#	m2.hesse()
#	m2.minos()
#	signal_pdf.plotOn( x2frame )
#	signal_pdf.paramOn( x2frame, RooFit.Layout(0.6,0.9,0.94))
#	x2frame.Draw()
#	c2.SaveAs('Plots/'+hist+"_RPVSt100tojj_"+PU+"_FitP4Gaus_rooFit.pdf")
#	del c2
#	'''
#
#	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
#	xframe = myWS.var("x").frame()
#	data.plotOn( xframe )
#	xframe.Draw()
#	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
#	#pdf.fitTo( data, RooFit.Save(true), RooFit.PrintEvalErrors(-1) ) # RooFit.Minimizer("Minuit2", "Migrad") )
#	#pdf.fitTo( data,RooFit.Save(true),RooFit.Minimizer("Minuit2", "Migrad"),RooFit.SumW2Error(kTRUE), RooFit.PrintEvalErrors(-1) )
#	nll_data = pdf.createNLL(data, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
#	m_data = RooMinuit(nll_data)
#	m_data.migrad()
#	m_data.hesse()
#	m_data.minos()
#	pdf.plotOn( xframe )
#	pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
#	pdf.plotOn( xframe, RooFit.Components("sig_pdf"), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
#	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
#	xframe.Draw()
#	c1.SaveAs('Plots/'+hist+'_QCD_RPVSt'+str(MASS)+'tojj_'+PU+'_FitP4Gaus_rooFit.pdf')
#	del c1
#
#	#### PSEUDOEXPERIMENT AS DATA
#	'''
#	numBkg = round( myWS.var("nbkg").getVal() )
#	#numBkg = round( myWS.var("nbkg").getVal()+myWS.var("nsig").getVal() )
#	numData = random.randint( numBkg-round(sqrt(numBkg)), numBkg+round(sqrt(numBkg)) )
#	data_obs = myWS.pdf("model_bkg").generateBinned(RooArgSet(mass),numData, RooFit.Name("data_obs")) 
#	#print myWS.var("nbkg").getVal(), myWS.var("nsig").getVal()
#	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
#	c1.SetLogy()
#	xframe = myWS.var("x").frame()
#	data_obs.plotOn( xframe )
#	xframe.Draw()
#	c1.SaveAs('Plots/'+hist+"_PseudoExp_"+PU+"_FitP4Gaus_rooFit.pdf")
#	del c1
#	'''
#
#	####### QCD AS DATA
#	#data_obs = RooDataHist( 'data_obs', 'data_obs', mass, Bkg)
#	data_obs = RooDataHist( 'data_obs', 'data_obs', mass, hData)
#
#	getattr( myWS, 'import')(data_obs)
#	'''
#	modelConfig = RooStats.ModelConfig( 'modelConfig', myWS )
#	modelConfig.SetPdf( myWS.pdf("model") )
#	#modelConfig.SetPdf( myWS.pdf("model_sig") )
#	modelConfig.SetPdf( myWS.pdf("model_bkg") )
#	poi = RooArgSet( myWS.var("nsig") )
#	modelConfig.SetParametersOfInterest( poi )
#	obs = RooArgSet( myWS.var("x") )
#	modelConfig.SetObservables( obs )
#	myWS.defineSet("nuisParams","p1,p2,p3,nbkg")
#	modelConfig.SetNuisanceParameters( myWS.set("nuisParams") )
#	getattr( myWS, 'import')(modelConfig)
#	'''
#
#	myWS.writeToFile(outputRootFile, true )
#	myWS.Print()
#
#	####### Creating datacard
#	outputfile = open('/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_1_5/src/MyLimits/datacard_RPVStop'+str(MASS)+'.txt','w')
#	outputfile.write("imax 1 channels\n")
#	outputfile.write("jmax 1 backgrounds\n")
#	outputfile.write("kmax 0 *\n")
#	outputfile.write("-------------------------------\n")
#	outputfile.write("shapes * * "+outputRootFile+" myWS:$PROCESS \n")
#	outputfile.write("-------------------------------\n")
#	outputfile.write("bin           1\n")
#	outputfile.write("observation  -1\n")
#	outputfile.write("-------------------------------\n")
#	outputfile.write("bin           1          1\n")
#	outputfile.write("process     sig_pdf bkg_pdf\n")
#	outputfile.write("process       0          1\n")
#	outputfile.write('rate          '+str( round( myWS.var("nsig").getVal() ) )+' '+str( round( myWS.var("nbkg").getVal() ) )+' \n')
#	outputfile.write("-------------------------------\n")
#	outputfile.write("# lumi    lnN     1.045         -     \n")
#	outputfile.write("# GausSigma  param       45.1220       5.7784  \n")
#	outputfile.write("# GausMean  param       1000.0000       10.0000  \n")
#	outputfile.write("# SigNormFit   lnN    1.0600       - \n")
#	outputfile.write("# SigNormPDF   lnN    1.0300       - \n")
#	outputfile.write("# SigNormJES   lnN    1.0400       - \n")
#	outputfile.write("# SigNormPU   lnN    1.0300        - \n")
#	outputfile.write("# SigNormISR   lnN    1.1000        - \n")
#	outputfile.write("# SigNormBtag   lnN    1.0000       - -\n")
#	outputfile.write("# b  param       78.8566       33.5562\n")
#	outputfile.write("# c  param       -8.4161       10.6159\n")
#	outputfile.write("# d  param       -0.8140       1.5043\n")
#	outputfile.write("# BkgNorm    lnN     -       2.0000\n")
#	outputfile.close()

def rooFitterTree( inFileBkg, inFileSignal, inFileData, hist, folder ):
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
	bkgTree = inFileBkg.Get(folder+'/RUNATree' )
	bkg = RooDataSet( "bkg", "bkg", RooArgSet(massAveForFit), RooFit.Import( bkgTree ) )
	signalTree = inFileSignal.Get(folder+'/RUNATree' )
	signal = RooDataSet( "signal", "signal", RooArgSet(massAveForFit), RooFit.Import( signalTree ) )
	dataTree = inFileData.Get(folder+'/RUNATree' )
	data = RooDataSet( "data", "data", RooArgSet(massAveForFit), RooFit.Import( dataTree ) )
	
	getattr( myWS, 'import')(data)

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	xframe = massAveForFit.frame()
	data.plotOn( xframe )
	xframe.Draw()
	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	pdf.fitTo( data, RooFit.Save(true), RooFit.Minimizer("Minuit2", "Migrad") )
	#pdf.fitTo( data, RooFit.Save(true) , RooFit.Minimizer("Minuit2", "Migrad"), RooFit.SumW2Error(kTRUE) )
	pdf.plotOn( xframe )
	pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
	pdf.plotOn( xframe, RooFit.Components("sig_pdf"), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	c1.SaveAs('Plots/'+hist+"_QCD_RPVSt100tojj_"+PU+"_FitP4Gaus_rooFitTree.pdf")
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
	myWS.writeToFile("Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_"+PU+"_rooFitTree.root", True )
	myWS.Print()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--process', action='store', default='Full', help='Type of fit to use.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-m', '--mass', action='store', type=int, default=100, help='Decay, example: jj, bj.' )
	parser.add_argument('-pu', '--PU', action='store', default='Asympt25ns', help='PU, example: PU40bx25.' )
	parser.add_argument('-l', '--lumi', action='store', default='1000', help='Luminosity, example: 1.' )
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	process = args.process
	jj = args.decay
	PU = args.PU
	lumi = args.lumi
	MASS = args.mass

	outputDir = "Plots/"
	inFileBkg = TFile('Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15DR74_'+PU+'_v03_v01.root')
	inFileSignal = TFile('Rootfiles/v01_v06/RUNAnalysis_RPVSt'+str(MASS)+'tojj_RunIISpring15DR74_'+PU+'_v02p2_v06.root')
	inFileData = TFile('Rootfiles/v01_v06/RUNAnalysis_QCDPtAll_RunIISpring15DR74_'+PU+'_v01_v06.root')
	outputRootFile = '/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_4_5_patch1/src/RUNA/RUNAnalysis/test/Rootfiles/workspace_QCD_RPVSt'+str(MASS)+'tojj_FitP4Gaus_'+PU+'_rooFit_'+lumi+'fb.root'

	###### Input parameters
	hist = 'massAve_cutNOMassAsym'  # str ( sys.argv[1] )
	#hist = 'massAve_cutTau31'  # str ( sys.argv[1] )
	folder = "BoostedAnalysisPlotsPruned"      # str ( sys.argv[2] )
	

	if 'bkg' in process:
		bkgFit( inFileBkg, hist, folder, 30.0, 400.0, lumi )

	elif 'full' in process:
		dummyReturn = FitterCombination( inFileBkg, inFileSignal, hist, folder, P4, 30.0, 400.0 )
	elif 'rooFit' in process:
		rooFitter( inFileBkg, inFileSignal, hist, folder, MASS, outputRootFile, 80.0, 300.0  )
		#rooFitter( inFileBkg, inFileSignal, hist, folder, MASS, outputRootFile, 250.0, 450.0  )
	else:
		rooFitterTree( inFileBkg, inFileSignal, inFileData, hist, folder )

	


