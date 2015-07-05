#!/usr/bin/env python

###################
### Make Fitting
###################

from ROOT import RooFit, RooStats
from ROOT import *
from setTDRStyle import *
from array import array
import argparse
import glob,sys, os
import warnings
import random

ROOT.gSystem.SetIncludePath('-I$ROOFITSYS/include')
if os.access('RooPowerFunction.cxx', os.R_OK): ROOT.gROOT.ProcessLine('.L RooPowerFunction.cxx+')

gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')
TVirtualFitter.SetMaxIterations(50000000)		######### Trick to increase number of iterations


gStyle.SetOptFit()
gStyle.SetStatY(0.94)
gStyle.SetStatX(0.9)
gStyle.SetStatW(0.15)
gStyle.SetStatH(0.15) 
xline = array('d', [0,2000])
yline = array('d', [0,0])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

######## Fit Functions
P4 = TF1("P4", "[0]*pow(1-x/13000.0,[1])/pow(x/13000.0,[2]+[3]*log(x/13000.))",0,2000);
mTilde = TF1("mTilde", "(x - [0])/[1]", 0, 300 )
sumExpo = TF1("sumExpo", "[0]*exp(-[1]*x)+[2]*exp(-[3]*x)", 0, 1000 )
expoPoli = TF1("expoPoli", "exp([0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x)", 0, 1000 )
sigmoid = TF1("sigmoid", "mTilde/ (sqrt(1+ pow(mTilde,2)))", 0, 1000 )
landau = TF1("landau","[0]*TMath::Landau(-x,[1],[2])",50,300)
gaus = TF1("gaus", "gaus", 0, 2000);
P4Gaus = TF1("P4Gaus", "[0]*pow(1-x/13000.0,[1])/pow(x/13000.0,[2]+[3]*log(x/13000.))+gaus(4)",50,500);

def Fitter( inFile, Signal, hist, folder, fitFunction, minX, maxX ):
	"""Main Fitter"""

	massBins = [0, 30, 60, 90, 120, 150, 180, 210, 250, 290, 330, 370, 410, 460, 510, 560, 610, 670, 730, 790, 860, 930, 1000, 1080, 1160, 1240, 1330, 1420, 1520, 1620, 1730, 1840, 2000]

	h1 = inFile.Get(folder+'/' + hist)
	histo = h1.Clone(hist)
	binSize = histo.GetBinWidth(1)

	PreFitStart= histo.GetMaximumBin()*binSize-minX
	PreFitEnd  = histo.GetMaximumBin()*binSize+maxX
	print PreFitStart
	#fitFunction.SetParameter(1, histo.GetMaximumBin()*binSize)
	#fitFunction.SetParameter(2, 10000.)
	fitFunction.SetParameter(1,100)
	fitFunction.SetParameter(0,1)
	histo.Fit(fitFunction,"","",PreFitStart,PreFitEnd)
	histo.Fit(fitFunction,"","",PreFitStart,PreFitEnd)
	histo.Fit(fitFunction,"","",PreFitStart,PreFitEnd)
	#histo.Fit(fitFunction,"MR","",PreFitStart,PreFitEnd)
	#if 'QCD' in Signal: fitFunction.SetParameter(0,1)
	#histo.Fit(fitFunction,"MR","",PreFitStart,PreFitEnd)
	#histo.Fit(fitFunction,"MR","",PreFitStart,PreFitEnd)

			
	######### Plotting Histograms
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	c1.SetLogy()
	gStyle.SetOptFit()
	gStyle.SetStatY(0.94)
	gStyle.SetStatX(0.9)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.15) 
	histo.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	histo.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	histo.GetYaxis().SetTitleOffset(1.2);
	histo.SetTitle("")
	histo.Sumw2()
	histo.Draw()
	#setSelection( Signal, '13 TeV - '+PU, 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.5 )
	c1.SaveAs(outputDir+hist+"_"+Signal+"_"+PU+"_Fit.pdf")
	del c1
	fitFunctionParameters = [ fitFunction.GetParameter(0), fitFunction.GetParameter(1), fitFunction.GetParameter(2), fitFunction.GetParameter(3) ]
	return fitFunctionParameters

