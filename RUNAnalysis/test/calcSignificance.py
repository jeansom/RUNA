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

	inFile = TFile('Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_rooFit.root')
	myWS = inFile.Get("myWS") 
	data = myWS.data("data")

	sbModel = myWS.obj("modelConfig") 
	sbModel.SetName("S+B Model")
	#sbModel.GetParametersOfInterest().first().setVal(5.)
	#sbModel.GetParametersOfInterest().first().setConstant()
	sbModel.SetSnapshot( sbModel.GetParametersOfInterest() )

	bModel = sbModel.Clone()
	bModel.SetName("B Model")
	bModel.GetParametersOfInterest().first().setVal(0.)
	#bModel.GetParametersOfInterest().first().setConstant()
	bModel.SetSnapshot( bModel.GetParametersOfInterest() )


	# create the AsymptoticCalculator from data,alt model, null model
	asym_calc = RooStats.AsymptoticCalculator(data, bModel, sbModel, True)
	#asym_calc.SetOneSidedDiscovery(True)
	result = asym_calc.GetHypoTest()
	result.Print()

	# Frequentist calculator
	fc = RooStats.FrequentistCalculator(data, bModel, sbModel)
	fc.SetToys(100,50)

	# create the test statistics
	profll = RooStats.ProfileLikelihoodTestStat( sbModel.GetPdf() )
	profll.SetOneSidedDiscovery( True )

	# configure  ToyMCSampler and set the test statistics
	toymcs = RooStats.ToyMCSampler( fc.GetTestStatSampler()  )
	toymcs.SetTestStatistic( profll )

	if not sbModel.GetPdf().canBeExtended(): toymcs.SetNEventsPerToy(1)

	# run the test
	fqResult = RooStats.HypoTestResult( fc.GetHypoTest() )
	fqResult.Print()
	

if __name__ == '__main__':


	#inFileBkg = TFile('Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_rooFit.root')

	frequentistCalculator( )

	


