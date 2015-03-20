#!/usr/bin/env python

###################
### Make Fitting
###################

from ROOT import RooFit, RooStats
from ROOT import *
from setTDRStyle import *
from array import array
import glob,sys, os
import warnings

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
sigmoid = TF1("sigmoid", "mTilde/ (sqrt(1+ pow(mTilde,2)))", 0, 1000 )
landau = TF1("landau","[0]*TMath::Landau(-x,[1],[2])",50,300)
gaus = TF1("gaus", "gaus", 0, 2000);
P4Gaus = TF1("P4Gaus", "[0]*pow(1-x/13000.0,[1])/pow(x/13000.0,[2]+[3]*log(x/13000.))+gaus(4)",50,500);

def Fitter( Signal, outputDir, hist, folder, fitFunction, minX, maxX ):
	"""Main Fitter"""

	inputFile = 'Rootfiles/RUNAPlots_'+Signal+'_'+PU+'.root'
	binSize = 1
	massBins = [0, 30, 60, 90, 120, 150, 180, 210, 250, 290, 330, 370, 410, 460, 510, 560, 610, 670, 730, 790, 860, 930, 1000, 1080, 1160, 1240, 1330, 1420, 1520, 1620, 1730, 1840, 2000]

	inFile = TFile(inputFile)

	h1 = inFile.Get(folder+'/' + hist)
	histo = h1.Clone(hist)

	PreFitStart= histo.GetMaximumBin()*binSize-minX
	PreFitEnd  = histo.GetMaximumBin()*binSize+maxX
	#fitFunction.SetParameter(1, histo.GetMaximumBin()*binSize)
	#fitFunction.SetParameter(2, 10000.)
	histo.Fit(fitFunction,"MR","",PreFitStart,PreFitEnd)
	if 'QCD' in Signal: fitFunction.SetParameter(0,1)
	histo.Fit(fitFunction,"MR","",PreFitStart,PreFitEnd)
	histo.Fit(fitFunction,"MR","",PreFitStart,PreFitEnd)
	#fitFunction.SetParameter(1,-5)
	#fitFunction.SetParameter(1, -5)
	#fitFunction.SetParameter(2, 15)   # max 11.9
	#fitFunction.SetParameter(3, 1.2)   # max 6

			
	######### Plotting Histograms
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	gStyle.SetOptFit()
	gStyle.SetStatY(0.94)
	gStyle.SetStatX(0.9)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.15) 
	histo.GetXaxis().SetTitle("Average Mass [GeV]")
	histo.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	histo.GetYaxis().SetTitleOffset(1.2);
	histo.SetTitle("")
	histo.Sumw2()
	histo.Draw()
	setSelection( Signal, '13 TeV - '+PU, 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.5 )
	c1.SaveAs(outputDir+hist+"_"+Signal+"_"+PU+"_Fit.pdf")
	del c1

