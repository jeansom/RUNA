#!/usr/bin/env python

################################
### Creating datacards
################################

from ROOT import *
from ROOT import RooRealVar, RooDataHist, RooArgList, RooArgSet, RooAddPdf, RooFit, RooGenericPdf, RooWorkspace, RooMsgService, RooHistPdf, RooGaussian
from array import array
from collections import OrderedDict
import argparse
import glob,sys, os
import warnings
import random
import numpy as np
from multiprocessing import Process
try: 
	from RUNA.RUNAnalysis.scaleFactors import *
	from RUNA.RUNAnalysis.commonFunctions import *
except ImportError: 
	sys.path.append('../python') 
	from scaleFactors import *
	from commonFunctions import *
sys.path.append('../../RUNAnalysis/test') 
from RUNBkgEstimation import *


currentDir = os.getcwdu()
gROOT.Reset()
gROOT.SetBatch()
gSystem.SetIncludePath('-I$ROOFITSYS/include')
if os.access('RooPowerFunction.cxx', os.R_OK): ROOT.gROOT.ProcessLine('.L RooPowerFunction.cxx+')

#xline = array('d', [0,2000])
#yline = array('d', [0,0])
#line = TGraph(2, xline, yline)
#line.SetLineColor(kRed)


def signalUnc( hSignal, signalMass ):
	"""docstring for signalUnc"""

	######## Signal uncertainties
        hSigSyst = {}
        signalCDF = TGraph(hSignal.GetNbinsX()+1)

        # JES and JER uncertainties
	if args.jesUnc or args.jerUnc:
		signalCDF.SetPoint(0,0.,0.)
		integral = 0.
		for i in range(1, hSignal.GetNbinsX()+1):
			x = hSignal.GetXaxis().GetBinLowEdge(i+1)
			integral = integral + hSignal.GetBinContent(i)
			signalCDF.SetPoint(i,x,integral)

		if args.jesUnc:
			print ' |---> Adding JES'
			hSigSyst['JESUp'] = hSignal.Clone()
			hSigSyst['JESDown'] = hSignal.Clone()

		if args.jerUnc:
			print ' |---> Adding JER'
			hSigSyst['JERUp'] = hSignal.Clone()
			hSigSyst['JERDown'] = hSignal.Clone()


        # reset signal histograms
        for key in hSigSyst: hSigSyst[key].Reset()

        # produce JES signal shapes
        if args.jesUnc:
		for q in range(1, hSignal.GetNbinsX()+1):
			xLow = hSignal.GetXaxis().GetBinLowEdge(q)
			xUp = hSignal.GetXaxis().GetBinLowEdge(q+1)
			jes = 1. - jesValue
			xLowPrime = jes*xLow
			xUpPrime = jes*xUp
			hSigSyst['JESDown'].SetBinContent(q, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
			jes = 1. + jesValue
			xLowPrime = jes*xLow
			xUpPrime = jes*xUp
			hSigSyst['JESUp'].SetBinContent(q, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))

        # produce JER signal shapes
	if args.jerUnc:
		for i in range(1, hSignal.GetNbinsX()+1):
			xLow = hSignal.GetXaxis().GetBinLowEdge(i)
			xUp = hSignal.GetXaxis().GetBinLowEdge(i+1)
			jer = 1. - jerValue
			xLowPrime = jer*(xLow-float(signalMass))+float(signalMass)
			xUpPrime = jer*(xUp-float(signalMass))+float(signalMass)
			hSigSyst['JERDown'].SetBinContent(i, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
			jer = 1. + jerValue
			xLowPrime = jer*(xLow-float(signalMass))+float(signalMass)
			xUpPrime = jer*(xUp-float(signalMass))+float(signalMass)
			hSigSyst['JERUp'].SetBinContent(i, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))

	return hSigSyst

