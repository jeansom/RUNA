#!/usr/bin/env python

from ROOT import *
from ROOT import RooFit, RooStats
from setTDRStyle import *
import warnings

gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')

gStyle.SetOptFit()
gStyle.SetStatY(0.94)
gStyle.SetStatX(0.9)
gStyle.SetStatW(0.15)
gStyle.SetStatH(0.15) 

def frequentistCalculator(  ):
	"""Compute the significance (hypothesis test) using a frequentist calculator"""

	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )

	inFile = TFile('Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_rooFit_1fb.root')
	myWS = inFile.Get("myWS") 
	data = myWS.data("data_obs")

	sbModel = myWS.obj("modelConfig") 
	sbModel.SetName("S+B Model")
	#sbModel.GetParametersOfInterest().first().setVal(5.)
	#sbModel.GetParametersOfInterest().first().setConstant()
	sbModel.SetSnapshot( sbModel.GetParametersOfInterest() )

	bModel = sbModel.Clone()
	bModel.SetName("B Model")
	bModel.GetParametersOfInterest().first().setVal(0.)
	bModel.GetParametersOfInterest().first().setConstant()
	bModel.SetSnapshot( bModel.GetParametersOfInterest() )

	#c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	#test = data.reduce( RooFit.Name('test'))
	#testHisto = TH1D('test','test', 10, 80, 180)
	#testHisto = test.fillHistogram( testHisto, RooArgList(x) )
	#testHisto.Draw()

	#x = RooRealVar( "x", "x", 50., 180. )
	#testHisto = sbModel.GetPdf() 
	#xframe = x.frame()
	#testHisto.plotOn( xframe  )

	#c1.SaveAs("test.pdf")


	# create the AsymptoticCalculator from data,alt model, null model
	################################### Here, roostats is fitting again and the parameters are wrong.
	asym_calc = RooStats.AsymptoticCalculator(data, bModel, sbModel)
	asym_calc.SetOneSidedDiscovery( True )
	result = asym_calc.GetHypoTest()
	result.Print()

	tw = TStopwatch()
	tw.Start()
	# Frequentist calculator
	fc = RooStats.FrequentistCalculator(data, bModel, sbModel)
	fc.SetToys(10,10) 

	# create the test statistics
	profll = RooStats.ProfileLikelihoodTestStat( sbModel.GetPdf() )
	profll.SetOneSidedDiscovery( True )

	# configure  ToyMCSampler and set the test statistics
	toymcs = RooStats.ToyMCSampler( fc.GetTestStatSampler()  )
	toymcs.SetTestStatistic( profll )

	pc = RooStats.ProofConfig( myWS, 10, "", 0 ) #ROOT.kFALSE)
	toymcs.SetProofConfig(pc)    # enable proof

	########################################## change to 0
	if not sbModel.GetPdf().canBeExtended(): toymcs.SetNEventsPerToy(0)

	# run the test
	fqResult = RooStats.HypoTestResult( fc.GetHypoTest() )
	fqResult.Print()
	tw.Stop()
	print tw.CpuTime(), tw.RealTime()

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	plot = RooStats.HypoTestPlot( fqResult )
	plot.SetLogYaxis(true)
	plot.Draw()
	c1.SaveAs("Plots/Significance.pdf")
	

if __name__ == '__main__':


	#inFileBkg = TFile('Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_rooFit.root')

	frequentistCalculator( )