def FitterCombination( inFileBkg, inFileSignal, hist, folder, bkgFunction ):
	"""docstring for FitterCombination"""

	outputDir = "Plots/"

	binSize = 10
	h1 = inFileBkg.Get(folder+'/' + hist)
	histoBkg = h1.Clone(hist)
	histoBkg.Scale( 10 )
	hBkg = h1.Clone(hist)
	hBkg.Scale( 10 )
	h2 = inFileSignal.Get(folder+'/' + hist)
	histoSignal = h2.Clone(hist)
	histoSignal.Scale( 10 )
	hSignal = h2.Clone(hist)
	hSignal.Scale( 10 )

	bkgFitStart= 60#histoBkg.GetMaximumBin()*binSize-30.   #### I found that 60 and 190 are good values for the fit by doing several test by hand.
	bkgFitEnd  = 190 #histoBkg.GetMaximumBin()*binSize+300.
	histoBkg.Fit(bkgFunction,"MR","",bkgFitStart,bkgFitEnd)
	bkgFunction.SetParameter(0,1.)
	histoBkg.Fit(bkgFunction,"MR","",bkgFitStart,bkgFitEnd)
	histoBkg.Fit(bkgFunction,"MR","",bkgFitStart,bkgFitEnd)
	histoBkg.Fit(bkgFunction,"MR","",bkgFitStart,bkgFitEnd)
			
	signalFitStart= histoSignal.GetMaximumBin()*binSize-40.
	signalFitEnd  = histoSignal.GetMaximumBin()*binSize+40.
	histoSignal.Fit( gaus, "MR","",signalFitStart,signalFitEnd)
	histoSignal.Fit( gaus, "MR","",signalFitStart,signalFitEnd)
	histoSignal.Fit( gaus, "MR","",signalFitStart,signalFitEnd)

	P4Gaus.SetParameter(0,bkgFunction.GetParameter(0))				
	P4Gaus.SetParameter(1,bkgFunction.GetParameter(1))
	P4Gaus.SetParameter(2,bkgFunction.GetParameter(2))
	P4Gaus.SetParameter(3,bkgFunction.GetParameter(3))
	P4Gaus.SetParameter(4,gaus.GetParameter(0))
	P4Gaus.SetParameter(5,gaus.GetParameter(1))
	P4Gaus.SetParameter(6,gaus.GetParameter(2))
	
	hBkg.Add( hSignal )
	hBkg.Fit( P4Gaus, "MRI", "", bkgFitStart, bkgFitEnd)
	hBkg.Fit( P4Gaus, "MRI", "", bkgFitStart, bkgFitEnd)
	hBkg.Fit( P4Gaus, "MRI", "", bkgFitStart, bkgFitEnd)
	gaus2 = TF1("gaus2", "gaus", signalFitStart, signalFitEnd);
	P4_2 = TF1("P4_2", "[0]*pow(1-x/13000.0,[1])/pow(x/13000.0,[2]+[3]*log(x/13000.))", bkgFitStart, bkgFitEnd);
	P4_2.SetParameter(0, P4Gaus.GetParameter(0) )
	P4_2.SetParameter(1, P4Gaus.GetParameter(1) )
	P4_2.SetParameter(2, P4Gaus.GetParameter(2) )
	P4_2.SetParameter(3, P4Gaus.GetParameter(3) )
	gaus2.SetParameter(0, P4Gaus.GetParameter(4) )
	gaus2.SetParameter(1, P4Gaus.GetParameter(5) )
	gaus2.SetParameter(2, P4Gaus.GetParameter(6) )


	######## Calculating Pull and Residual
	hPull = hBkg.Clone()
	hResidual = hBkg.Clone()
	
	for bin in range(0,  hBkg.GetNbinsX()):
		hPull.SetBinContent(bin, 0.)
		hPull.SetBinError(bin, 0.)
		hResidual.SetBinContent(bin, 0.)
		hResidual.SetBinError(bin, 0.)
	
	for ibin in range(0, hBkg.GetNbinsX()):
	
		binCont = hBkg.GetBinContent(ibin)
		binErr = hBkg.GetBinError(ibin)
		valIntegral = P4_2.Eval( hBkg.GetBinCenter(ibin) ) ### +5 because binSize is 10
		#print binCont, binErr, valIntegral 
	
		diff = (binCont - valIntegral)/ valIntegral
		errDiff = diff * TMath.Sqrt( TMath.Power( P4Gaus.GetParError(0) / P4Gaus.GetParameter(0),2 ) + TMath.Power( P4Gaus.GetParError(1)/ P4Gaus.GetParameter(1), 2 )  + TMath.Power( P4Gaus.GetParError(2)/ P4Gaus.GetParameter(2), 2 )  + TMath.Power( P4Gaus.GetParError(3)/ P4Gaus.GetParameter(3), 2 ) )
		if (( ibin >= bkgFitStart/binSize) and (binCont != 0) and (ibin <= bkgFitEnd/binSize)):
			pull = (binCont - valIntegral)/ binErr
			#print pull
			hPull.SetBinContent(ibin, pull)
			hPull.SetBinError(ibin, 1.0)
	
			hResidual.SetBinContent(ibin, diff)
			#hResidual.SetBinError(ibin, binErr/valIntegral )
			hResidual.SetBinError(ibin, errDiff )#/valIntegral)


	######### Plotting Histograms
	'''
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	histoBkg.GetXaxis().SetTitle("Average Mass [GeV]")
	histoBkg.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	histoBkg.GetYaxis().SetTitleOffset(1.2);
	histoBkg.SetTitle("")
	histoBkg.Sumw2()
	histoBkg.Draw()
	setSelection( 'QCD Pt80to1000', '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.5 )
	c1.SaveAs(outputDir+hist+"_QCD_FitP4.pdf")
	del c1

	c2 = TCanvas('c2', 'c2',  10, 10, 750, 500 )
	histoSignal.GetXaxis().SetTitle("Average Mass [GeV]")
	histoSignal.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	histoSignal.GetYaxis().SetTitleOffset(1.2);
	histoSignal.SetTitle("")
	histoSignal.Sumw2()
	histoSignal.Draw()
	setSelection( 'RPV Stop 100 GeV', '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.5 )
	c2.SaveAs(outputDir+hist+"_RPVSt100tojj_FitGauss.pdf")
	del c2

	c3 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	hBkg.GetXaxis().SetTitle("Average Mass [GeV]")
	hBkg.GetYaxis().SetTitle("Events / 10 GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	hBkg.GetYaxis().SetTitleOffset(1.2);
	hBkg.SetTitle("")
	hBkg.Sumw2()
	#hBkg.SetMaximum( 1.5 * hBkg.GetMaximum() )
	hBkg.Draw()
	P4Gaus.Draw("same")
	gaus2.SetLineColor(1)
	gaus2.Draw("same")
	P4_2.SetLineColor(3)
	P4_2.Draw("same")
	setSelection( 'QCD + RPV #tilde{t} 100 GeV', '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1, |cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', yMax=0.4 )
	c3.SaveAs(outputDir+hist+"_QCD_RPVSt100tojj_FitP4Gaus.pdf")
	del c3
	'''
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
	hPull.SetMaximum(3)
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
	#hResidual.Sumw2()
	hResidual.Draw("e")
	line.Draw("same")
	c3.SaveAs(outputDir+hist+"_QCD_RPVSt100tojj_"+PU+"_FitP4Gaus.pdf")
	del c3