def shapeCards( datahistosFile, histosFile, signalFile, signalSample, hist, signalMass, minMass, maxMass, outputName, outputFileTheta ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )

	############################################################# DATA
	#hData = histosFile.Get('massAve_deltaEtaDijet_QCDPtAll')
	#hData = datahistosFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_DATA_ABCDProj')
	dataFile = TFile( datahistosFile )
	hData = dataFile.Get(hist+'_DATA')
	hData.Rebin( args.reBin )
	#hData = hData.Rebin( len( boostedMassAveBins )-1, hData.GetName(), boostedMassAveBins )
	#hData = histosFile.Get(hist+'_QCDPtAll_A')
	#hData.Add(htmpSignal)
	#hData.Scale(1/hData.Integral())
	#maxMass = boostedMassAveBins[ hData.FindLastBinAbove( 0, 1) ]
	#minMass = signalMass-30
	#maxMass = signalMass+30
	massAve = RooRealVar( 'massAve', 'massAve', minMass, maxMass  )
	#massAveData = RooRealVar( 'massAveData', 'massAveData', minMass, maxMass  )
	rooDataHist = RooDataHist('rooDatahist','rooDatahist',RooArgList(massAve), hData ) # if isData else hPseudo )
	rooDataHist.Print()
	############################################################################################

	
	####################### Signal 
	if 'gaus' in args.technique: 
		hSignal = TH1F( 'massAve_RPVStop', 'massAve_RPVStop', maxMass/args.reBin, minMass, maxMass)
		for q in range( hSignal.GetNbinsX()+1 ):
			gausEval = signalFile.Eval( hSignal.GetXaxis().GetBinCenter( q ) )
			hSignal.SetBinContent( q, gausEval )

		#meanSig = RooRealVar( 'meanSig', 'mean of signal', sigGaus.GetParameter( 1 ) )
		#sigmaSig = RooRealVar( 'sigmaSig', 'sigma of signal', sigGaus.GetParameter( 2 ) )
		#signalPdf = RooGaussian( 'signal', 'signal', massAve, meanSig, sigmaSig )
		#signalPdf.Print()
	else:
		signalHistosFile = TFile( signalFile )
		hSignal = signalHistosFile.Get(hist+'_'+signalSample)
		hSignal.Rebin( args.reBin )

	#hSignal = hSignal.Rebin( len( boostedMassAveBins )-1, hSignal.GetName(), boostedMassAveBins )
	signalXS = search(dictXS, 'RPVStopStopToJets_UDD312_M-'+str(signalMass) )
	rooSigHist = RooDataHist( 'rooSigHist', 'rooSigHist', RooArgList(massAve), hSignal )
	sigAcc = rooSigHist.sumEntries()  #round(hSignal.Integral( hSignal.GetXaxis().FindBin( minMass ), hSignal.GetXaxis().FindBin( maxMass )), 2)
	rooSigHist.Print()

	#signal = RooHistPdf('signal','signal',RooArgSet(massAve),rooSigHist)
	#signal.Print()
	#signal_norm = RooRealVar('signal_norm','signal_norm',0,-1e+04,1e+04)
	#if args.fitBonly: signal_norm.setConstant()
	#signal_norm.Print()

	######## Signal uncertainties
	'''
        hSigSyst = {}
        hSigSystDataHist = {}
        signalCDF = TGraph(hSignal.GetNbinsX()+1)

        # JES and JER uncertainties
	if args.jesUnc or args.jerUnc:
		signalCDF.SetPoint(0,0.,0.)
		integral = 0.
		for i in range(1, hSignal.GetNbinsX()+1):
			x = hSignal.GetXaxis().GetBinLowEdge(i+1)
			integral = integral + hSignal.GetBinContent(i)
			signalCDF.SetPoint(i,x,integral)

		if args.jesUnc:
			print ' |---> Adding JES'
			hSigSyst['JESUp'] = hSignal.Clone()
			hSigSyst['JESDown'] = hSignal.Clone()

		if args.jerUnc:
			print ' |---> Adding JER'
			hSigSyst['JERUp'] = hSignal.Clone()
			hSigSyst['JERDown'] = hSignal.Clone()


        # reset signal histograms
        for key in hSigSyst:
		hSigSyst[key].Reset()
		hSigSyst[key].SetName(hSigSyst[key].GetName() + '_' + key)

        # produce JES signal shapes
        if args.jesUnc:
		for q in range(1, hSignal.GetNbinsX()+1):
			xLow = hSignal.GetXaxis().GetBinLowEdge(q)
			xUp = hSignal.GetXaxis().GetBinLowEdge(q+1)
			jes = 1. - jesValue
			xLowPrime = jes*xLow
			xUpPrime = jes*xUp
			hSigSyst['JESDown'].SetBinContent(q, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
			jes = 1. + jesValue
			xLowPrime = jes*xLow
			xUpPrime = jes*xUp
			hSigSyst['JESUp'].SetBinContent(q, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
			hSigSystDataHist['JESUp'] = RooDataHist('hSignalJESUp','hSignalJESUp',RooArgList(massAve),hSigSyst['JESUp'])
			hSigSystDataHist['JESDown'] = RooDataHist('hSignalJESDown','hSignalJESDown',RooArgList(massAve),hSigSyst['JESDown'])

        # produce JER signal shapes
	if args.jerUnc:
		for i in range(1, hSignal.GetNbinsX()+1):
			xLow = hSignal.GetXaxis().GetBinLowEdge(i)
			xUp = hSignal.GetXaxis().GetBinLowEdge(i+1)
			jer = 1. - jerValue
			xLowPrime = jer*(xLow-float(signalMass))+float(signalMass)
			xUpPrime = jer*(xUp-float(signalMass))+float(signalMass)
			hSigSyst['JERDown'].SetBinContent(i, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
			jer = 1. + jerValue
			xLowPrime = jer*(xLow-float(signalMass))+float(signalMass)
			xUpPrime = jer*(xUp-float(signalMass))+float(signalMass)
			hSigSyst['JERUp'].SetBinContent(i, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
		hSigSystDataHist['JERUp'] = RooDataHist('hSignalJERUp','hSignalJERUp',RooArgList(massAve),hSigSyst['JERUp'])
		hSigSystDataHist['JERDown'] = RooDataHist('hSignalJERDown','hSignalJERDown',RooArgList(massAve),hSigSyst['JERDown'])

	'''
	#####################################################################
	hSigSyst = signalUnc( hSignal, signalMass ) 
        hSigSystDataHist = {}
        if args.jesUnc:
		hSigSystDataHist['JESUp'] = RooDataHist('hSignalJESUp','hSignalJESUp',RooArgList(massAve),hSigSyst['JESUp'])
		hSigSystDataHist['JESDown'] = RooDataHist('hSignalJESDown','hSignalJESDown',RooArgList(massAve),hSigSyst['JESDown'])

	if args.jerUnc:
		hSigSystDataHist['JERUp'] = RooDataHist('hSignalJERUp','hSignalJERUp',RooArgList(massAve),hSigSyst['JERUp'])
		hSigSystDataHist['JERDown'] = RooDataHist('hSignalJERDown','hSignalJERDown',RooArgList(massAve),hSigSyst['JERDown'])


	#################################### Background
	if args.altBkg:
		newBkgHistoFile = datahistosFile.replace( 'DATA', 'DATA_ABCDBkg' )
		newBkgFile = TFile( newBkgHistoFile )
		htmpBkg = newBkgFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_DATA_ABCDProj' )
		if (htmpBkg.GetBinWidth( 1 ) != args.reBin ): 
			print '|----- Bin size in DATA_C histogram is different than rest.'
			sys.exit(0)
	else: 
		htmpBkg = dataFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_DATA_ABCDProj')
		htmpBkg.Rebin( args.reBin )
	#hBkg = histosFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_QCDPtAll_ABCDProj')
	#hBkg = histosFile.Get(hist+'_QCDPtAll_BCD')
	#htmpBkg = htmpBkg.Rebin( len( boostedMassAveBins )-1, htmpBkg.GetName(), boostedMassAveBins )
	hBkg = htmpBkg.Clone()
	hBkg.Reset()
	for ibin in range( htmpBkg.GetNbinsX() ):
		binCont = htmpBkg.GetBinContent( ibin )
		binErr = htmpBkg.GetBinError( ibin )
		if binCont == 0:
			hBkg.SetBinContent( ibin, 0 )
			hBkg.SetBinError( ibin, 1.8 )
		else:
			hBkg.SetBinContent( ibin, binCont )
			hBkg.SetBinError( ibin, binErr )
	#hBkg.Scale(1/hBkg.Integral())
	hPseudo = hBkg.Clone()
        #background_norm = RooRealVar('background_norm','background_norm',bkgAcc,0.,1e+07)
        #background_norm = RooRealVar('background_norm','background_norm',1.,0.,1e+07)
        #background_norm.Print()
	if not args.isData:
		newNumEvents = random.randint( bkgAcc-round(TMath.Sqrt(bkgAcc)), bkgAcc+round(TMath.Sqrt(bkgAcc)) )
		print 'Events in MC:', bkgAcc, ', in PseudoExperiment:', newNumEvents
		hPseudo.FillRandom( hBkg, newNumEvents ) 
		#hPseudo.Scale(1/hPseudo.Integral())

	###### Adding statistical uncertanty
	hBkgStatUncUp = hBkg.Clone()
	hBkgStatUncUp.Reset()
	hBkgStatUncDown = hBkg.Clone()
	hBkgStatUncDown.Reset()
	for i in range( hBkg.GetNbinsX()+1 ):
		cont = hBkg.GetBinContent(i) 
		contErr = hBkg.GetBinError(i)
		hBkgStatUncUp.SetBinContent( i,  cont + (1*contErr) )
		hBkgStatUncDown.SetBinContent( i, cont - (1*contErr) )
	hBkgStatUncUpDataHist = RooDataHist( 'hBkgStatUncUp', 'hBkgStatUncUp', RooArgList(massAve), hBkgStatUncUp )
	hBkgStatUncDownDataHist = RooDataHist( 'hBkgStatUncDown', 'hBkgStatUncDown', RooArgList(massAve), hBkgStatUncDown )

	if 'template' in args.technique:
		rooBkgHist = RooDataHist( 'rooBkgHist', 'rooBkgHist', RooArgList(massAve), hBkg )
		bkgAcc = rooBkgHist.sumEntries()
		rooBkgHist.Print()
		background = RooHistPdf('background','background',RooArgSet(massAve),rooBkgHist)
		background.Print()

	else:
		massAveBkg = RooRealVar( 'massAveBkg', 'massAveBkg', minMass, maxMass  )
		p1 = RooRealVar('p1','p1', 1 ,0.,100.)
		p2 = RooRealVar('p2','p2', 1 ,0.,60.)
		p3 = RooRealVar('p3','p3', 1 , -10.,10.)

		bkgAcc = round(hBkg.Integral( hBkg.GetXaxis().FindBin( minMass ), hBkg.GetXaxis().FindBin( maxMass )), 2)
		background = RooGenericPdf('background','(pow(1-@0/%.1f,@1)/pow(@0/%.1f,@2+@3*log(@0/%.1f)))'%(1300,1300,1300),RooArgList(massAveBkg,p1,p2,p3))
		background.Print()


        hBkgSyst = {}
        hBkgSystDataHist = {}

	if args.bkgUnc:
		print ' |---> Adding bkg unc'
		hBkgSyst['BkgUncUp'] = hBkg.Clone()
		hBkgSyst['BkgUncDown'] = hBkg.Clone()

		for key in hBkgSyst:
			hBkgSyst[key].Reset()
			hBkgSyst[key].SetName(hBkgSyst[key].GetName() + '_' + key)

		for q in range(0, hBkg.GetNbinsX()):
			binCont = hBkg.GetBinContent( q )
			bkgUncUp = 1. + (args.bkgUncValue/100.)
			hBkgSyst['BkgUncUp'].SetBinContent(q, binCont*bkgUncUp )
			bkgUncDown = 1. - (args.bkgUncValue/100.)
			hBkgSyst['BkgUncDown'].SetBinContent(q, binCont*bkgUncDown )
		hBkgSystDataHist['BkgUncUp'] = RooDataHist('hBkgBkgUncUp','hBkgBkgUncUp',RooArgList(massAve),hBkgSyst['BkgUncUp'])
		hBkgSystDataHist['BkgUncDown'] = RooDataHist('hBkgBkgUncDown','hBkgBkgUncDown',RooArgList(massAve),hBkgSyst['BkgUncDown'])

	############################################################################################


	#model = RooAddPdf("model","s+b",RooArgList(background,signal),RooArgList(background_norm,signal_norm))
	#res = model.fitTo(rooDataHist, RooFit.Save(kTRUE), RooFit.Strategy(0))
	#res.Print()


	############################ Create Workspace
	myWS = RooWorkspace("myWS")
        getattr(myWS,'import')(rooBkgHist,RooFit.Rename("background"))
        #getattr(myWS,'import')(background,RooFit.Rename("background"))
        #getattr(myWS,'import')(signal_norm)
        #getattr(myWS,'import')(background_norm)
	'''
	if 'gaus' in args.technique: 
		getattr(myWS,'import')(signalPdf,RooFit.Rename("signal")) 
		if args.jesUnc:
			getattr(myWS,'import')(signalPdfJESUp,RooFit.Rename("signal__JESUp")) 
			getattr(myWS,'import')(signalPdfJESDown,RooFit.Rename("signal__JESDown")) 
	else: 
	'''
	getattr(myWS,'import')(rooSigHist,RooFit.Rename("signal"))
	if args.jesUnc:
		getattr(myWS,'import')(hSigSystDataHist['JESUp'],RooFit.Rename("signal__JESUp"))
		getattr(myWS,'import')(hSigSystDataHist['JESDown'],RooFit.Rename("signal__JESDown"))
	if args.jerUnc:
		getattr(myWS,'import')(hSigSystDataHist['JERUp'],RooFit.Rename("signal__JERUp"))
		getattr(myWS,'import')(hSigSystDataHist['JERDown'],RooFit.Rename("signal__JERDown"))
        if args.bkgUnc:
		getattr(myWS,'import')(hBkgSystDataHist['BkgUncUp'],RooFit.Rename("background__BkgUncUp"))
		getattr(myWS,'import')(hBkgSystDataHist['BkgUncDown'],RooFit.Rename("background__BkgUncDown"))
	getattr(myWS,'import')(hBkgStatUncUpDataHist, RooFit.Rename("background__BkgStatUncUp") )
	getattr(myWS,'import')(hBkgStatUncDownDataHist, RooFit.Rename("background__BkgStatUncDown") )
        getattr(myWS,'import')(rooDataHist,RooFit.Rename("data_obs"))
        myWS.Print()
	outputRootFile = currentDir+'/Rootfiles/workspace_'+outputName+'.root'
        myWS.writeToFile(outputRootFile, True)
	print ' |----> Workspace created in root file:\n', outputRootFile
	'''
	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
#	c1.SetLogy()
	xframe = myWS.var("massAve").frame()
	signalPdf.plotOn( xframe )
	xframe.Draw()
	c1.SaveAs('test.png')
	del c1
	'''
	############################################################################################
        
	
	######################### write a datacard

	dataCardName = currentDir+'/Datacards/datacard_'+outputName+'.txt'
        datacard = open( dataCardName ,'w')
        datacard.write('imax 1\n')
        datacard.write('jmax 1\n')
        datacard.write('kmax *\n')
        datacard.write('---------------\n')
        if args.jesUnc or args.jerUnc or args.lumiUnc or args.bkgUnc or args.unc: 
		datacard.write('shapes * * '+outputRootFile+' myWS:$PROCESS myWS:$PROCESS__$SYSTEMATIC\n')
	else: datacard.write("shapes * * "+outputRootFile+" myWS:$PROCESS \n")
        datacard.write('---------------\n')
        datacard.write('bin '+signalSample+'\n')
        datacard.write('observation -1\n')
        datacard.write('------------------------------\n')
        datacard.write('bin          '+signalSample+'          '+signalSample+'\n')
        datacard.write('process      signal     background\n')
        datacard.write('process      0          1\n')
        #datacard.write('rate         -1         -1\n')
        datacard.write('rate         '+str(sigAcc)+'         '+str(bkgAcc)+'\n')
        datacard.write('------------------------------\n')
	if args.lumiUnc: datacard.write('lumi  lnN    %f         -\n'%(lumiValue))
	if args.puUnc: datacard.write('pu  lnN    %f         -\n'%(puValue))
        if args.jesUnc: datacard.write('JES  shape   1          -\n')
	if args.jerUnc: datacard.write('JER  shape   1          -\n')
        #flat parameters --- flat prior
	#if args.bkgUnc: datacard.write('BkgUnc  shape   -	   '+str( round( 1/ (args.bkgUncValue/34.1), 2 ) )+'\n')
	if args.bkgUnc: datacard.write('BkgUnc  shape   -	   1 \n')
	#NcombineUnc = ( 1 / TMath.Sqrt( args.bkgUncValue / 100. ) ) - 1
	#datacard.write('background_norm  gmN '+str(int(round(NcombineUnc)))+'  -  '+str( round(bkgAcc/NcombineUnc,2) )+'\n')
        #datacard.write('p1  flatParam\n')
	datacard.write('BkgStatUnc  shape   -	   1 \n')
        datacard.close()
	print ' |----> Datacard created:\n', dataCardName
	############################################################################################

	########## Theta
	if args.theta:
		print ' |----> Creating Theta file\n', outputFileTheta
		outFile = TFile( outputFileTheta, 'update')
		tmpName = 'rpvstopjj'+str(signalMass) 
		hSignal.SetName('massAve__'+tmpName)
		hSignal.Write()
		hSigSyst['JESDown'].SetName('massAve__'+tmpName+'__jes__down' )
		hSigSyst['JESDown'].Write()
		hSigSyst['JESUp'].SetName('massAve__'+tmpName+'__jes__up' )
		hSigSyst['JESUp'].Write()
		hSigSyst['JERDown'].SetName('massAve__'+tmpName+'__jer__down' )
		hSigSyst['JERDown'].Write()
		hSigSyst['JERUp'].SetName('massAve__'+tmpName+'__jer__up' )
		hSigSyst['JERUp'].Write()
		if (signalMass == 100): #or (signalMass == 170):
			hBkg.SetName('massAve__background')
			hBkg.Write()
			hBkgSyst['BkgUncDown'].SetName('massAve__background__unc__down')
			hBkgSyst['BkgUncDown'].Write()
			hBkgSyst['BkgUncUp'].SetName('massAve__background__unc__up')
			hBkgSyst['BkgUncUp'].Write()
			hData.SetName('massAve__DATA')
			hData.Write()
		outFile.Close()
	############################################################################################