def FitterCombination( inFileBkg, inFileSignal, hist, folder, bkgFunction, minX, maxX ):
	"""docstring for FitterCombination"""

	outputDir = "Plots/"

	binSize = 10
	h1 = inFileBkg.Get(folder+'/' + hist)
	histoBkg = h1.Clone()
	hBkg = h1.Clone()
	hBkg1 = h1.Clone()
	h2 = inFileSignal.Get(folder+'/' + hist)
	histoSignal = h2.Clone(hist)
	hSignal = h2.Clone()

	PreFitStart= histoBkg.GetMaximumBin()*binSize-minX
	PreFitEnd  = histoBkg.GetMaximumBin()*binSize+maxX
	bkgParameters = Fitter( inFileBkg, 'QCD', hist, folder, P4, minX, maxX )
	print bkgParameters
			
	signalFitStart= histoSignal.GetMaximumBin()*binSize-30.
	signalFitEnd  = histoSignal.GetMaximumBin()*binSize+30.
	histoSignal.Fit( gaus, "MR","",signalFitStart,signalFitEnd)
	histoSignal.Fit( gaus, "MR","",signalFitStart,signalFitEnd)

	P4Gaus.SetParameter(0,bkgParameters[0])				
	P4Gaus.SetParameter(1,bkgParameters[1])
	P4Gaus.SetParameter(2,bkgParameters[2])
	P4Gaus.SetParameter(3,bkgParameters[3])
	P4Gaus.SetParameter(4,gaus.GetParameter(0))
	P4Gaus.SetParameter(5,gaus.GetParameter(1))
	P4Gaus.SetParameter(6,gaus.GetParameter(2))
	
	hBkg.Add( hSignal )
	hBkg.Fit( P4Gaus, "MRI", "", PreFitStart, PreFitEnd)
	hBkg.Fit( P4Gaus, "MRI", "", PreFitStart, PreFitEnd)
	hBkg.Fit( P4Gaus, "MRI", "", PreFitStart, PreFitEnd)
	gaus2 = TF1("gaus2", "gaus", signalFitStart, signalFitEnd);
	P4_2 = TF1("P4_2", "[0]*pow(1-x/13000.0,[1])/pow(x/13000.0,[2]+[3]*log(x/13000.))", PreFitStart, PreFitEnd);
	P4_2.SetParameter(0, P4Gaus.GetParameter(0) )
	P4_2.SetParameter(1, P4Gaus.GetParameter(1) )
	P4_2.SetParameter(2, P4Gaus.GetParameter(2) )
	P4_2.SetParameter(3, P4Gaus.GetParameter(3) )
	gaus2.SetParameter(0, P4Gaus.GetParameter(4) )
	gaus2.SetParameter(1, P4Gaus.GetParameter(5) )
	gaus2.SetParameter(2, P4Gaus.GetParameter(6) )
	P4GausParameters = [ P4Gaus.GetParameter(0), P4Gaus.GetParameter(1), P4Gaus.GetParameter(2), P4Gaus.GetParameter(3), P4Gaus.GetParameter(4), P4Gaus.GetParameter(5), P4Gaus.GetParameter(6) ]
	print P4GausParameters


	######## Calculating Pull and Residual
	hPull = hBkg.Clone()
	hResidual = hBkg.Clone()
	
	for bin in range(0,  hBkg.GetNbinsX()):
		hPull.SetBinContent(bin, 0.)
		hPull.SetBinError(bin, 0.)
		hResidual.SetBinContent(bin, 0.)
		hResidual.SetBinError(bin, 0.)
	
	for ibin in range(0, hBkg.GetNbinsX()):
	
		#binCont = hBkg1.GetBinContent(ibin)
		#binErr = hBkg1.GetBinError(ibin)
		binCont = hBkg.GetBinContent(ibin)
		binErr = hBkg.GetBinError(ibin)
		valIntegral = P4_2.Eval( hBkg1.GetBinCenter(ibin) ) ### +5 because binSize is 10
		#print binCont, binErr, valIntegral 
	
		diff = (binCont - valIntegral)/ valIntegral
		errDiff = diff * TMath.Sqrt( TMath.Power( P4Gaus.GetParError(0) / P4Gaus.GetParameter(0),2 ) + TMath.Power( P4Gaus.GetParError(1)/ P4Gaus.GetParameter(1), 2 )  + TMath.Power( P4Gaus.GetParError(2)/ P4Gaus.GetParameter(2), 2 )  + TMath.Power( P4Gaus.GetParError(3)/ P4Gaus.GetParameter(3), 2 ) )
		if (( ibin > PreFitStart/binSize) and (binCont != 0) and (ibin < PreFitEnd/binSize)):
			pull = (binCont - valIntegral)/ binErr
			#print pull
			hPull.SetBinContent(ibin, pull)
			hPull.SetBinError(ibin, 1.0)
	
			hResidual.SetBinContent(ibin, diff)
			#hResidual.SetBinError(ibin, binErr/valIntegral )
			hResidual.SetBinError(ibin, errDiff )#/valIntegral)


	######### Plotting Histograms
	c3 = TCanvas('c1', 'c1',  10, 10, 750, 1000 )
	pad1 = TPad("pad1", "Fit",0,0.50,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.25,1.00,0.50,-1);
	pad3 = TPad("pad3", "Residual",0,0,1.00,0.25,-1);
	pad1.Draw()
	pad2.Draw()
	pad3.Draw()

	pad1.cd()
	hBkg.GetXaxis().SetTitle("Average Mass [GeV]")
	hBkg.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	hBkg.GetYaxis().SetTitleOffset(1.2);
	hBkg.SetTitle("")
	hBkg.Sumw2()
	#hBkg.SetMaximum( 1.5 * hBkg.GetMaximum() )
	hBkg.Draw()
	hBkg.GetXaxis().SetRangeUser( 0, PreFitEnd+30 )
	P4Gaus.Draw("same")
	gaus2.SetLineColor(1)
	gaus2.Draw("same")
	P4_2.SetLineColor(3)
	P4_2.Draw("same")
	setSelection( 'QCD + RPV #tilde{t} 100 GeV', '13 TeV - '+PU, 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1, |cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.5 )


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
	hPull.GetXaxis().SetRangeUser( 0, PreFitEnd+30 )
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
	hResidual.SetMaximum(1)
	hResidual.GetXaxis().SetRangeUser( 0, PreFitEnd+30 )
	#hResidual.Sumw2()
	hResidual.Draw("e")
	line.Draw("same")
	c3.SaveAs(outputDir+hist+"_QCD_RPVSt100tojj_"+PU+"_FitP4Gaus.pdf")
	del c3

	return P4GausParameters