def rooFitter( inFileBkg, inFileSignal, hist, folder ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )
	
	myWS = RooWorkspace("myWS")

	x = RooRealVar( "x", "x", 50., 180. )
	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[50,180],p1[0,1000],p2[0,100],p3[0,10]})")
	myWS.factory("Gaussian:sig_pdf(x, mean[90,110], sigma[0,10])")
	myWS.factory("SUM:model(nsig[0,10000]*sig_pdf, nbkg[0,1000000]*bkg_pdf)")
	myWS.Print()

	#x = myWS.var("x")
	#mass = myWS.var("mass")
	pdf = myWS.pdf("model")

	mass = RooArgList( x )
	h1 = inFileBkg.Get(folder+'/' + hist)
	hBkg = h1.Clone()
	#hBkg.Scale( 10 )
	hData = h1.Clone()
	#hData.Scale( 10 )
	bkg = RooDataHist( 'bkg', 'bkg', mass, hBkg)
	h2 = inFileSignal.Get(folder+'/' + hist)
	hSignal = h2.Clone()
	#hSignal.Scale( 10 )
	signal = RooDataHist( 'signal', 'signal', mass, hSignal)
	hData.Add( hSignal )
	#data = RooDataHist( 'data', 'data', mass, hData)
	data_obs = RooDataHist( 'data_obs', 'data_obs', mass, hData)
	getattr( myWS, 'import')(data_obs)

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	xframe = x.frame()
	data_obs.plotOn( xframe )
	xframe.Draw()
	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	pdf.fitTo( data_obs, RooFit.Save(true) ) #, RooFit.Minimizer("Minuit2", "Migrad") )
	#pdf.fitTo( data_obs, RooFit.Save(true) , RooFit.Minimizer("Minuit2", "Migrad"), RooFit.SumW2Error(kTRUE) )
	pdf.plotOn( xframe )
	pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
	pdf.plotOn( xframe, RooFit.Components("sig_pdf"), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	c1.SaveAs('Plots/'+hist+"_QCD_RPVSt100tojj_"+PU+"_FitP4Gaus_rooFit.pdf")
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
	myWS.writeToFile("Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_"+PU+"_rooFit_1fb.root", true )
	myWS.Print()

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
	#mass = myWS.var("mass")
	pdf = myWS.pdf("model")

	#mass = RooArgList( x )
	massAveForFit = RooRealVar( "massAveForFit", "massAveForFit", 50., 180. )
	bkgTree = inFileBkg.Get(folder+'/RUNATree' )
	bkg = RooDataSet( "bkg", "bkg", RooArgSet(massAveForFit), RooFit.Import( bkgTree ) )
	signalTree = inFileSignal.Get(folder+'/RUNATree' )
	signal = RooDataSet( "signal", "signal", RooArgSet(massAveForFit), RooFit.Import( signalTree ) )
	dataTree = inFileData.Get(folder+'/RUNATree' )
	data_obs = RooDataSet( "data_obs", "data_obs", RooArgSet(massAveForFit), RooFit.Import( dataTree ) )
	
	getattr( myWS, 'import')(data_obs)

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	xframe = massAveForFit.frame()
	data_obs.plotOn( xframe )
	xframe.Draw()
	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
	pdf.fitTo( data_obs, RooFit.Save(true), RooFit.Minimizer("Minuit2", "Migrad") )
	#pdf.fitTo( data_obs, RooFit.Save(true) , RooFit.Minimizer("Minuit2", "Migrad"), RooFit.SumW2Error(kTRUE) )
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

	try: 
		option = sys.argv[1]
		PU = sys.argv[2]
	except IndexError: 
		option = ''
		PU = 'PU40bx50'

	inFileBkg = TFile('Rootfiles/RUNAPlots_QCDALL_'+PU+'.root')
	inFileSignal = TFile('Rootfiles/RUNAPlots_RPVSt100tojj_'+PU+'.root')
	inFileData = TFile('Rootfiles/RUNAPlots_QCDALL_RPVSt100tojj_'+PU+'.root')

	###### Input parameters
	hist = 'massAve_cutSubjetPtRatio'  # str ( sys.argv[1] )
	folder = "AnalysisPlotsPruned"      # str ( sys.argv[2] )

	if 'simple' in option:
		Fitter( 'QCDALL', "Plots/", hist, folder, P4, 30.0, 200.0 )
		Fitter( 'RPVSt100tojj', "Plots/", hist, folder, 'gaus', 50.0, 50.0 )

	elif 'full' in option:
		FitterCombination( inFileBkg, inFileSignal, hist, folder, P4 )
	elif 'rooFit' in option:
		rooFitter( inFileBkg, inFileSignal, hist, folder )
	else:
		rooFitterTree( inFileBkg, inFileSignal, inFileData, hist, folder )

	


