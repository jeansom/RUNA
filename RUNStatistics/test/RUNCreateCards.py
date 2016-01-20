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
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python') 
	import CMS_lumi as CMS_lumi 
	from histoLabels import labels, labelAxis 
	import tdrstyle as tdrstyle

currentDir = os.getcwdu()
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

def shapeCards( histosFile, signalSample, hist, signalMass, outputRootFile ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )
	
	minX = signalMass - 100
	maxX = signalMass + 100
	hSignal = histosFile.Get(hist+'_'+signalSample+'_A')
	hSignal.Scale(1/hSignal.Integral())
	sigAcc = hSignal.Integral(hSignal.GetXaxis().FindBin(minX), hSignal.GetXaxis().FindBin( maxX )) #/hSignal.Integral(1,hSignal.GetXaxis().FindBin( maxX) )

	mass = RooRealVar( 'mass', 'mass', minX, maxX  )
	rooSigHist = RooDataHist( 'rooSigHist', 'rooSigHist', RooArgList(mass), hSignal )
	rooSigHist.Print()

	signal = RooHistPdf('signal','signal',RooArgSet(mass),rooSigHist)
        signal.Print()
        signal_norm = RooRealVar('signal_norm','signal_norm',0,-1e+05,1e+05)
        #if args.fitBonly: signal_norm.setConstant()
        signal_norm.Print()

	#hBkg = histosFile.Get(hist+'_DATA_BCD')
	hBkg = histosFile.Get(hist+'_QCDPtAll_BCD')
	hBkg.Scale(1/hBkg.Integral())
	rooBkgHist = RooDataHist( 'rooBkgHist', 'rooBkgHist', RooArgList(mass), hBkg )
	rooBkgHist.Print()
	#hBkg.Add( hSignal )
	background = RooHistPdf('background','background',RooArgSet(mass),rooBkgHist)
        background.Print()
	bkgAcc = hBkg.Integral( hBkg.GetXaxis().FindBin( minX ), hBkg.GetXaxis().FindBin( maxX )) #/hBkg.Integral(1,hBkg.GetXaxis().FindBin( maxX) )

        # S+B model
        #model = RooAddPdf("model","s+b",RooArgList(background,signal),RooArgList(background_norm,signal_norm))

	#hData = histosFile.Get(hist+'_DATA_A')
	hData = histosFile.Get(hist+'_QCDPtAll_A')
	hData.Scale(1/hData.Integral())
        rooDataHist = RooDataHist('rooDatahist','rooDatahist',RooArgList(mass),hData)
        rooDataHist.Print()

	#res = model.fitTo(rooDataHist, RooFit.Save(kTRUE), RooFit.Strategy(0))
	#res.Print()

	myWS = RooWorkspace("myWS")
	getattr(myWS,'import')(rooSigHist,RooFit.Rename("signal"))
        getattr(myWS,'import')(rooBkgHist,RooFit.Rename("background"))
        getattr(myWS,'import')(signal_norm)
        getattr(myWS,'import')(rooDataHist,RooFit.Rename("data_obs"))
        myWS.Print()
        myWS.writeToFile(outputRootFile, True)
 # -----------------------------------------
        # write a datacard

        #datacard = open('/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_1_5/src/MyLimits/datacard_RPVStop'+str(MASS)+'.txt','w')
        datacard = open( currentDir+'/Datacards/datacard_'+signalSample+'.txt','w')
        datacard.write('imax 1\n')
        datacard.write('jmax 1\n')
        datacard.write('kmax *\n')
        datacard.write('---------------\n')
	datacard.write("shapes * * "+currentDir+'/'+outputRootFile+" myWS:$PROCESS \n")
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
        datacard.write('signal_norm  flatParam\n')
        #datacard.write('p1  flatParam\n')
        datacard.close()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--process', action='store', default='Full', help='Type of fit to use.' )
	#parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-m', '--mass', action='store', type=int, default=100, help='Decay, example: jj, bj.' )
	parser.add_argument('-l', '--lumi', action='store', default='1000', help='Luminosity, example: 1.' )
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	process = args.process
	lumi = args.lumi
	MASS = args.mass

	CMS_lumi.lumi_13TeV = '2.43 fb^{-1}'

	signalSample = 'RPVSt'+str(MASS)
	fileHistos = '../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+signalSample+'_allHistos_v0.root'
	#outputRootFile = '/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_4_5_patch1/src/RUNA/RUNAnalysis/test/Rootfiles/workspace_QCD_RPVSt'+str(MASS)+'tojj_FitP4Gaus_'+PU+'_rooFit_'+lumi+'fb.root'
	outputRootFile = 'Rootfiles/workspace_'+signalSample+'.root'

	###### Input parameters
	hist = 'massAve_massAsymVsdeltaEtaDijet'
	minFit = 240
	maxFit = 1000

	CMS_lumi.extraText = "Preliminary Simulation"
	p = Process( target=shapeCards, args=( TFile.Open(fileHistos), signalSample, hist, MASS, outputRootFile ) )
	p.start()
	p.join()

	