def rooFitter( inFileBkg, inFileSignal, hist, folder, MASS, outputRootFile, minX, maxX ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )

	P4GausParameters = FitterCombination( inFileBkg, inFileSignal, hist, folder, P4, minX, maxX )
	
	myWS = RooWorkspace("myWS")

	''' CONFIG FOR 732 WORKS PERFECT
	x = RooRealVar( "x", "x", 50., 190. )
	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[50,190],p1[2116,2117],p2[-62,63],p3[-5,-4]})")
	myWS.factory("Gaussian:sig_pdf(x, mean[93,94], sigma[5,6])")
	myWS.factory("SUM:model(nsig[0,100000]*sig_pdf, nbkg[0,1000000]*bkg_pdf)")
	myWS.factory("SUM:model_b(nbkg[0,1000000]*bkg_pdf)")

	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[70,600], p1[-4000,4000],p2[-300,300],p3[0,40]})")

	'''

	myWS.factory("x[50,200]")
	myWS.var("x").setBins(15)
	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1["+str(P4GausParameters[1])+"],p2["+str(P4GausParameters[2])+"],p3["+str(P4GausParameters[3])+"]})")
	myWS.factory("Gaussian:sig_pdf(x, mean["+str(MASS)+"], sigma[0,50])")
	#myWS.factory("Gaussian:sig_pdf(x, mean[93.29], sigma[5.52])")
	#myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1[-2000,1000],p2[-200,200],p3[-20,20]})")
	#myWS.factory("Gaussian:sig_pdf(x, mean[90,100], sigma[0,10])")
	myWS.factory("SUM:model_bkg( nbkg[0,100000]*bkg_pdf )")
	#myWS.factory("SUM:model_sig( nsig[0,10000]*sig_pdf )")
	myWS.factory("SUM:model( nbkg[0,100000]*bkg_pdf , nsig[0,100000]*sig_pdf)")
	myWS.Print()

	bkg_pdf = myWS.pdf("model_bkg")
	#signal_pdf = myWS.pdf("model_sig")
	#bkg_pdf = myWS.pdf("bkg_pdf")
	#signal_pdf = myWS.pdf("sig_pdf")
	pdf = myWS.pdf("model")

	mass = RooArgList( myWS.var("x") )
	h1 = inFileBkg.Get(folder+'/' + hist)
	hBkg = h1.Clone()
	hData = h1.Clone()
	bkg = RooDataHist( 'bkg', 'bkg', mass, hBkg)
	h2 = inFileSignal.Get(folder+'/' + hist)
	hSignal = h2.Clone()
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
	#bkg_pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
	bkg_pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	xframe.SetMaximum(100000)
	xframe.SetMinimum(0.00001)
	c1.SaveAs('Plots/'+hist+"_QCD_"+PU+"_FitP4Gaus_rooFit.pdf")
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
	c2.SaveAs('Plots/'+hist+"_RPVSt100tojj_"+PU+"_FitP4Gaus_rooFit.pdf")
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
	pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
	pdf.plotOn( xframe, RooFit.Components("sig_pdf"), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	c1.SaveAs('Plots/'+hist+"_QCD_RPVSt100tojj_"+PU+"_FitP4Gaus_rooFit.pdf")
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
	c1.SaveAs('Plots/'+hist+"_PseudoExp_"+PU+"_FitP4Gaus_rooFit.pdf")
	del c1
	'''

	####### QCD AS DATA
	data_obs = RooDataHist( 'data_obs', 'data_obs', mass, hBkg)

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

	myWS.writeToFile(outputRootFile, true )
	myWS.Print()

	####### Creating datacard
	outputfile = open('/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_1_5/src/MyLimits/datacard.txt','w')
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
	myWS.writeToFile("Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_"+PU+"_rooFitTree.root", true )
	myWS.Print()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--process', action='store', default='Full', help='Type of fit to use.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-m', '--mass', action='store', type=int, default=100, help='Decay, example: jj, bj.' )
	parser.add_argument('-pu', '--PU', action='store', default='PU20bx25', help='PU, example: PU40bx25.' )
	parser.add_argument('-l', '--lumi', action='store', default='1', help='Luminosity, example: 1.' )
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
	inFileBkg = TFile('Rootfiles/v09/RUNAnalysis_QCDPtAll_PHYS14_'+PU+'_v03_v09.root')
	inFileSignal = TFile('Rootfiles/v09/RUNAnalysis_RPVSt100tojj_PHYS14_'+PU+'_v03_v09.root')
	#inFileData = TFile('Rootfiles/RUNAnalysis_QCDPtAll_RPVSt100tojj_PHYS14_'+PU+'_v03_v06.root')
	inFileData = TFile('Rootfiles/v09/RUNAnalysis_QCDPtAll_PHYS14_'+PU+'_v03_v09.root')
	outputRootFile = '/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_3_1_patch2/src/RUNA/RUNAnalysis/test/Rootfiles/workspace_QCD_RPVSt'+str(MASS)+'tojj_FitP4Gaus_'+PU+'_rooFit_'+lumi+'fb.root'

	###### Input parameters
	hist = 'massAve_cutSubjetPtRatio'  # str ( sys.argv[1] )
	folder = "BoostedAnalysisPlotsPruned"      # str ( sys.argv[2] )
	

	if 'simple' in process:
		Fitter( inFileBkg, 'QCDALL', hist, folder, P4, 30.0, 400.0 )
		#Fitter( inFileSignal, 'RPVSt100tojj', hist, folder, 'gaus', 50.0, 50.0 )

	elif 'full' in process:
		dummyReturn = FitterCombination( inFileBkg, inFileSignal, hist, folder, P4, 30.0, 400.0 )
	elif 'rooFit' in process:
		rooFitter( inFileBkg, inFileSignal, hist, folder, MASS, outputRootFile, 30.0, 400.0  )
	else:
		rooFitterTree( inFileBkg, inFileSignal, inFileData, hist, folder )

	