def createGausShapes( name, xmin, xmax, rebinX, labX, labY, log):
	"""docstring for plot"""

	#selection = [ 'low', 'high' ]
	selection = [ 'low' ]
	gausParam = {}
	histos = {}
	newGausFunct = {}

	for sel in selection:
		constList = []
		constErrList = []
		numEventsList = []
		numEventsErrList = []
		meanList = []
		meanErrList = []
		sigmaList = []
		sigmaErrList = []
		#if 'low' in sel: massList = [ 80, 90, 100, 110, 120, 130, 140, 150 ]
		#else: massList = [ 170, 180, 190, 210, 220, 230, 240, 300, 350 ] 
		massList = [ 80, 90, 100, 110, 120, 130, 140, 150, 170, 180, 190, 210, 220, 230, 240, 300, 350 ]
		for xmass in massList:
			inFileSample = currentDir+'/../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str(xmass)+'_'+sel+'_v05p2.root'
			if xmass < 150 : massWindow = 10 
			elif ( xmass > 150 ) and ( xmass < 230 ) : massWindow = 20 
			else: massWindow = 30
			gStyle.SetOptFit(1)
			signalHistosFile = TFile.Open( inFileSample )
			hSignal = signalHistosFile.Get( name+'_RPVStopStopToJets_UDD312_M-'+str(xmass))
			hSignal.Rebin( rebinX )
			htmpSignal = hSignal.Clone()
			htmpSignal.Reset()
			sigGaus = TF1( 'sigGaus', 'gaus', 0, 500 )
			for i in range(2): 
				sigGaus.SetParameter( 1, xmass )
				hSignal.Fit( sigGaus, 'MIR', '', xmass-massWindow, xmass+massWindow )
			gausParam[ xmass ] = sigGaus 
			numEventsList.append( sigGaus.Integral( 0, 500 ) )
			numEventsErrList.append( sigGaus.IntegralError( 0, 500 ) )
			constList.append( sigGaus.GetParameter( 0 ) )
			constErrList.append( sigGaus.GetParError( 0 ) )
			meanList.append( sigGaus.GetParameter( 1 ) )
			meanErrList.append( sigGaus.GetParError( 1 ) )
			sigmaList.append( sigGaus.GetParameter( 2 ) )
			sigmaErrList.append( sigGaus.GetParError( 2 ) )
			can1 = TCanvas('c'+str(xmass), 'c'+str(xmass),  10, 10, 750, 500 )
			hSignal.GetXaxis().SetRangeUser( xmass-50 , xmass+50 )
			hSignal.Draw()
			can1.SaveAs( 'Plots/test'+str(xmass)+'.png' )
			del can1
			#for q in range( hSignal.GetNbinsX()+1 ):
			#	gausEval = sigGaus.Eval( hSignal.GetXaxis().GetBinCenter( q ) )
			#	htmpSignal.SetBinContent( q, gausEval )
			#histos[ xmass ] = htmpSignal 
		
		zeroList = [0]*len(massList)
		numEventsGraph = TGraphErrors( len( massList ), array( 'd', massList), array( 'd', numEventsList), array('d', zeroList ), array( 'd', numEventsErrList) )
		canNumEvents = TCanvas('NumberEvents', 'NumberEvents',  10, 10, 750, 500 )
		gStyle.SetOptFit(1)
		if 'high' in sel: 
			canNumEvents.SetLogy()
			numEventsFit = TF1("numEventsFit", "expo", 150, 500 )
		else:
			numEventsFit = TF1("numEventsFit", "pol2", 50, 200 )
		for i in range(3): numEventsGraph.Fit( numEventsFit, 'MIR' )
		numEventsGraph.SetMarkerStyle( 21 )
		numEventsGraph.GetXaxis().SetTitle('Average pruned mass [GeV]')
		numEventsGraph.GetYaxis().SetTitle('Number of Events')
		numEventsGraph.GetYaxis().SetTitleOffset(0.95)
		numEventsGraph.Draw('AP')
		canNumEvents.SaveAs( 'Plots/NumberEvents_'+sel+'.png' )
		del canNumEvents

		constGraph = TGraphErrors( len( massList ), array( 'd', massList), array( 'd', constList), array('d', zeroList ), array( 'd', constErrList) )
		canConstant = TCanvas('Constant', 'Constant',  10, 10, 750, 500 )
		gStyle.SetOptFit(1)
		if 'high' in sel: 
			canConstant.SetLogy()
			constFit = TF1("constFit", "expo", 150, 500 )
		else:
			constFit = TF1("constFit", "pol2", 50, 200 )
		for i in range(3): constGraph.Fit( constFit, 'MIR' )
		constGraph.SetMarkerStyle( 21 )
		constGraph.GetXaxis().SetTitle('Average pruned mass [GeV]')
		constGraph.GetYaxis().SetTitle('Number of Events')
		constGraph.GetYaxis().SetTitleOffset(0.95)
		constGraph.Draw('AP')
		canConstant.SaveAs( 'Plots/Constant_'+sel+'.png' )
		del canConstant

		meanGraph = TGraphErrors( len( massList ), array( 'd', massList), array( 'd', meanList), array('d', zeroList ), array( 'd', meanErrList) )
		meanFit = TF1("meanFit", "pol2", 50, 200 )
		for i in range(3): meanGraph.Fit( meanFit, 'MIR' )
		can1 = TCanvas('MeanGaus', 'MeanGaus',  10, 10, 750, 500 )
		gStyle.SetOptFit(1)
		meanGraph.SetMarkerStyle( 21 )
		meanGraph.GetXaxis().SetTitle('Average pruned mass [GeV]')
		meanGraph.GetYaxis().SetTitle('Mean')
		meanGraph.GetYaxis().SetTitleOffset(0.95)
		meanGraph.Draw('AP')
		can1.SaveAs( 'Plots/MeanGaus_'+sel+'.png' )

		sigmaGraph = TGraphErrors( len( massList ), array( 'd', massList), array( 'd', sigmaList), array('d', zeroList ), array( 'd', sigmaErrList) )
		sigmaFit = TF1("sigmaFit", "expo", 0, 400 )
		for i in range(3): sigmaGraph.Fit( sigmaFit, 'MIR' )
		canSigma = TCanvas('SigmaGaus', 'SigmaGaus',  10, 10, 750, 500 )
		gStyle.SetOptStat(1)
		sigmaGraph.SetMarkerStyle( 21 )
		sigmaGraph.GetXaxis().SetTitle('Average pruned mass [GeV]')
		sigmaGraph.GetYaxis().SetTitle('Sigma')
		sigmaGraph.GetYaxis().SetTitleOffset(0.95)
		sigmaGraph.Draw('aps')
		sigmaFit.Draw('sames')
		canSigma.Update()
		canSigma.SaveAs( 'Plots/SigmaGaus_'+sel+'.png' )
		del canSigma

		#if 'low' in sel: massList2 = [ 80, 90, 100, 110, 120, 130, 140, 150 ]
		#else: massList2 = range( 160, 400, 10 )
		for xmass in range(80, 400, 10 ): #massList2:#
			sigNewGaus = TF1( 'sigNewGaus', 'gaus', 0, 500 )
			sigNewGaus.SetParameter( 0, constFit.Eval( xmass ) )
			sigNewGaus.SetParameter( 1, xmass )
			sigNewGaus.SetParameter( 2, sigmaFit.Eval( xmass ) )
			newGausFunct[ xmass ] = sigNewGaus 
	dummy=1
	can1 = TCanvas('c', 'c',  10, 10, 750, 500 )
	gausParam[ 80 ].Draw()
	gausParam[ 80 ].GetXaxis().SetRangeUser( 50, 400  )
	for x in gausParam:
		if x != 80: 
			gausParam[ x ].SetLineColor(dummy)
			gausParam[ x ].Draw("same")
		dummy=dummy+1
	can1.SaveAs( 'Plots/GaussShapes.png' )
	del can1

	dummy2 = 1
	canNewGaus = TCanvas('canNewGaus', 'canNewGaus',  10, 10, 750, 500 )
	canNewGaus.SetLogy()
	newGausFunct[ 80 ].Draw()
	newGausFunct[ 80 ].GetXaxis().SetRangeUser( 50, 450  )
	newGausFunct[ 80 ].SetMinimum(0.001)
	for x in newGausFunct:
		if x != 80: 
			newGausFunct[ x ].SetLineColor(dummy2)
			newGausFunct[ x ].Draw("same")
		dummy2=dummy2+1
	canNewGaus.SaveAs( 'Plots/NewGaussShapes.png' )
	del canNewGaus
	return newGausFunct

def binByBinCards( datahistosFile, bkghistosFile, signalFile, signalSample, hist, signalMass, signalMassWidth, minMass, maxMass, outputName ):
	"""docstring for binByBinCards"""

	dataFile = TFile( datahistosFile )
	hData = dataFile.Get( hist+'_DATA')
	hData.Rebin ( args.reBin )

	####################### Signal 
	if 'gaus' in args.technique: 
		hSignal = TH1F( 'massAve_RPVStop', 'massAve_RPVStop', maxMass/args.reBin, minMass, maxMass)
		for q in range( hSignal.GetNbinsX()+1 ):
			gausEval = signalFile.Eval( hSignal.GetXaxis().GetBinCenter( q ) )
			hSignal.SetBinContent( q, gausEval )
	else:
		signalHistosFile = TFile( signalFile )
		hSignal = signalHistosFile.Get(hist+'_'+signalSample)
		hSignal.Rebin( args.reBin )
	hSigSyst = signalUnc( hSignal, signalMass ) 

	##### Bkg estimation
	hDataC = dataFile.Get( 'massAve_prunedMassAsymVsdeltaEtaDijet_DATA_C')
	hDataC.Rebin ( args.reBin )
	if args.altBkg:
		newBkgHistoFile = datahistosFile.replace( 'DATA', 'DATA_ABCDBkg' )
		newBkgFile = TFile( newBkgHistoFile )
		hDataRatioBD = newBkgFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_DATA_RatioBD' )
		if (hDataRatioBD.GetBinWidth( 1 ) != args.reBin ): 
			print '|----- Bin size in DATA_C histogram is different than rest.'
			sys.exit(0)
	else:
		hDataB = dataFile.Get( 'massAve_prunedMassAsymVsdeltaEtaDijet_DATA_B')
		hDataB.Rebin ( args.reBin )
		hDataD = dataFile.Get( 'massAve_prunedMassAsymVsdeltaEtaDijet_DATA_D')
		hDataD.Rebin ( args.reBin )

	lowEdgeWindow = int(signalMass/args.reBin -  2*( int( signalMassWidth )/args.reBin ))
	highEdgeWindow = int(signalMass/args.reBin + 2*( int( signalMassWidth )/args.reBin ))
	#print lowEdgeWindow*args.reBin, highEdgeWindow*args.reBin

	combineCards = 'combineCards.py '
	for ibin in range( lowEdgeWindow, highEdgeWindow+1):

		### Signal
		sigAcc = hSignal.GetBinContent( ibin )
		if ( sigAcc == 0 ) : continue
		sigStatUnc = 1+ ( abs(hSignal.GetBinError( ibin )-sigAcc)/sigAcc) 
		if args.jerUnc:
			sigAccJERDown = 1 - ( abs( hSigSyst['JERDown'].GetBinContent( ibin ) - sigAcc )/ sigAcc )
			sigAccJERUp = 1 + ( abs( hSigSyst['JERUp'].GetBinContent( ibin ) - sigAcc ) / sigAcc )
			if (sigAccJERDown < 0) or (sigAccJERUp > 2 ):
				print '-'*30, lowEdgeWindow*args.reBin, highEdgeWindow*args.reBin
				print ibin*args.reBin, hSigSyst['JERUp'].GetBinContent( ibin ), hSigSyst['JERDown'].GetBinContent( ibin ), sigAcc, sigAccJERDown, sigAccJERUp
				continue
		if args.jesUnc:
			sigAccJESDown = 1 - ( abs(hSigSyst['JESDown'].GetBinContent( ibin ) - sigAcc )/ sigAcc )
			sigAccJESUp = 1 + ( abs(hSigSyst['JESUp'].GetBinContent( ibin ) - sigAcc )/ sigAcc )
			if (sigAccJESDown < 0) or (sigAccJESUp > 2 ):
				print '-'*30, lowEdgeWindow*args.reBin, highEdgeWindow*args.reBin
				print ibin*args.reBin, hSigSyst['JESUp'].GetBinContent( ibin ), hSigSyst['JESDown'].GetBinContent( ibin ), sigAcc, sigAccJESDown, sigAccJESUp
				sys.exit(0)
		#print sigAccJERDown, sigAccJERUp, sigAccJESDown, sigAccJESUp

		### data
		contData = hData.GetBinContent( ibin )

		### bkg
		contDataC = hDataC.GetBinContent( ibin )
		if args.altBkg:
			tf = hDataRatioBD.GetBinContent( ibin )
			errBD = 1+ ( hDataRatioBD.GetBinError( ibin ) / tf )
		else:
			contDataB = hDataB.GetBinContent( ibin )
			contDataD = hDataD.GetBinContent( ibin )
			try: tf = contDataB/contDataD
			except ZeroDivisionError: tf = 0
			try: errBD = 1 + (TMath.Sqrt( TMath.Power( TMath.Sqrt( contDataD ) / contDataD, 2 ) + TMath.Power( TMath.Sqrt( contDataB ) / contDataB, 2 ) ) / tf )
			except ZeroDivisionError: errBD = 1
		bkgAcc = tf * contDataC

		dataCardName = currentDir+'/Datacards/datacard_'+outputName+'_bin'+str(ibin)+'.txt'
		datacard = open( dataCardName ,'w')
		datacard.write('imax 1\n')
		datacard.write('jmax 1\n')
		datacard.write('kmax *\n')
		datacard.write('---------------\n')
		datacard.write('bin '+signalSample+'bin'+str(ibin)+'\n')
		datacard.write('observation '+str(int(contData))+'\n')
		datacard.write('------------------------------\n')
		datacard.write('bin          '+signalSample+'bin'+str(ibin)+'          '+signalSample+'bin'+str(ibin)+'\n')
		datacard.write('process      signal     background\n')
		datacard.write('process      0          1\n')
		datacard.write('rate         '+str(sigAcc)+'         '+str(bkgAcc)+'\n')
		datacard.write('------------------------------\n')
		if args.lumiUnc: datacard.write('lumi  lnN    %f         -\n'%(lumiValue))
		if args.puUnc: datacard.write('pu  lnN    %f         -\n'%(puValue))
		if args.jesUnc: datacard.write('JES  lnN   '+str(sigAccJESDown)+'/'+str(sigAccJESUp)+'          -\n')
		if args.jerUnc: datacard.write('JER  lnN   '+str(sigAccJERDown)+'/'+str(sigAccJERUp)+'          -\n')
		datacard.write('BkgUnc'+str(ibin)+'  gmN   '+str(int(contDataC))+'  -	   '+str(tf)+'\n')
		if args.bkgUnc: 
			datacard.write('tfUnc  lnN	-	'+str(1+(args.bkgUncValue/100.))+'\n')
			datacard.write('tfStatUnc'+str(ibin)+'  lnN	-	'+str(errBD)+'\n')
		datacard.write('SigStatUnc'+str(ibin)+'  lnN   '+str(sigStatUnc)+'        -\n')
		datacard.close()
		combineCards += 'Name'+str(ibin)+'='+dataCardName+' '
		print ' |----> Datacard created:\n', dataCardName
	print combineCards, '>', currentDir+'/Datacards/datacard_'+outputName+'_bins.txt'


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--technique', action='store', dest='technique', default='template', help='Process: template or fit.' )
	parser.add_argument('-d', '--data', dest='isData', type=bool, default=True, help='Data: data or pseudoData.' )
	parser.add_argument('-i', '--injSig', dest='signalInjec', type=bool, default=False, help='Signal injection test.' )
	#parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-l', '--lumiUnc', dest='lumiUnc', type=bool, default=False, help='Luminosity, example: 1.' )
	parser.add_argument('-n', '--bkgUnc', dest='bkgUnc', type=bool, default=False, help='Normalization unc.' )
	parser.add_argument('-nV', '--bkgUncValue', dest='bkgUncValue', type=int, default=10, help='Value for bkg nomralization uncertainty.' )
	parser.add_argument('-p', '--puUnc', dest='puUnc', type=bool, default=False, help='Pileup unc.' )
    	parser.add_argument('-s', "--jesUnc", dest="jesUnc", type=bool, default=False, help="Relative uncertainty in the jet energy scale")
    	parser.add_argument('-r', "--jerUnc", dest="jerUnc", type=bool, default=False, help="Relative uncertainty in the jet resolution")
	parser.add_argument('-u', '--unc', dest='unc', type=bool, default=False, help='Luminosity, example: 1.' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-b', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-a', '--altBkg', action='store', type=bool, default=False, help='Regular ABCD (False) or alternative ABCD (true).' )
	parser.add_argument('-R', '--rebin', dest='reBin', type=int, default=1, help='Data: data or pseudoData.' )
    	parser.add_argument('-e', "--theta", dest="theta", type=bool, default=False, help="Create theta file.")
	parser.add_argument('-v', '--version', action='store', default='v05', dest='version', help='Version of rootfiles: v05.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	if args.unc: 
		args.lumiUnc = True
		args.jesUnc = True
		args.jerUnc = True
		args.bkgUnc = True
		args.puUnc = True

	###### Input parameters
	masses = OrderedDict()
	minMass = 50 
	maxMass = 350 #300 
	jesValue = 0.02
	jerValue = 0.1
	puValue = 1.015
	lumiValue = 1.027
	lumi = 2666

	outputFileTheta = ''
	if args.theta:
		outputFileTheta = currentDir+'/Rootfiles/theta_histos_Bin'+str(args.reBin)+'_low_'+args.version+'.root'
		if 'gaus' in args.technique: outputFileTheta = outputFileTheta.replace(args.version, args.version+'_GaussShape')
		if args.altBkg:  outputFileTheta = outputFileTheta.replace(args.version, args.version+'_altBkg')
		files = glob.glob(outputFileTheta)
		for f in files: os.remove(f)

	if 'gaus' in args.technique: 
		gausFunctList = createGausShapes( 'massAve_deltaEtaDijet', 0, 500, args.reBin, 0.85, 0.45, False )
		massList = range( 80, 360, 10 )
		massWidthList = [ ]
	else: 
		massList = [ 80, 90, 100, 110, 120, 130, 140, 150, 170, 180, 190, 210, 220, 230, 240, 300 ]
		massWidthList = [8.56280909196305, 8.445039648677378, 8.950556420141245, 9.860254339542022, 8.814786972730516, 10.021433248818914, 10.392360104091987, 9.435770844457956, 10.268425520508536, 10.45176971177987, 12.86644189449206, 10.084924444431165, 12.431737065699405, 10.809084324420656, 12.94592267653858, 15.762703291273564]

		#massList = [ 130 ]

	for mass in range( len(massList) ):
		signalSample = 'RPVStopStopToJets_UDD312_M-'+str(massList[mass])
		if args.version in [ 'v05' ]:
			if massList[ mass ] < 155: RANGE='low'
			else: RANGE='high'
		else:
			RANGE = 'low'
		dataFileHistos = currentDir+'/../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_DATA_'+RANGE+'_'+( 'v05' if 'v05p2' in args.version else args.version)+'.root'
		bkgFileHistos = currentDir+'/../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCDPtAll_'+RANGE+'_'+( 'v05' if 'v05p2' in args.version else args.version)+'.root'
		#if args.unc: outputName = signalSample+'_'+args.version+'_BkgEst30'
		if args.unc: outputName = signalSample+'_Bin'+str(args.reBin)+'_'+args.version
		else: outputName = signalSample+'_NOSys_'+args.version
		if args.signalInjec: outputName = outputName.replace( signalSample, signalSample+'_signalInjectionTest' )
		if args.altBkg: outputName = outputName.replace( signalSample, signalSample+'_altBkg' )
		if 'gaus' in args.technique: 
			outputName = outputName+'_GaussShape'
			signalFileHistos = gausFunctList[ massList[ mass ] ] 
		else: 
			signalFileHistos = currentDir+'/../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str( massList[mass] )+'_'+RANGE+'_'+args.version+'.root'

		print '#'*50 
		print ' |----> Creating datacard and workspace for RPV St', str( massList[ mass ] )
		print '#'*50 
		if 'bin' in args.technique: p = Process( target=binByBinCards, args=( dataFileHistos, TFile(bkgFileHistos), signalFileHistos, signalSample, 'massAve_deltaEtaDijet', massList[ mass ], massWidthList[ mass ],  minMass, maxMass, outputName ) )
		else: p = Process( target=shapeCards, args=( dataFileHistos, TFile(bkgFileHistos), signalFileHistos, signalSample, 'massAve_deltaEtaDijet', massList[ mass ], minMass, maxMass, outputName, outputFileTheta ) )
		p.start()
		p.join()
